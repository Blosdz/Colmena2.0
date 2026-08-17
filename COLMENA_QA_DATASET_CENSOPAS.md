# COLMENA — Dataset QA: CENSOPAS-COPSOQ (versión corta y media)

## 0. Qué es este documento

Fixtures **ejecutables** para correr la batería de auditoría descrita en
`COLMENA_TEST_AUDITORIA_CENSOPAS.md` (Dataset A / Dataset B de su §26) contra los endpoints
reales confirmados en `backend/app/api/v1/censopas.py` y los schemas de
`backend/app/schemas/censopas.py` (`CensopasManifest`, `CensopasBaremManifest`).

**Regla de origen de los ítems:** el texto de las preguntas oficiales del método CENSOPAS-COPSOQ
NO está reproducido aquí. Este documento no tiene el banco oficial verificado carácter por
carácter, y `COLMENA_SECCIONES_CENSOPAS_SEGUN_PDFS.md`/`COLMENA_TEST_AUDITORIA_CENSOPAS.md`
tampoco lo transcriben. Inventar 42/112 preguntas "parecidas a las oficiales" y presentarlas como
CENSOPAS sería exactamente lo que el harness prohíbe (§97: no inventar baremos/clasificaciones
para que la UI "se vea completa"). Por eso, igual que hace el propio
`test_censopas_flow.py` del repo (que usa textos como `"Exigencia 1"`), este dataset usa
**placeholders explícitos** (`"Ítem psicosocial D1-01 (QA placeholder)"`). Son válidos para
probar el motor (conteo, scoring, baremo, privacidad, reportes) pero **nunca deben usarse como
manifiesto oficial en producción**. Si existe un manifiesto oficial real en otro lugar
(por ejemplo un archivo `.json`/`.yaml` fuera de este repo o entregado por el evaluador
CENSOPAS), usar ese en vez de este dataset para cualquier prueba de concordancia oficial
(`§28` de la auditoría, `official_equivalence_enabled`).

Los 6 nombres de dimensión (`Exigencias psicológicas`, `Conflicto trabajo-familia`,
`Control sobre el trabajo`, `Apoyo social y calidad de liderazgo`, `Compensaciones`,
`Capital social`) sí están documentados en `COLMENA_SECCIONES_CENSOPAS_SEGUN_PDFS.md` §9.4
(citando el Manual técnico) y se reutilizan aquí tal cual — no son invención de este documento.

---

## 1. Endpoints confirmados que usa este dataset

```text
POST /api/v1/instruments
POST /api/v1/instruments/{id}/versions
POST /api/v1/instrument-versions/{version_id}/validate-manifest      → CensopasManifestValidation
POST /api/v1/instrument-versions/{version_id}/import-manifest        → CensopasManifestImportRead
POST /api/v1/instrument-versions/{version_id}/validate-barem-manifest → CensopasBaremManifestValidation
POST /api/v1/instrument-versions/{version_id}/import-barem-manifest   → CensopasBaremImportRead
GET  /api/v1/instrument-versions/{version_id}/censopas/readiness      → CensopasReadiness
POST /api/v1/projects/{project_id}/surveys/from-instrument
POST /api/v1/projects/{project_id}/studies                            {study_type: "CENSO", ...}
PATCH /api/v1/studies/{study_id}                                      {barem_id}
POST /api/v1/studies/{study_id}/unit-types
POST /api/v1/study-unit-types/{unit_type_id}/units
POST /api/v1/studies/{study_id}/open
POST /api/v1/studies/{study_id}/response-sessions
PUT  /api/v1/response-sessions/{id}/units                             {unit_ids: [...]}
PUT  /api/v1/response-sessions/{id}/responses/{item_id}                {raw_code}
POST /api/v1/response-sessions/{id}/complete
POST /api/v1/studies/{study_id}/censopas/scoring                      → AnalysisRunRead
GET  /api/v1/studies/{study_id}/censopas/results                      → CensopasResultsResponse
GET  /api/v1/studies/{study_id}/censopas/unit-results?unit_type_id=…  → CensopasUnitResultsResponse
```

`study_type: "CENSO"` está confirmado literal en `test_censopas_flow.py:108`.

---

## 2. Manifest QA — versión corta (`version_kind: "SHORT"`)

Objetivo (según `INST-001` de la auditoría): `TOTAL=42`, `PSICOSOCIALES=31`, `DIMENSIONES=6`.
Distribución de los 31 ítems puntuables entre las 6 dimensiones: D1=6, D2=5, D3=5, D4=5, D5=5,
D6=5. Los 11 restantes (hasta 42) son ítems sociodemográficos/descriptivos, `is_scored: false`,
sin construct asociado.

```json
{
  "version_kind": "SHORT",
  "manifest_version": "QA-SHORT-0.1",
  "source_reference": "Dataset QA interno — placeholders, NO es el banco oficial CENSOPAS-COPSOQ",
  "scales": [
    {
      "code": "LIKERT5",
      "name": "Escala Likert 5 puntos (frecuencia)",
      "options": [
        {"raw_code": "1", "label": "Nunca", "numeric_value": 1, "sort_order": 1},
        {"raw_code": "2", "label": "Casi nunca", "numeric_value": 2, "sort_order": 2},
        {"raw_code": "3", "label": "A veces", "numeric_value": 3, "sort_order": 3},
        {"raw_code": "4", "label": "Casi siempre", "numeric_value": 4, "sort_order": 4},
        {"raw_code": "5", "label": "Siempre", "numeric_value": 5, "sort_order": 5}
      ]
    }
  ],
  "questions": [
    "// 31 ítems psicosociales — patrón por dimensión, repetir Dn-0k para k=1..N_dimension",
    {"code": "D1-01", "source_code": "QA-D1-01", "question_text": "Ítem psicosocial D1-01 (QA placeholder)", "question_type": "LIKERT", "is_scored": true, "research_role": "ENDOGENOUS", "option_set_code": "LIKERT5", "is_required": true},
    "// ... D1-02 .. D1-06 (6 ítems), D2-01..D2-05 (5), D3-01..D3-05 (5), D4-01..D4-05 (5), D5-01..D5-05 (5), D6-01..D6-05 (5) = 31 total",
    "// 11 ítems sociodemográficos no puntuables",
    {"code": "SOC-01", "source_code": "QA-SOC-01", "question_text": "Edad (rango) — QA placeholder", "question_type": "SINGLE_CHOICE", "is_scored": false, "option_set_code": null, "is_required": true},
    "// ... SOC-02 .. SOC-11 (sexo, área, puesto, contrato, turno, antigüedad, etc.) = 11 total"
  ],
  "constructs": [
    {"code": "D1", "name": "Exigencias psicológicas", "construct_type": "DIMENSION", "items": [
      {"question_code": "D1-01", "weight": 1, "item_role": "SCORED", "scoring_direction": "DIRECT"},
      "// ... D1-02..D1-06, todas DIRECT salvo que se quiera probar REVERSE en al menos 1 ítem (recomendado para SCORE-001)"
    ]},
    {"code": "D2", "name": "Conflicto trabajo-familia", "construct_type": "DIMENSION", "items": ["// D2-01..D2-05"]},
    {"code": "D3", "name": "Control sobre el trabajo", "construct_type": "DIMENSION", "items": ["// D3-01..D3-05"]},
    {"code": "D4", "name": "Apoyo social y calidad de liderazgo", "construct_type": "DIMENSION", "items": ["// D4-01..D4-05"]},
    {"code": "D5", "name": "Compensaciones", "construct_type": "DIMENSION", "items": ["// D5-01..D5-05"]},
    {"code": "D6", "name": "Capital social", "construct_type": "DIMENSION", "items": ["// D6-01..D6-05"]}
  ],
  "scoring_rules": [
    {"question_code": "D1-01", "risk_map": {"1": 0, "2": 25, "3": 50, "4": 75, "5": 100}, "rule_version": "QA-0.1"},
    "// repetir risk_map idéntico para los 31 ítems psicosociales (ajustar por REVERSE si aplica: {\"1\":100,\"2\":75,\"3\":50,\"4\":25,\"5\":0})"
  ]
}
```

El bloque de arriba es una **plantilla**, no JSON literal completo (los `"// ..."` marcan
expansión mecánica). Generarlo completo con el script de §5 antes de llamar
`validate-manifest`/`import-manifest` — no pegar el placeholder directamente en la API.

## 3. Barem manifest QA (versión corta)

```json
{
  "name": "Barem QA versión corta",
  "barem_type": "EXPLORATORY",
  "population_label": "Dataset QA interno — sin validez poblacional",
  "source_reference": "QA interno, no oficial",
  "barem_version": "QA-SHORT-0.1",
  "cutoffs": [
    {"construct_code": "D1", "cut_1": 33, "cut_2": 66, "direction": "LOWER_BETTER"},
    {"construct_code": "D2", "cut_1": 33, "cut_2": 66, "direction": "LOWER_BETTER"},
    {"construct_code": "D3", "cut_1": 33, "cut_2": 66, "direction": "LOWER_BETTER"},
    {"construct_code": "D4", "cut_1": 33, "cut_2": 66, "direction": "LOWER_BETTER"},
    {"construct_code": "D5", "cut_1": 33, "cut_2": 66, "direction": "LOWER_BETTER"},
    {"construct_code": "D6", "cut_1": 33, "cut_2": 66, "direction": "LOWER_BETTER"}
  ]
}
```

`barem_type: "EXPLORATORY"` es intencional — nunca usar `"OFFICIAL"` con cutoffs 33/66
inventados. Esto es justo lo que `BAREM-005` de la auditoría prohíbe si se presenta como
oficial. Con `EXPLORATORY`, `official_equivalence_enabled` debe quedar en `false` y
`classification_status` en `PROVISIONAL` — verificar que así sea (`SCORE-005`, `CLASS-*`).

## 4. Dataset A — 20 sesiones (versión corta), con los casos obligatorios de §26 de la auditoría

Estructura de unidades (`unit_type: CENTRO`):

| Unidad | n sesiones | Propósito del caso |
|---|---:|---|
| Centro A | 5 | Publicable (`PRIV-004`, n=5) |
| Centro B | 4 | Debe suprimirse (`PRIV-003`, n=4) |
| Centro C | 11 | Resto de la muestra, incluye 1 sesión incompleta y 1 intento de código inválido |

Total 20 sesiones válidas + 1 sesión deliberadamente incompleta (no cuenta como válida) + 1
intento de `raw_code` inválido (debe ser rechazado por la API, no debe crear respuesta).

```text
Centro A (n=5): sesiones con D1 mayormente alto (4-5) → riesgo desfavorable esperado en D1
Centro B (n=4): mezcla neutra (raw_code 3 en casi todo) → usado solo para probar supresión,
                no para verificar clasificación
Centro C (n=11): incluye:
  - 5 sesiones con respuestas favorables (raw_code 1-2 en toda la escala)
  - 5 sesiones con respuestas desfavorables (raw_code 4-5 en toda la escala)
  - 1 sesión con raw_code exactamente en el corte esperado (para CLASS-005 / empate:
    diseñar de forma que el % desfavorable de D1 caiga en 49.9% vs 50.0% al variar solo esta
    sesión — usar como caso CLASS-001/CLASS-002)
  - dejar 1 de estas sesiones con solo 20 de los 31 ítems psicosociales respondidos antes de
    `complete` → prueba de completitud (RESP-004) — NO completar la sesión, o completarla y
    verificar que el motor identifique missing explícito, según el comportamiento real de
    `/response-sessions/{id}/complete` (confirmar si exige 100% de obligatorios)
Intento de código inválido: PUT .../responses/{item_id} {"raw_code": "9"} sobre escala LIKERT5
  (válidos 1-5) → debe devolver error de validación, no debe crearse response (CAT-003)
```

## 5. Generador reproducible del manifest + respuestas (versión corta)

```python
# scripts/qa/gen_censopas_short.py
"""Genera el manifest CENSOPAS QA (versión corta) y una matriz de respuestas
para las 20 sesiones del Dataset A. Salidas: censopas_manifest_short.json,
censopas_barem_short.json, censopas_responses_short.csv."""
import json
import random

random.seed(42)

DIMENSIONS = [
    ("D1", "Exigencias psicológicas", 6),
    ("D2", "Conflicto trabajo-familia", 5),
    ("D3", "Control sobre el trabajo", 5),
    ("D4", "Apoyo social y calidad de liderazgo", 5),
    ("D5", "Compensaciones", 5),
    ("D6", "Capital social", 5),
]
SOC_ITEMS = 11

questions = []
constructs = []
scoring_rules = []
risk_map_direct = {"1": 0, "2": 25, "3": 50, "4": 75, "5": 100}

for code, name, n_items in DIMENSIONS:
    items = []
    for k in range(1, n_items + 1):
        q_code = f"{code}-{k:02d}"
        questions.append({
            "code": q_code, "source_code": f"QA-{q_code}",
            "question_text": f"Ítem psicosocial {q_code} (QA placeholder)",
            "question_type": "LIKERT", "is_scored": True,
            "research_role": "ENDOGENOUS", "option_set_code": "LIKERT5",
            "is_required": True,
        })
        items.append({"question_code": q_code, "weight": 1, "item_role": "SCORED", "scoring_direction": "DIRECT"})
        scoring_rules.append({"question_code": q_code, "risk_map": risk_map_direct, "rule_version": "QA-0.1"})
    constructs.append({"code": code, "name": name, "construct_type": "DIMENSION", "items": items})

for k in range(1, SOC_ITEMS + 1):
    questions.append({
        "code": f"SOC-{k:02d}", "source_code": f"QA-SOC-{k:02d}",
        "question_text": f"Dato sociodemográfico {k} (QA placeholder)",
        "question_type": "SINGLE_CHOICE", "is_scored": False, "is_required": False,
    })

manifest = {
    "version_kind": "SHORT",
    "manifest_version": "QA-SHORT-0.1",
    "source_reference": "Dataset QA interno — placeholders, NO oficial",
    "scales": [{
        "code": "LIKERT5", "name": "Escala Likert 5 puntos",
        "options": [
            {"raw_code": str(i), "label": lbl, "numeric_value": i, "sort_order": i}
            for i, lbl in enumerate(["Nunca", "Casi nunca", "A veces", "Casi siempre", "Siempre"], start=1)
        ],
    }],
    "questions": questions,
    "constructs": constructs,
    "scoring_rules": scoring_rules,
}
json.dump(manifest, open("censopas_manifest_short.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

barem = {
    "name": "Barem QA versión corta",
    "barem_type": "EXPLORATORY",
    "population_label": "Dataset QA interno",
    "source_reference": "QA interno, no oficial",
    "barem_version": "QA-SHORT-0.1",
    "cutoffs": [
        {"construct_code": code, "cut_1": 33, "cut_2": 66, "direction": "LOWER_BETTER"}
        for code, _, _ in DIMENSIONS
    ],
}
json.dump(barem, open("censopas_barem_short.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# Matriz de respuestas: 20 sesiones (5 Centro A desfavorable, 4 Centro B neutro,
# 11 Centro C mixto con 1 caso límite de empate)
profiles = (
    [("A", "desfavorable")] * 5
    + [("B", "neutro")] * 4
    + [("C", "favorable")] * 5
    + [("C", "desfavorable")] * 5
    + [("C", "limite")] * 1
)

def sample_code(profile: str) -> str:
    if profile == "favorable":
        return str(random.choice([1, 1, 2]))
    if profile == "desfavorable":
        return str(random.choice([4, 5, 5]))
    if profile == "neutro":
        return "3"
    if profile == "limite":
        return str(random.choice([3, 4]))
    raise ValueError(profile)

rows = []
all_item_codes = [f"{c}-{k:02d}" for c, _, n in DIMENSIONS for k in range(1, n + 1)]
for idx, (unit, profile) in enumerate(profiles, start=1):
    row = {"session": idx, "unit": unit}
    for item_code in all_item_codes:
        row[item_code] = sample_code(profile)
    rows.append(row)

import csv
with open("censopas_responses_short.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["session", "unit", *all_item_codes])
    writer.writeheader()
    writer.writerows(rows)

print("Generado: censopas_manifest_short.json, censopas_barem_short.json, censopas_responses_short.csv")
```

Este script no llama a la API — produce los tres artefactos JSON/CSV. El seeding real (POST
secuencial contra `/import-manifest`, `/import-barem-manifest`, creación de estudio/unidades/
sesiones) depende del entorno (URL, auth) y debe escribirse aparte, siguiendo exactamente la
secuencia de §1.

## 6. Dataset B — versión media (bosquejo, no expandido en detalle)

Mismo mecanismo que Dataset A pero con `version_kind: "MEDIUM"`, `TOTAL=112`,
`PSICOSOCIALES=69`, 6 dimensiones + 20 subdimensiones, y los conteos de participación exigidos
por `TEL-001..TEL-005`:

```text
convocados = 200
recibidos  = 186
válidos    = 180
tasa_valida = 180/200 = 90%
```

Extender `scripts/qa/gen_censopas_short.py` reemplazando `DIMENSIONS` por una lista de 6
dimensiones × subdimensiones (repartiendo 69 ítems puntuables entre 20 subdimensiones, p.ej.
3-4 ítems por subdimensión) y `SOC_ITEMS` a 43 (para llegar a 112 totales). No se expande aquí
ítem por ítem porque sería 112 líneas de placeholder sin valor adicional sobre el patrón ya
mostrado en Dataset A — el generador es mecánicamente idéntico, solo cambia la tabla de
dimensiones/subdimensiones y los conteos objetivo.

Debe incluir además, para cubrir `PRIV-005`/`PRIV-006`/`RES-006`:

```text
al menos un cruce Área × Turno × Contrato con n=3 (bloqueo por cruce, no por variable individual)
al menos un caso de "ataque por totales" (grupo pequeño deducible por resta desde el total)
```

## 7. Casos de prueba que este dataset habilita directamente

| ID auditoría | Cubierto por | Cómo verificar |
|---|---|---|
| INST-001 | Manifest §2 | `validate-manifest` → `expected`/`actual` = 42/31/6 |
| PRIV-003 | Centro B (n=4) | `unit-results` → `suppressed: true`, `suppression_reason: BELOW_MINIMUM_N` |
| PRIV-004 | Centro A (n=5) | `unit-results` → publicable si no hay riesgo de cruce adicional |
| CAT-003 | Intento raw_code="9" | `PUT .../responses/{id}` debe rechazar, no crear response |
| RESP-004 | Sesión incompleta en Centro C | `censopas/results` debe reflejar n_valid menor, no imputar |
| CLASS-001/002/005 | Sesión "límite" en Centro C | Variar esa única sesión y comparar % desfavorable D1 en 49.9% vs 50.0% |
| SCORE-005 | Barem `EXPLORATORY` | `classification_status` debe ser `PROVISIONAL`, `official_equivalence_enabled: false` |
| BAREM-005 | Barem §3 | Confirmar que el frontend nunca etiquete estos cutoffs como oficiales |

## 8. Definition of Done de este dataset

```text
[ ] scripts/qa/gen_censopas_short.py ejecutado, genera manifest/barem/respuestas
[ ] POST .../validate-manifest devuelve valid=true con expected=actual (42/31/6)
[ ] POST .../import-manifest y .../import-barem-manifest devuelven 201
[ ] estudio CENSO abierto, 20 sesiones completadas + 1 incompleta + 1 intento inválido
[ ] POST .../censopas/scoring devuelve status COMPLETED
[ ] GET .../censopas/results: scoring_status=NOT_CONFIGURED u equivalente, official_equivalence_enabled=false
[ ] GET .../censopas/unit-results: Centro B suprimido, Centro A publicable
[ ] los 8 casos de la tabla §7 verificados
[ ] Dataset B (versión media) generado por extensión del mismo script antes de cerrar Fase 3
[ ] cualquier discrepancia registrada en COLMENA_TEST_AUDITORIA_CENSOPAS.md, no silenciada
```
