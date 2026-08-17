"""Workflow de scoring CENSOPAS-COPSOQ (harness §27-31).

Regla absoluta (§62): este módulo nunca recibe objetos `Participant` — sólo
trabaja con `response_session_id`/`study_id`, ya anónimos por diseño (los
`response_sessions` no llevan `participant_id`, ver harness §12).
"""

from __future__ import annotations

import hashlib
import json
import statistics
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.analytics.censopas.classification import classify_collective_result, classify_construct_score
from app.analytics.censopas.scoring import derive_item_values
from app.core.exceptions import (
    ConflictError,
    InsufficientSampleError,
    NotFoundError,
    ValidationDomainError,
)
from app.models.analysis import AnalysisRun
from app.models.censopas import Barem, BaremBand, BaremCutoff, ConstructResult, ConstructScore, ResponseScore
from app.models.construct import Construct, ConstructItem
from app.models.option_set import OptionSet, OptionSetOption
from app.models.question import Question
from app.models.response import Response, ResponseSession, ResponseSessionUnit
from app.models.study import StudyUnit, StudyUnitType
from app.models.scoring import ScoringRule
from app.repositories.censopas import CensopasRepository
from app.repositories.instruments import InstrumentRepository
from app.repositories.responses import valid_session_ids
from app.repositories.studies import StudyRepository
from app.schemas.censopas import (
    BaremBandGenerate,
    BaremBandsReplace,
    BaremCreate,
    BaremEditableCopyCreate,
    BaremCutoffCreate,
    CensopasManifest,
    CensopasManifestImportRead,
    CensopasManifestValidation,
    CensopasBaremImportRead,
    CensopasBaremManifest,
    CensopasBaremManifestValidation,
    ScoringRuleCreate,
)
from app.services.instrument_edit_policy import InstrumentEditPolicy
from app.services.privacy_service import PrivacyService


class CensopasScoringService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = CensopasRepository(session)
        self.study_repo = StudyRepository(session)
        self.instrument_repo = InstrumentRepository(session)

    @staticmethod
    def validate_manifest_payload(
        payload: CensopasManifest,
    ) -> CensopasManifestValidation:
        canonical = payload.model_dump(mode="json", exclude={"declared_hash"})
        calculated_hash = hashlib.sha256(
            json.dumps(
                canonical,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        expected = (
            {
                "questions": 42,
                "scored": 31,
                "descriptive": 11,
                "dimensions": 6,
                "subdimensions": 0,
            }
            if payload.version_kind == "SHORT"
            else {
                "questions": 112,
                "scored": 69,
                "descriptive": 43,
                "dimensions": 6,
                "subdimensions": 20,
            }
        )
        scored_questions = [
            question for question in payload.questions if question.is_scored
        ]
        actual = {
            "questions": len(payload.questions),
            "scored": len(scored_questions),
            "descriptive": len(payload.questions) - len(scored_questions),
            "dimensions": sum(
                construct.construct_type == "DIMENSION"
                for construct in payload.constructs
            ),
            "subdimensions": sum(
                construct.construct_type == "SUBDIMENSION"
                for construct in payload.constructs
            ),
        }
        errors: list[str] = []
        warnings: list[str] = []

        def add_error(code: str) -> None:
            if code not in errors:
                errors.append(code)

        for field, expected_value in expected.items():
            if actual[field] != expected_value:
                add_error(f"{field.upper()}_COUNT_MISMATCH")

        question_codes = [question.code for question in payload.questions]
        source_codes = [question.source_code for question in payload.questions]
        question_orders = [question.sort_order for question in payload.questions]
        scale_codes = [scale.code for scale in payload.scales]
        construct_codes = [construct.code for construct in payload.constructs]
        rule_codes = [rule.question_code for rule in payload.scoring_rules]
        if len(question_codes) != len(set(question_codes)):
            add_error("DUPLICATE_QUESTION_CODES")
        if len(source_codes) != len(set(source_codes)):
            add_error("DUPLICATE_SOURCE_CODES")
        if len(question_orders) != len(set(question_orders)):
            add_error("DUPLICATE_QUESTION_ORDER")
        if len(scale_codes) != len(set(scale_codes)):
            add_error("DUPLICATE_SCALE_CODES")
        if len(construct_codes) != len(set(construct_codes)):
            add_error("DUPLICATE_CONSTRUCT_CODES")
        if len(rule_codes) != len(set(rule_codes)):
            add_error("DUPLICATE_SCORING_RULES")

        questions_by_code = {question.code: question for question in payload.questions}
        scales_by_code = {scale.code: scale for scale in payload.scales}
        constructs_by_code = {construct.code: construct for construct in payload.constructs}
        rules_by_question = {rule.question_code: rule for rule in payload.scoring_rules}
        for scale in payload.scales:
            raw_codes = [option.raw_code for option in scale.options]
            values = [option.numeric_value for option in scale.options]
            if len(raw_codes) != len(set(raw_codes)):
                add_error("DUPLICATE_SCALE_RAW_CODES")
            if len(values) != len(set(values)):
                add_error("DUPLICATE_SCALE_VALUES")

        linked_scored: set[str] = set()
        for construct in payload.constructs:
            if construct.construct_type == "VARIABLE" and construct.parent_code is not None:
                add_error("VARIABLE_WITH_PARENT")
            if construct.construct_type in ("DIMENSION", "SUBDIMENSION"):
                if not construct.parent_code or construct.parent_code not in constructs_by_code:
                    add_error("INVALID_CONSTRUCT_PARENT")
            if construct.construct_type == "DIMENSION" and construct.parent_code:
                parent = constructs_by_code.get(construct.parent_code)
                if parent and parent.construct_type != "VARIABLE":
                    add_error("DIMENSION_PARENT_MUST_BE_VARIABLE")
            if construct.construct_type == "SUBDIMENSION" and construct.parent_code:
                parent = constructs_by_code.get(construct.parent_code)
                if parent and parent.construct_type != "DIMENSION":
                    add_error("SUBDIMENSION_PARENT_MUST_BE_DIMENSION")
            for link in construct.items:
                question = questions_by_code.get(link.question_code)
                if question is None:
                    add_error("UNKNOWN_LINKED_QUESTION")
                    continue
                if link.item_role == "SCORED":
                    if construct.construct_type not in ("DIMENSION", "SUBDIMENSION"):
                        add_error("SCORED_ITEM_OUTSIDE_SCORING_TREE")
                    if link.scoring_direction not in ("DIRECT", "REVERSE"):
                        add_error("MISSING_SCORING_DIRECTION")
                    linked_scored.add(link.question_code)

        for question in scored_questions:
            if question.question_type != "LIKERT":
                add_error("SCORED_QUESTION_NOT_LIKERT")
            if not question.option_set_code or question.option_set_code not in scales_by_code:
                add_error("SCORED_QUESTION_WITHOUT_SCALE")
            if question.code not in linked_scored:
                add_error("SCORED_QUESTION_OUTSIDE_DIMENSION_TREE")
            rule = rules_by_question.get(question.code)
            if rule is None:
                add_error("MISSING_SCORING_RULE")
                continue
            scale = scales_by_code.get(question.option_set_code or "")
            if scale is not None:
                raw_codes = {option.raw_code for option in scale.options}
                if set(rule.risk_map) != raw_codes:
                    add_error("INCOMPLETE_RISK_MAP")
            if any(value < 1 or value > 5 for value in rule.risk_map.values()):
                add_error("RISK_MAP_OUT_OF_RANGE")

        for question in payload.questions:
            if question.option_set_code and question.option_set_code not in scales_by_code:
                add_error("UNKNOWN_OPTION_SET")
        if payload.declared_hash and payload.declared_hash.lower() != calculated_hash:
            add_error("DECLARED_HASH_MISMATCH")
        if not payload.declared_hash:
            warnings.append("DECLARED_HASH_NOT_PROVIDED")

        return CensopasManifestValidation(
            valid=not errors,
            calculated_hash=calculated_hash,
            errors=errors,
            warnings=warnings,
            expected=expected,
            actual=actual,
        )

    async def import_manifest(
        self,
        instrument_version_id: int,
        payload: CensopasManifest,
    ) -> CensopasManifestImportRead:
        version = await self.instrument_repo.get_version_with_instrument(
            instrument_version_id
        )
        if version is None:
            raise NotFoundError(
                f"Versión de instrumento {instrument_version_id} no encontrada"
            )
        await InstrumentEditPolicy.can_edit_question(
            self.session, version.instrument, version
        )
        validation = self.validate_manifest_payload(payload)
        if not validation.valid:
            raise ValidationDomainError(
                "El manifiesto CENSOPAS no superó la validación.",
                validation=validation.model_dump(mode="json"),
            )

        existing_models = (Question, Construct, OptionSet, ScoringRule)
        for model in existing_models:
            stmt = select(model).where(
                model.instrument_version_id == instrument_version_id
            )
            if (await self.session.execute(stmt)).scalars().first() is not None:
                raise ConflictError(
                    "La importación sólo se permite sobre una versión vacía; clone o cree una versión DRAFT.",
                    model=model.__name__,
                )

        try:
            scales_by_code: dict[str, OptionSet] = {}
            for scale_data in payload.scales:
                scale = OptionSet(
                    instrument_version_id=instrument_version_id,
                    owner_user_id=version.instrument.owner_user_id,
                    code=scale_data.code,
                    name=scale_data.name,
                    metadata_={"manifest_hash": validation.calculated_hash},
                    options=[
                        OptionSetOption(
                            raw_code=option.raw_code,
                            label=option.label,
                            numeric_value=option.numeric_value,
                            sort_order=option.sort_order,
                            is_active=True,
                        )
                        for option in scale_data.options
                    ],
                )
                self.session.add(scale)
                await self.session.flush()
                scales_by_code[scale_data.code] = scale

            questions_by_code: dict[str, Question] = {}
            for question_data in payload.questions:
                question = Question(
                    instrument_version_id=instrument_version_id,
                    option_set_id=(
                        scales_by_code[question_data.option_set_code].id
                        if question_data.option_set_code
                        else None
                    ),
                    code=question_data.code,
                    source_code=question_data.source_code,
                    question_text=question_data.question_text,
                    question_type=question_data.question_type,
                    research_role=question_data.research_role,
                    category=question_data.category,
                    is_scored=question_data.is_scored,
                    is_required_default=question_data.is_required,
                    sort_order=question_data.sort_order,
                    metadata_={
                        **question_data.metadata,
                        "manifest_hash": validation.calculated_hash,
                    },
                )
                self.session.add(question)
                await self.session.flush()
                questions_by_code[question_data.code] = question

            constructs_by_code: dict[str, Construct] = {}
            pending = list(payload.constructs)
            while pending:
                progressed = False
                for construct_data in list(pending):
                    if (
                        construct_data.parent_code
                        and construct_data.parent_code not in constructs_by_code
                    ):
                        continue
                    construct = Construct(
                        instrument_version_id=instrument_version_id,
                        parent_id=(
                            constructs_by_code[construct_data.parent_code].id
                            if construct_data.parent_code
                            else None
                        ),
                        code=construct_data.code,
                        name=construct_data.name,
                        construct_type=construct_data.construct_type,
                        sort_order=construct_data.sort_order,
                        metadata_={
                            **construct_data.metadata,
                            "manifest_hash": validation.calculated_hash,
                        },
                    )
                    self.session.add(construct)
                    await self.session.flush()
                    constructs_by_code[construct_data.code] = construct
                    pending.remove(construct_data)
                    progressed = True
                if not progressed:
                    raise ValidationDomainError("La jerarquía del manifiesto contiene un ciclo.")

            for construct_data in payload.constructs:
                construct = constructs_by_code[construct_data.code]
                for link in construct_data.items:
                    self.session.add(
                        ConstructItem(
                            construct_id=construct.id,
                            question_id=questions_by_code[link.question_code].id,
                            weight=link.weight,
                            item_role=link.item_role,
                            scoring_direction=link.scoring_direction,
                            sort_order=link.sort_order,
                            metadata_={"manifest_hash": validation.calculated_hash},
                        )
                    )

            for rule_data in payload.scoring_rules:
                question = questions_by_code[rule_data.question_code]
                self.session.add(
                    ScoringRule(
                        instrument_version_id=instrument_version_id,
                        question_id=question.id,
                        rule_code=f"CENSOPAS_{rule_data.question_code}",
                        rule_type="RISK_MAP",
                        parameters={"risk_map": rule_data.risk_map},
                        source_reference=rule_data.source_reference or payload.source_reference,
                        rule_version=rule_data.rule_version,
                        status="VALIDATED",
                    )
                )

            version.source_reference = payload.source_reference
            version.scoring_status = "CONFIGURED"
            version.config = {
                **version.config,
                "censopas_version_kind": payload.version_kind,
                "censopas_expected": validation.expected,
                "manifest_version": payload.manifest_version,
                "manifest_hash": validation.calculated_hash,
            }
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        readiness = await self.get_readiness(instrument_version_id)
        return CensopasManifestImportRead(
            instrument_version_id=instrument_version_id,
            manifest_hash=validation.calculated_hash,
            imported={
                "scales": len(payload.scales),
                "questions": len(payload.questions),
                "constructs": len(payload.constructs),
                "scoring_rules": len(payload.scoring_rules),
            },
            readiness=readiness,
        )

    async def get_readiness(self, instrument_version_id: int) -> dict:
        version = await self.instrument_repo.get_version_with_instrument(instrument_version_id)
        if version is None:
            raise NotFoundError(f"Versión de instrumento {instrument_version_id} no encontrada")

        version_token = " ".join(
            filter(None, (version.version_code, version.version_name, version.edition))
        ).upper()
        configured_kind = version.config.get("censopas_version_kind")
        if configured_kind == "MEDIUM":
            version_kind = "MEDIUM"
            defaults = {
                "questions": 112,
                "scored": 69,
                "descriptive": 43,
                "dimensions": 6,
                "subdimensions": 20,
            }
        elif configured_kind == "SHORT":
            version_kind = "SHORT"
            defaults = {
                "questions": 42,
                "scored": 31,
                "descriptive": 11,
                "dimensions": 6,
                "subdimensions": 0,
            }
        elif any(token in version_token for token in ("MEDIUM", "MEDIA")):
            version_kind = "MEDIUM"
            defaults = {
                "questions": 112,
                "scored": 69,
                "descriptive": 43,
                "dimensions": 6,
                "subdimensions": 20,
            }
        elif any(token in version_token for token in ("SHORT", "CORTA")):
            version_kind = "SHORT"
            defaults = {
                "questions": 42,
                "scored": 31,
                "descriptive": 11,
                "dimensions": 6,
                "subdimensions": 0,
            }
        else:
            version_kind = "UNKNOWN"
            defaults = {}

        configured = version.config.get("censopas_expected", {})
        expected = {**defaults, **configured}
        questions = list(
            (
                await self.session.execute(
                    select(Question).where(
                        Question.instrument_version_id == instrument_version_id
                    )
                )
            )
            .scalars()
            .all()
        )
        constructs = list(
            (
                await self.session.execute(
                    select(Construct)
                    .where(Construct.instrument_version_id == instrument_version_id)
                    .options(selectinload(Construct.item_links))
                )
            )
            .scalars()
            .all()
        )
        scored_questions = {question.id for question in questions if question.is_scored}
        instrument_token = " ".join(
            filter(None, (version.instrument.code, version.instrument.name))
        ).upper()
        if version_kind == "UNKNOWN" and "CENSOPAS" in instrument_token:
            inferred_kind = (
                "SHORT"
                if len(scored_questions) == 31
                else "MEDIUM"
                if len(scored_questions) == 69
                else None
            )
            if inferred_kind == "SHORT":
                version_kind = "SHORT"
                expected = {
                    "questions": 42,
                    "scored": 31,
                    "descriptive": 11,
                    "dimensions": 6,
                    "subdimensions": 0,
                    **configured,
                }
            elif inferred_kind == "MEDIUM":
                version_kind = "MEDIUM"
                expected = {
                    "questions": 112,
                    "scored": 69,
                    "descriptive": 43,
                    "dimensions": 6,
                    "subdimensions": 20,
                    **configured,
                }
        dimensions = [c for c in constructs if c.construct_type == "DIMENSION"]
        subdimensions = [c for c in constructs if c.construct_type == "SUBDIMENSION"]
        scored_constructs = dimensions + subdimensions
        linked_scored = {
            link.question_id
            for construct in scored_constructs
            for link in construct.item_links
            if (link.item_role or "SCORED") == "SCORED"
        }
        rules = await self.repo.list_scoring_rules(instrument_version_id)
        ruled_questions = {
            rule.question_id
            for rule in rules
            if rule.question_id is not None and rule.status in ("ACTIVE", "VALIDATED")
        }
        actual = {
            "questions": len(questions),
            "scored": len(scored_questions),
            "descriptive": len(questions) - len(scored_questions),
            "dimensions": len(dimensions),
            "subdimensions": len(subdimensions),
            "scoring_rules": len(ruled_questions & scored_questions),
            "linked_scored": len(linked_scored & scored_questions),
        }

        errors: list[str] = []
        warnings: list[str] = []
        if version_kind == "UNKNOWN":
            errors.append("UNSUPPORTED_CENSOPAS_VERSION")
        for field in ("questions", "scored", "descriptive", "dimensions", "subdimensions"):
            if field in expected and actual[field] != expected[field]:
                errors.append(f"{field.upper()}_COUNT_MISMATCH")
        if scored_questions - linked_scored:
            errors.append("SCORED_QUESTIONS_OUTSIDE_DIMENSION_TREE")
        if linked_scored - scored_questions:
            errors.append("NON_SCORED_QUESTIONS_IN_SCORING_MATRIX")
        if scored_questions - ruled_questions:
            errors.append("MISSING_VALIDATED_SCORING_RULES")
        if any(not construct.item_links for construct in scored_constructs):
            errors.append("EMPTY_SCORING_CONSTRUCTS")

        required_construct_ids = {construct.id for construct in scored_constructs}
        barems = await self.repo.list_barems(instrument_version_id)
        active_barems = [barem for barem in barems if barem.status == "ACTIVE"]
        official_barem = next(
            (
                barem
                for barem in active_barems
                if barem.metadata_.get("barem_type") == "OFFICIAL"
            ),
            None,
        )
        cutoff_ids: set[int] = set()
        if official_barem is not None:
            loaded_barem = await self.repo.get_barem(official_barem.id)
            cutoff_ids = {cutoff.construct_id for cutoff in loaded_barem.cutoffs}
            if required_construct_ids - cutoff_ids:
                warnings.append("OFFICIAL_BAREM_INCOMPLETE")
        else:
            warnings.append("OFFICIAL_BAREM_NOT_AVAILABLE")

        ready_for_scoring = not errors
        equivalence_enabled = bool(
            version.instrument.metadata_.get("official_equivalence_enabled", False)
        )
        ready_for_official_reporting = bool(
            ready_for_scoring
            and official_barem is not None
            and not (required_construct_ids - cutoff_ids)
            and equivalence_enabled
        )
        if not equivalence_enabled:
            warnings.append("OFFICIAL_EQUIVALENCE_DISABLED")

        return {
            "instrument_version_id": instrument_version_id,
            "version_kind": version_kind,
            "ready_for_scoring": ready_for_scoring,
            "ready_for_official_reporting": ready_for_official_reporting,
            "expected": expected,
            "actual": actual,
            "errors": errors,
            "warnings": warnings,
        }

    async def run_scoring(self, study_id: int) -> AnalysisRun:
        study = await self.study_repo.get(study_id)
        if study is None:
            raise NotFoundError(f"Estudio {study_id} no encontrado")
        if study.instrument_version_id is None:
            raise ValidationDomainError(
                "El estudio no tiene una versión de instrumento asociada; no se puede aplicar scoring."
            )

        version = await self.instrument_repo.get_version_with_instrument(study.instrument_version_id)
        if version is None:
            raise NotFoundError(f"Versión de instrumento {study.instrument_version_id} no encontrada")

        readiness = await self.get_readiness(version.id)
        if (
            readiness["version_kind"] != "UNKNOWN"
            and not readiness["ready_for_scoring"]
        ):
            raise ValidationDomainError(
                "La versión CENSOPAS no está lista para ejecutar scoring.",
                readiness=readiness,
            )

        run = AnalysisRun(
            study_id=study_id,
            analysis_type="CENSOPAS_SCORING",
            status="PENDING",
            parameters={"instrument_version_id": version.id},
        )
        self.session.add(run)
        await self.session.flush()
        run.status = "RUNNING"
        run.started_at = datetime.now(UTC)
        await self.session.flush()

        try:
            constructs = await self._load_constructs(version.id)
            scored_constructs = [c for c in constructs if c.item_links]
            if not scored_constructs:
                raise ValidationDomainError(
                    "La versión del instrumento no tiene constructos DIMENSION/SUBDIMENSION "
                    "con ítems vinculados."
                )

            missing_rules = await self._diagnose_missing_scoring_rules(scored_constructs, version.id)
            if missing_rules:
                run.parameters = {**run.parameters, "missing_scoring_rules": missing_rules}
                raise ValidationDomainError(
                    "Faltan scoring_rules para uno o más ítems puntuables; cárguelas con "
                    "POST /instrument-versions/{id}/scoring-rules antes de ejecutar el scoring.",
                    missing_scoring_rules=missing_rules,
                )

            sessions = await self._load_valid_sessions(study_id)
            if not sessions:
                raise InsufficientSampleError(
                    "No hay sesiones COMPLETED con validation_status=VALID para calcular "
                    "el scoring CENSOPAS."
                )

            barem = await self.repo.get_barem(study.barem_id) if study.barem_id else None
            session_units = await self._load_session_units(study_id)
            cutoffs_by_construct = {c.construct_id: c for c in barem.cutoffs} if barem else {}

            unmapped_by_construct: dict[str, list[str]] = {}
            built_results: list[ConstructResult] = []
            for construct in scored_constructs:
                session_scores, unmapped = await self._score_construct_for_sessions(
                    construct, sessions, version.id, run.id
                )
                if unmapped:
                    unmapped_by_construct[construct.code] = sorted(unmapped)
                cutoff = cutoffs_by_construct.get(construct.id)
                for response_session_id, score, n_answered, n_total in session_scores:
                    classification = None
                    if cutoff is not None:
                        classification = classify_construct_score(
                            score,
                            float(cutoff.cut_1),
                            float(cutoff.cut_2),
                            cutoff.direction,
                            cutoff.favorable_label,
                            cutoff.intermediate_label,
                            cutoff.unfavorable_label,
                        )
                    await self.repo.add_construct_score(
                        ConstructScore(
                            study_id=study_id,
                            analysis_run_id=run.id,
                            response_session_id=response_session_id,
                            construct_id=construct.id,
                            barem_id=barem.id if barem else None,
                            n_answered=n_answered,
                            n_total=n_total,
                            completion_pct=round((n_answered / n_total) * 100, 4) if n_total else 0,
                            score_0_100=score,
                            classification=classification,
                            algorithm_version="censopas-v2",
                            metadata_={"scoring_chain": "raw_code -> risk_value -> score_0_100"},
                        )
                    )
                result = self._build_construct_result(
                    study_id,
                    run.id,
                    construct,
                    [score for _, score, _, _ in session_scores],
                    cutoff,
                    barem,
                )
                built_results.append(result)
                await self.repo.add_construct_result(result)

                unit_scores: dict[tuple[int, int], list[float]] = {}
                for response_session_id, score, _n_answered, _n_total in session_scores:
                    for unit_type_id, unit_id in session_units.get(
                        response_session_id, []
                    ):
                        unit_scores.setdefault((unit_type_id, unit_id), []).append(score)
                for (unit_type_id, unit_id), grouped_scores in unit_scores.items():
                    unit_result = self._build_construct_result(
                        study_id,
                        run.id,
                        construct,
                        grouped_scores,
                        cutoff,
                        barem,
                    )
                    unit_result.unit_type_id = unit_type_id
                    unit_result.unit_id = unit_id
                    unit_result.metadata_ = {
                        "aggregation": "STUDY_UNIT",
                        "min_publishable_n": study.min_publishable_n,
                    }
                    await self.repo.add_construct_result(unit_result)

            if all(result.n_valid == 0 for result in built_results):
                run.parameters = {**run.parameters, "unmapped_codes": unmapped_by_construct}
                raise ValidationDomainError(
                    "El scoring CENSOPAS produjo cero casos válidos en todos los constructos; "
                    "verifique que los raw_code registrados coincidan con las scoring_rules.",
                    unmapped_codes=unmapped_by_construct,
                )

            run.status = "COMPLETED"
            run.completed_at = datetime.now(UTC)
            await self.session.flush()
            await self.session.commit()
        except Exception as exc:
            run.status = "FAILED"
            run.completed_at = datetime.now(UTC)
            run.error_message = str(exc)
            await self.session.flush()
            await self.session.commit()
            raise

        return run

    async def _load_constructs(self, instrument_version_id: int) -> list[Construct]:
        stmt = (
            select(Construct)
            .where(
                Construct.instrument_version_id == instrument_version_id,
                Construct.construct_type.in_(("DIMENSION", "SUBDIMENSION")),
            )
            .options(
                selectinload(Construct.item_links).selectinload(ConstructItem.question)
            )
        )
        return list((await self.session.execute(stmt)).scalars().all())

    async def _diagnose_missing_scoring_rules(
        self, constructs: list[Construct], instrument_version_id: int
    ) -> list[dict]:
        missing: list[dict] = []
        for construct in constructs:
            for link in construct.item_links:
                if (link.item_role or "SCORED") != "SCORED":
                    continue
                rule = await self.repo.get_scoring_rule_for_question(
                    instrument_version_id, link.question_id
                )
                if rule is None:
                    missing.append(
                        {
                            "construct_id": construct.id,
                            "construct_code": construct.code,
                            "question_id": link.question_id,
                            "question_code": link.question.code if link.question else None,
                        }
                    )
        return missing

    async def _load_session_units(
        self, study_id: int
    ) -> dict[int, list[tuple[int, int]]]:
        """Sesión -> unidades a las que pertenece, incluidas sus ancestras.

        `StudyUnit.parent_id` permite agrupar unidades pequeñas bajo una
        unidad organizacional mayor (p.ej. "Contabilidad"/"Tesorería" bajo
        "Administración financiera") sin re-etiquetar las sesiones: cada
        sesión asignada a una unidad hija también se propaga a sus
        ancestras, de modo que la unidad agregadora reciba el conteo
        combinado y pueda publicarse aunque las hijas por separado no
        alcancen `min_publishable_n` (ver `get_unit_results`).
        """
        stmt = (
            select(
                ResponseSessionUnit.response_session_id,
                StudyUnitType.id,
                StudyUnit.id,
            )
            .join(
                StudyUnit,
                StudyUnit.id == ResponseSessionUnit.study_unit_id,
            )
            .join(
                StudyUnitType,
                StudyUnitType.id == StudyUnit.study_unit_type_id,
            )
            .join(
                ResponseSession,
                ResponseSession.id == ResponseSessionUnit.response_session_id,
            )
            .where(ResponseSession.study_id == study_id)
        )
        rows = (await self.session.execute(stmt)).all()
        mapping: dict[int, list[tuple[int, int]]] = {}
        for response_session_id, unit_type_id, unit_id in rows:
            mapping.setdefault(response_session_id, []).append(
                (unit_type_id, unit_id)
            )

        all_unit_ids = {unit_id for pairs in mapping.values() for _, unit_id in pairs}
        if not all_unit_ids:
            return mapping

        info_by_unit: dict[int, tuple[int, int | None]] = {}
        pending = set(all_unit_ids)
        while pending:
            units_stmt = select(
                StudyUnit.id, StudyUnit.study_unit_type_id, StudyUnit.parent_id
            ).where(StudyUnit.id.in_(pending))
            rows = (await self.session.execute(units_stmt)).all()
            pending = set()
            for unit_id, unit_type_id, parent_id in rows:
                info_by_unit[unit_id] = (unit_type_id, parent_id)
                if parent_id is not None and parent_id not in info_by_unit:
                    pending.add(parent_id)

        for response_session_id, pairs in mapping.items():
            expanded = list(pairs)
            seen = set(pairs)
            for _unit_type_id, unit_id in pairs:
                _, ancestor_id = info_by_unit.get(unit_id, (None, None))
                while ancestor_id is not None:
                    ancestor_type_id, next_ancestor_id = info_by_unit.get(
                        ancestor_id, (None, None)
                    )
                    key = (ancestor_type_id, ancestor_id)
                    if key not in seen:
                        expanded.append(key)
                        seen.add(key)
                    ancestor_id = next_ancestor_id
            mapping[response_session_id] = expanded
        return mapping

    async def _load_valid_sessions(self, study_id: int) -> list[ResponseSession]:
        stmt = select(ResponseSession).where(ResponseSession.id.in_(valid_session_ids(study_id)))
        return list((await self.session.execute(stmt)).scalars().all())

    async def _score_construct_for_sessions(
        self,
        construct: Construct,
        sessions: list[ResponseSession],
        instrument_version_id: int,
        analysis_run_id: int,
    ) -> tuple[list[tuple[int, float, int, int]], set[str]]:
        scores: list[tuple[int, float, int, int]] = []
        unmapped_codes: set[str] = set()
        for response_session in sessions:
            weighted_scores: list[tuple[float, float]] = []
            n_total = sum(
                1 for link in construct.item_links if (link.item_role or "SCORED") == "SCORED"
            )
            for link in construct.item_links:
                rule = await self.repo.get_scoring_rule_for_question(
                    instrument_version_id, link.question_id
                )
                if rule is None:
                    continue

                response = await self._get_response(response_session.id, link.question_id)
                if response is None or response.is_missing:
                    continue

                values = derive_item_values(
                    response.raw_code,
                    rule.parameters.get("risk_map", rule.parameters.get("map", {})),
                    link.scoring_direction,
                )
                if values is None:
                    if response.raw_code is not None:
                        unmapped_codes.add(response.raw_code)
                    continue

                risk_value, score_0_100 = values
                await self.repo.add_response_score(
                    ResponseScore(
                        response_id=response.id,
                        scoring_rule_id=rule.id,
                        risk_value=risk_value,
                        score_0_100=score_0_100,
                        algorithm_version="censopas-v2",
                        metadata_={
                            "analysis_run_id": analysis_run_id,
                            "construct_id": construct.id,
                            "direction": link.scoring_direction,
                        },
                    )
                )
                weighted_scores.append((score_0_100, float(link.weight)))

            total_weight = sum(weight for _, weight in weighted_scores)
            if total_weight > 0:
                construct_score = sum(
                    score * weight for score, weight in weighted_scores
                ) / total_weight
                scores.append(
                    (response_session.id, construct_score, len(weighted_scores), n_total)
                )

        return scores, unmapped_codes

    async def _get_response(self, response_session_id: int, question_id: int) -> Response | None:
        stmt = select(Response).where(
            Response.response_session_id == response_session_id, Response.question_id == question_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    def _build_construct_result(
        self,
        study_id: int,
        analysis_run_id: int,
        construct: Construct,
        session_scores: list[float],
        cutoff,
        barem: Barem | None,
    ) -> ConstructResult:
        n_valid = len(session_scores)
        construct_score = statistics.fmean(session_scores) if n_valid else None

        favorable_n = intermediate_n = unfavorable_n = 0
        collective_classification = None

        if cutoff is not None and n_valid:
            labels = [
                classify_construct_score(
                    score,
                    float(cutoff.cut_1),
                    float(cutoff.cut_2),
                    cutoff.direction,
                    cutoff.favorable_label,
                    cutoff.intermediate_label,
                    cutoff.unfavorable_label,
                )
                for score in session_scores
            ]
            favorable_n = labels.count(cutoff.favorable_label)
            intermediate_n = labels.count(cutoff.intermediate_label)
            unfavorable_n = labels.count(cutoff.unfavorable_label)
            collective_classification = classify_collective_result(
                (favorable_n / n_valid) * 100,
                (intermediate_n / n_valid) * 100,
                (unfavorable_n / n_valid) * 100,
            )

        return ConstructResult(
            study_id=study_id,
            analysis_run_id=analysis_run_id,
            construct_id=construct.id,
            n_valid=n_valid,
            favorable_n=favorable_n,
            intermediate_n=intermediate_n,
            unfavorable_n=unfavorable_n,
            favorable_pct=round((favorable_n / n_valid) * 100, 4) if n_valid else None,
            intermediate_pct=round((intermediate_n / n_valid) * 100, 4) if n_valid else None,
            unfavorable_pct=round((unfavorable_n / n_valid) * 100, 4) if n_valid else None,
            construct_score=construct_score,
            classification=collective_classification,
            classification_status="PROVISIONAL",
            barem_id=barem.id if barem else None,
            algorithm_version="censopas-v2",
            metadata_={},
        )

    async def get_results(self, study_id: int) -> list[ConstructResult]:
        results = await self.repo.list_construct_results(study_id)
        if not results:
            return []
        latest_run_id = max(
            (result.analysis_run_id for result in results if result.analysis_run_id is not None),
            default=None,
        )
        return [
            result
            for result in results
            if result.analysis_run_id == latest_run_id and result.unit_id is None
        ]

    async def get_unit_results(
        self, study_id: int, unit_type_id: int
    ) -> dict:
        study = await self.study_repo.get(study_id)
        if study is None:
            raise NotFoundError(f"Estudio {study_id} no encontrado")
        unit_type = await self.session.get(StudyUnitType, unit_type_id)
        if unit_type is None or unit_type.study_id != study_id:
            raise NotFoundError(
                f"Tipo de unidad {unit_type_id} no encontrado en el estudio {study_id}"
            )
        latest_run = await self._latest_run(study_id)
        if latest_run is None or latest_run.status != "COMPLETED":
            raise ConflictError(
                "No existe una corrida CENSOPAS completa para agregar por unidad.",
                latest_run_status=latest_run.status if latest_run else None,
            )
        all_results = await self.repo.list_construct_results(study_id)
        results = [
            result
            for result in all_results
            if result.analysis_run_id == latest_run.id
            and result.unit_type_id == unit_type_id
            and result.unit_id is not None
        ]
        # Todas las unidades del tipo (no sólo las que tienen resultados): se
        # necesitan para recorrer la cadena `parent_id` completa al buscar una
        # unidad ancestra publicable.
        units_stmt = select(StudyUnit).where(StudyUnit.study_unit_type_id == unit_type_id)
        units = {
            unit.id: unit for unit in (await self.session.execute(units_stmt)).scalars().all()
        }

        def _nearest_publishable_ancestor(
            unit_id: int, by_unit: dict[int, ConstructResult]
        ) -> int | None:
            unit = units.get(unit_id)
            ancestor_id = unit.parent_id if unit else None
            while ancestor_id is not None:
                ancestor_result = by_unit.get(ancestor_id)
                if ancestor_result is not None and ancestor_result.n_valid >= study.min_publishable_n:
                    return ancestor_id
                ancestor_unit = units.get(ancestor_id)
                ancestor_id = ancestor_unit.parent_id if ancestor_unit else None
            return None

        secondary_ids: set[int] = set()
        absorbed_ids: set[int] = set()
        # (construct_id, ancestor_unit_id) -> nombres de las unidades hijas
        # que quedaron agrupadas bajo esa ancestra publicable.
        grouped_names: dict[tuple[int, int], list[str]] = {}
        grouped: dict[int, list[ConstructResult]] = {}
        for result in results:
            grouped.setdefault(result.construct_id, []).append(result)
        for construct_id, construct_results in grouped.items():
            by_unit = {result.unit_id: result for result in construct_results}

            # Unidades por debajo del umbral: si tienen una ancestra publicable
            # (n agregado >= min_publishable_n), se agrupan bajo ella y dejan
            # de mostrarse individualmente (harness §31 + agrupación manual
            # de unidades vía `StudyUnit.parent_id`).
            for unit_id, result in by_unit.items():
                if result.n_valid >= study.min_publishable_n:
                    continue
                ancestor_id = _nearest_publishable_ancestor(unit_id, by_unit)
                if ancestor_id is not None:
                    absorbed_ids.add(result.id)
                    unit = units.get(unit_id)
                    grouped_names.setdefault((construct_id, ancestor_id), []).append(
                        unit.name if unit else str(unit_id)
                    )

            visible_results = [
                result for result in construct_results if result.id not in absorbed_ids
            ]
            primary = [
                result for result in visible_results if result.n_valid < study.min_publishable_n
            ]
            publishable = [
                result for result in visible_results if result.n_valid >= study.min_publishable_n
            ]
            if len(primary) == 1 and publishable:
                secondary = min(
                    publishable,
                    key=lambda item: (item.n_valid, item.unit_id),
                )
                secondary_ids.add(secondary.id)

        payload_results = []
        for result in results:
            if result.id in absorbed_ids:
                continue
            is_secondary = result.id in secondary_ids
            privacy = self.apply_privacy(
                result,
                result.n_valid + 1 if is_secondary else study.min_publishable_n,
            )
            unit = units[result.unit_id]
            privacy.update(
                unit_type_id=unit_type.id,
                unit_type_code=unit_type.code,
                unit_type_name=unit_type.name,
                unit_id=unit.id,
                unit_code=unit.code,
                unit_name=unit.name,
                grouped_units=grouped_names.get((result.construct_id, unit.id), []),
                suppression_reason=(
                    "SECONDARY_DEDUCTION_PROTECTION"
                    if is_secondary
                    else "BELOW_MINIMUM_N"
                    if privacy["suppressed"]
                    else None
                ),
            )
            payload_results.append(privacy)
        return {
            "study_id": study_id,
            "unit_type_id": unit_type_id,
            "min_publishable_n": study.min_publishable_n,
            "secondary_suppression_applied": bool(secondary_ids),
            "results": payload_results,
        }

    async def _latest_run(self, study_id: int) -> AnalysisRun | None:
        stmt = (
            select(AnalysisRun)
            .where(
                AnalysisRun.study_id == study_id,
                AnalysisRun.analysis_type == "CENSOPAS_SCORING",
            )
            .order_by(AnalysisRun.created_at.desc(), AnalysisRun.id.desc())
        )
        return (await self.session.execute(stmt)).scalars().first()

    @staticmethod
    def _describe_missing(run: AnalysisRun | None) -> list[str]:
        if run is None:
            return [
                "El estudio aún no tiene una corrida de scoring CENSOPAS. "
                "Ejecute POST /studies/{id}/censopas/scoring."
            ]
        if run.status != "COMPLETED":
            parts: list[str] = []
            if run.parameters.get("missing_scoring_rules"):
                parts.append(f"Faltan scoring_rules: {run.parameters['missing_scoring_rules']}")
            if run.parameters.get("unmapped_codes"):
                parts.append(f"Códigos de respuesta sin mapear: {run.parameters['unmapped_codes']}")
            if not parts and run.error_message:
                parts.append(run.error_message)
            return parts or [f"La última corrida terminó en estado {run.status}."]
        return []

    async def get_results_or_conflict(self, study_id: int) -> list[ConstructResult]:
        latest_run = await self._latest_run(study_id)
        if latest_run is None or latest_run.status != "COMPLETED":
            raise ConflictError(
                "El scoring CENSOPAS no se ha completado exitosamente para este estudio.",
                missing=self._describe_missing(latest_run),
                latest_run_status=latest_run.status if latest_run else None,
            )
        return await self.get_results(study_id)

    # --- Configuración (scoring_rules / barems) — prerequisito administrativo ----

    async def create_scoring_rule(self, instrument_version_id: int, payload: ScoringRuleCreate) -> ScoringRule:
        version = await self.instrument_repo.get_version_with_instrument(instrument_version_id)
        if version is None:
            raise NotFoundError(f"Versión de instrumento {instrument_version_id} no encontrada")
        rule = ScoringRule(
            instrument_version_id=instrument_version_id,
            question_id=payload.question_id,
            construct_id=payload.construct_id,
            rule_code=payload.rule_code,
            rule_type=payload.rule_type,
            parameters=payload.parameters,
            formula_expression=payload.formula_expression,
            source_reference=payload.source_reference,
            rule_version=payload.rule_version,
            status=payload.status,
        )
        rule = await self.repo.add_scoring_rule(rule)
        await self.session.commit()
        return rule

    async def list_scoring_rules(self, instrument_version_id: int) -> list[ScoringRule]:
        return await self.repo.list_scoring_rules(instrument_version_id)

    async def validate_barem_manifest(
        self,
        instrument_version_id: int,
        payload: CensopasBaremManifest,
    ) -> CensopasBaremManifestValidation:
        version = await self.instrument_repo.get_version_with_instrument(
            instrument_version_id
        )
        if version is None:
            raise NotFoundError(
                f"Versión de instrumento {instrument_version_id} no encontrada"
            )
        stmt = select(Construct).where(
            Construct.instrument_version_id == instrument_version_id,
            Construct.construct_type.in_(("DIMENSION", "SUBDIMENSION")),
        )
        constructs = list((await self.session.execute(stmt)).scalars().all())
        required_codes = sorted(construct.code for construct in constructs)
        configured_codes = [cutoff.construct_code for cutoff in payload.cutoffs]
        canonical = payload.model_dump(mode="json", exclude={"declared_hash"})
        calculated_hash = hashlib.sha256(
            json.dumps(
                canonical,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        errors: list[str] = []
        if len(configured_codes) != len(set(configured_codes)):
            errors.append("DUPLICATE_CONSTRUCT_CUTOFFS")
        if set(configured_codes) != set(required_codes):
            errors.append("INCOMPLETE_CONSTRUCT_COVERAGE")
        if any(cutoff.cut_1 >= cutoff.cut_2 for cutoff in payload.cutoffs):
            errors.append("INVALID_CUTOFF_ORDER")
        if payload.barem_type == "OFFICIAL" and not payload.authority:
            errors.append("OFFICIAL_AUTHORITY_REQUIRED")
        if payload.declared_hash and payload.declared_hash.lower() != calculated_hash:
            errors.append("DECLARED_HASH_MISMATCH")
        return CensopasBaremManifestValidation(
            valid=not errors,
            calculated_hash=calculated_hash,
            errors=errors,
            required_constructs=required_codes,
            configured_constructs=sorted(configured_codes),
        )

    async def import_barem_manifest(
        self,
        instrument_version_id: int,
        payload: CensopasBaremManifest,
    ) -> CensopasBaremImportRead:
        validation = await self.validate_barem_manifest(
            instrument_version_id, payload
        )
        if not validation.valid:
            raise ValidationDomainError(
                "El manifiesto de baremo no superó la validación.",
                validation=validation.model_dump(mode="json"),
            )
        constructs_stmt = select(Construct).where(
            Construct.instrument_version_id == instrument_version_id,
            Construct.construct_type.in_(("DIMENSION", "SUBDIMENSION")),
        )
        constructs = list(
            (await self.session.execute(constructs_stmt)).scalars().all()
        )
        constructs_by_code = {construct.code: construct for construct in constructs}
        try:
            barem = Barem(
                instrument_version_id=instrument_version_id,
                name=payload.name,
                population_label=payload.population_label,
                source_reference=payload.source_reference,
                barem_version=payload.barem_version,
                status="DRAFT",
                metadata_={
                    "barem_type": payload.barem_type,
                    "authority": payload.authority,
                    "content_hash": validation.calculated_hash,
                    "official_equivalence": False,
                    "imported_from_manifest": True,
                },
            )
            self.session.add(barem)
            await self.session.flush()
            for cutoff_data in payload.cutoffs:
                self.session.add(
                    BaremCutoff(
                        barem_id=barem.id,
                        construct_id=constructs_by_code[cutoff_data.construct_code].id,
                        cut_1=cutoff_data.cut_1,
                        cut_2=cutoff_data.cut_2,
                        direction=cutoff_data.direction,
                        favorable_label=cutoff_data.favorable_label,
                        intermediate_label=cutoff_data.intermediate_label,
                        unfavorable_label=cutoff_data.unfavorable_label,
                        metadata_={"content_hash": validation.calculated_hash},
                    )
                )
            await self.session.commit()
            await self.session.refresh(barem)
        except Exception:
            await self.session.rollback()
            raise
        return CensopasBaremImportRead(
            barem_id=barem.id,
            status=barem.status,
            barem_type=payload.barem_type,
            content_hash=validation.calculated_hash,
            cutoffs_imported=len(payload.cutoffs),
        )

    async def create_barem(self, instrument_version_id: int, payload: BaremCreate) -> Barem:
        version = await self.instrument_repo.get_version_with_instrument(instrument_version_id)
        if version is None:
            raise NotFoundError(f"Versión de instrumento {instrument_version_id} no encontrada")
        barem = Barem(
            instrument_version_id=instrument_version_id,
            name=payload.name,
            population_label=payload.population_label,
            source_reference=payload.source_reference,
            barem_version=payload.barem_version,
            status=payload.status,
            valid_from=payload.valid_from,
            valid_to=payload.valid_to,
            metadata_=payload.metadata,
        )
        barem = await self.repo.add_barem(barem)
        await self.session.commit()
        return barem

    async def list_barems(self, instrument_version_id: int) -> list[Barem]:
        version = await self.instrument_repo.get_version_with_instrument(instrument_version_id)
        if version is None:
            raise NotFoundError(f"Versión de instrumento {instrument_version_id} no encontrada")
        return await self.repo.list_barems(instrument_version_id)

    async def _root_construct_ids(self, instrument_version_id: int) -> list[int]:
        """Variables raíz que reciben baremos por defecto.

        Dimensiones y subdimensiones conservan su scoring, pero no deben
        multiplicar el editor de niveles del baremo general.
        """
        stmt = (
            select(Construct.id)
            .where(
                Construct.instrument_version_id == instrument_version_id,
                Construct.parent_id.is_(None),
            )
            .order_by(Construct.sort_order, Construct.id)
        )
        return list((await self.session.execute(stmt)).scalars().all())

    async def create_editable_barem_copy(
        self, barem_id: int, payload: BaremEditableCopyCreate
    ) -> Barem:
        source = await self.repo.get_barem(barem_id)
        if source is None:
            raise NotFoundError(f"Baremo {barem_id} no encontrado")

        root_ids = set(await self._root_construct_ids(source.instrument_version_id))
        copied = Barem(
            instrument_version_id=source.instrument_version_id,
            name=payload.name or f"{source.name} — versión editable",
            population_label=source.population_label,
            source_reference=source.source_reference,
            barem_version=payload.barem_version or f"{source.barem_version or 'v1'}-edit",
            status="DRAFT",
            valid_from=source.valid_from,
            valid_to=source.valid_to,
            metadata_={**(source.metadata_ or {}), "copied_from_barem_id": source.id},
        )
        self.session.add(copied)
        await self.session.flush()
        for band in source.bands:
            if band.construct_id not in root_ids:
                continue
            self.session.add(
                BaremBand(
                    barem_id=copied.id,
                    construct_id=band.construct_id,
                    code=band.code,
                    label=band.label,
                    min_value=band.min_value,
                    max_value=band.max_value,
                    severity_order=band.severity_order,
                    interpretation=band.interpretation,
                    color_hint=band.color_hint,
                    classification_code=band.classification_code,
                    metadata_={**(band.metadata_ or {}), "copied_from_band_id": band.id},
                )
            )
        await self.session.commit()
        return await self.repo.get_barem(copied.id)

    @staticmethod
    def _validate_bands(bands) -> None:
        grouped: dict[int, list] = {}
        for band in bands:
            grouped.setdefault(band.construct_id, []).append(band)
        for construct_id, construct_bands in grouped.items():
            ordered = sorted(
                construct_bands, key=lambda item: (float(item.min_value), item.severity_order)
            )
            if len({band.severity_order for band in ordered}) != len(ordered):
                raise ValidationDomainError(
                    f"El constructo {construct_id} repite el orden de severidad."
                )
            if abs(float(ordered[0].min_value)) > 1e-9 or abs(
                float(ordered[-1].max_value) - 100
            ) > 1e-9:
                raise ValidationDomainError(
                    f"Los niveles del constructo {construct_id} deben cubrir de 0 a 100."
                )
            for index, band in enumerate(ordered):
                if float(band.min_value) >= float(band.max_value):
                    raise ValidationDomainError(
                        f"El nivel {band.label} tiene un rango vacío o invertido."
                    )
                if index and abs(
                    float(band.min_value) - float(ordered[index - 1].max_value)
                ) > 1e-6:
                    raise ValidationDomainError(
                        f"Los niveles del constructo {construct_id} tienen huecos o solapamientos."
                    )

    async def replace_bands(self, barem_id: int, payload: BaremBandsReplace) -> Barem:
        barem = await self.repo.get_barem(barem_id)
        if barem is None:
            raise NotFoundError(f"Baremo {barem_id} no encontrado")
        if barem.status == "ACTIVE":
            raise ValidationDomainError(
                "Un baremo activo es inmutable; cree una nueva versión para modificarlo."
            )
        self._validate_bands(payload.bands)
        construct_ids = {band.construct_id for band in payload.bands}
        stmt = select(Construct.id).where(
            Construct.instrument_version_id == barem.instrument_version_id,
            Construct.id.in_(construct_ids),
        )
        valid_ids = set((await self.session.execute(stmt)).scalars().all())
        if construct_ids != valid_ids:
            raise ValidationDomainError(
                "Todos los niveles deben pertenecer a constructos de la versión del instrumento."
            )
        for existing_band in list(barem.bands):
            await self.session.delete(existing_band)
        await self.session.flush()
        barem.bands = [
            BaremBand(
                construct_id=band.construct_id,
                code=band.code,
                label=band.label,
                min_value=band.min_value,
                max_value=band.max_value,
                severity_order=band.severity_order,
                interpretation=band.interpretation,
                color_hint=band.color_hint,
                classification_code=band.classification_code,
                metadata_=band.metadata,
            )
            for band in payload.bands
        ]
        await self.session.commit()
        return await self.repo.get_barem(barem_id)

    async def generate_bands(self, barem_id: int, payload: BaremBandGenerate) -> Barem:
        barem = await self.repo.get_barem(barem_id)
        if barem is None:
            raise NotFoundError(f"Baremo {barem_id} no encontrado")
        if payload.labels and len(payload.labels) != payload.levels:
            raise ValidationDomainError("La cantidad de etiquetas debe coincidir con los niveles.")
        labels = payload.labels or (
            ["Bajo", "Medio", "Alto"]
            if payload.levels == 3
            else ["Muy bajo", "Bajo", "Medio", "Alto", "Muy alto"]
        )
        colors = (
            ["#22c55e", "#f59e0b", "#ef4444"]
            if payload.direction == "LOWER_BETTER"
            else ["#ef4444", "#f59e0b", "#22c55e"]
        )
        if payload.levels == 5:
            colors = list(reversed(["#166534", "#22c55e", "#f59e0b", "#f97316", "#dc2626"]))
            if payload.direction == "LOWER_BETTER":
                colors = list(reversed(colors))

        stmt = select(Construct.id).where(
            Construct.instrument_version_id == barem.instrument_version_id
        )
        all_construct_ids = list((await self.session.execute(stmt)).scalars().all())
        construct_ids = (
            payload.construct_ids
            if payload.construct_ids is not None
            else await self._root_construct_ids(barem.instrument_version_id)
        )
        if not construct_ids:
            raise ValidationDomainError("La versión no tiene constructos para generar niveles.")
        if not set(construct_ids).issubset(set(all_construct_ids)):
            raise ValidationDomainError("Uno o más constructos no pertenecen a esta versión.")

        boundaries_by_construct: dict[int, list[float]] = {}
        scoring_run_id = None
        if payload.method == "QUANTILES":
            if payload.study_id is None:
                raise ValidationDomainError(
                    "Para generar cuantiles seleccione el estudio piloto."
                )
            run_stmt = (
                select(AnalysisRun)
                .where(
                    AnalysisRun.study_id == payload.study_id,
                    AnalysisRun.analysis_type == "LIKERT_SCORING",
                    AnalysisRun.status == "COMPLETED",
                )
                .order_by(AnalysisRun.completed_at.desc(), AnalysisRun.id.desc())
            )
            scoring_run = (await self.session.execute(run_stmt)).scalars().first()
            if scoring_run is None:
                raise ValidationDomainError(
                    "El estudio piloto todavía no tiene una corrida de scoring Likert."
                )
            scoring_run_id = scoring_run.id
            for construct_id in construct_ids:
                values_stmt = select(ConstructScore.score_0_100).where(
                    ConstructScore.analysis_run_id == scoring_run.id,
                    ConstructScore.construct_id == construct_id,
                    ConstructScore.score_0_100.is_not(None),
                )
                values = [
                    float(value) for value in (await self.session.execute(values_stmt)).scalars().all()
                ]
                if len(values) < payload.levels:
                    raise ValidationDomainError(
                        f"El constructo {construct_id} necesita al menos {payload.levels} "
                        "puntajes piloto para calcular cuantiles."
                    )
                cuts = statistics.quantiles(values, n=payload.levels, method="inclusive")
                boundaries = [0.0, *cuts, 100.0]
                if any(
                    boundaries[index] >= boundaries[index + 1]
                    for index in range(len(boundaries) - 1)
                ):
                    raise ValidationDomainError(
                        f"El constructo {construct_id} no tiene variabilidad suficiente "
                        "para producir niveles cuantílicos distintos."
                    )
                boundaries_by_construct[construct_id] = boundaries
        else:
            width = 100 / payload.levels
            boundaries_by_construct = {
                construct_id: [
                    round(index * width, 8) for index in range(payload.levels)
                ]
                + [100.0]
                for construct_id in construct_ids
            }

        bands = []
        for construct_id in construct_ids:
            boundaries = boundaries_by_construct[construct_id]
            for index, label in enumerate(labels):
                min_value = boundaries[index]
                max_value = boundaries[index + 1]
                classification_codes = (
                    ["UNFAVORABLE", "INTERMEDIATE", "FAVORABLE"]
                    if payload.direction == "HIGHER_BETTER" and payload.levels == 3
                    else ["FAVORABLE", "INTERMEDIATE", "UNFAVORABLE"]
                    if payload.levels == 3
                    else [f"LEVEL_{index + 1}"] * payload.levels
                )
                bands.append(
                    {
                        "construct_id": construct_id,
                        "code": f"NIVEL_{index + 1}",
                        "label": label,
                        "min_value": min_value,
                        "max_value": max_value,
                        "severity_order": index + 1,
                        "color_hint": colors[index],
                        "classification_code": classification_codes[index],
                        "metadata": {
                            "generated": True,
                            "generation_method": payload.method,
                            "pilot_study_id": payload.study_id,
                            "scoring_run_id": scoring_run_id,
                            "direction": payload.direction,
                        },
                    }
                )
        return await self.replace_bands(barem_id, BaremBandsReplace(bands=bands))

    async def activate_barem(self, barem_id: int) -> Barem:
        barem = await self.repo.get_barem(barem_id)
        if barem is None:
            raise NotFoundError(f"Baremo {barem_id} no encontrado")
        validations: list[str] = []
        if not barem.source_reference:
            validations.append("Falta la fuente metodológica del baremo.")
        if not barem.population_label:
            validations.append("Falta la población de referencia del baremo.")
        if not barem.barem_version:
            validations.append("Falta la versión del baremo.")
        if barem.metadata_.get("barem_type") != "OFFICIAL" and not barem.bands:
            validations.append("El baremo no tiene niveles configurados.")
        else:
            try:
                self._validate_bands(barem.bands)
            except ValidationDomainError as exc:
                validations.append(str(exc))
            required_construct_ids = set(
                await self._root_construct_ids(barem.instrument_version_id)
            )
            configured_construct_ids = {band.construct_id for band in barem.bands}
            missing_construct_ids = sorted(required_construct_ids - configured_construct_ids)
            if (
                barem.metadata_.get("barem_type") != "OFFICIAL"
                and missing_construct_ids
            ):
                validations.append(
                    f"Faltan niveles para las variables raíz {missing_construct_ids}."
                )
        if barem.metadata_.get("barem_type") == "OFFICIAL":
            stmt = select(Construct.id).where(
                Construct.instrument_version_id == barem.instrument_version_id,
                Construct.construct_type.in_(("DIMENSION", "SUBDIMENSION")),
            )
            required_cutoff_ids = set(
                (await self.session.execute(stmt)).scalars().all()
            )
            configured_cutoff_ids = {cutoff.construct_id for cutoff in barem.cutoffs}
            missing_cutoff_ids = sorted(required_cutoff_ids - configured_cutoff_ids)
            if missing_cutoff_ids:
                validations.append(
                    f"Faltan cortes oficiales C1/C2 para los constructos {missing_cutoff_ids}."
                )
            if not barem.metadata_.get("authority"):
                validations.append("Falta la autoridad del baremo oficial.")
            if not barem.metadata_.get("content_hash"):
                validations.append("Falta el hash auditable del baremo oficial.")
        if validations:
            raise ValidationDomainError(
                "El baremo no cumple los requisitos para activarse.",
                validations=validations,
                barem_id=barem.id,
                status=barem.status,
            )
        barem.status = "ACTIVE"
        await self.session.commit()
        return await self.repo.get_barem(barem_id)

    async def add_cutoff(self, barem_id: int, payload: BaremCutoffCreate) -> BaremCutoff:
        barem = await self.repo.get_barem(barem_id)
        if barem is None:
            raise NotFoundError(f"Barem {barem_id} no encontrado")
        if barem.status == "ACTIVE":
            raise ValidationDomainError(
                "Un baremo activo es inmutable; cree una nueva versión para modificarlo."
            )
        if payload.cut_1 >= payload.cut_2:
            raise ValidationDomainError("cut_1 debe ser menor que cut_2.")
        construct = await self.session.get(Construct, payload.construct_id)
        if (
            construct is None
            or construct.instrument_version_id != barem.instrument_version_id
            or construct.construct_type not in ("DIMENSION", "SUBDIMENSION")
        ):
            raise ValidationDomainError(
                "El corte debe pertenecer a una dimensión o subdimensión de la misma versión."
            )
        cutoff = BaremCutoff(
            barem_id=barem_id,
            construct_id=payload.construct_id,
            cut_1=payload.cut_1,
            cut_2=payload.cut_2,
            direction=payload.direction,
            favorable_label=payload.favorable_label,
            intermediate_label=payload.intermediate_label,
            unfavorable_label=payload.unfavorable_label,
        )
        cutoff = await self.repo.add_cutoff(cutoff)
        await self.session.commit()
        return cutoff

    @staticmethod
    def apply_privacy(result: ConstructResult, min_publishable_n: int) -> dict:
        suppressed = not PrivacyService.can_publish_group(result.n_valid, min_publishable_n)
        data = {
            "construct_id": result.construct_id,
            "construct_code": result.construct.code,
            "construct_name": result.construct.name,
            "n_valid": result.n_valid,
            "suppressed": suppressed,
            "classification_status": result.classification_status,
        }
        if suppressed:
            data.update(
                favorable_n=None,
                intermediate_n=None,
                unfavorable_n=None,
                favorable_pct=None,
                intermediate_pct=None,
                unfavorable_pct=None,
                construct_score=None,
                collective_classification=None,
            )
        else:
            data.update(
                favorable_n=result.favorable_n,
                intermediate_n=result.intermediate_n,
                unfavorable_n=result.unfavorable_n,
                favorable_pct=float(result.favorable_pct) if result.favorable_pct is not None else None,
                intermediate_pct=float(result.intermediate_pct) if result.intermediate_pct is not None else None,
                unfavorable_pct=float(result.unfavorable_pct) if result.unfavorable_pct is not None else None,
                construct_score=float(result.construct_score) if result.construct_score is not None else None,
                collective_classification=result.classification,
            )
        return data
