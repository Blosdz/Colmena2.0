"""Render del bundle de ReportService a un documento Word (.docx).

Consume el mismo `bundle` dict que antes sólo se serializaba a JSON
(`ReportService._build_bundle`): estudio, `analysis_results`, `barem_results`
(`StudyResultsOverview` con la lista de `ConstructBaremResult` — las tablas
de baremación por dimensión, ya con supresión de privacidad aplicada). No
recalcula nada: sólo formatea lo que el bundle ya trae.

Las gráficas se generan con matplotlib en backend "Agg" (sin display) y se
insertan como PNG embebido — no hay renderizado interactivo en el reporte
descargado, sólo imágenes estáticas dentro del Word.
"""

from __future__ import annotations

import io
from datetime import datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (después de matplotlib.use)
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

_MUTED_RGB = RGBColor(0x6B, 0x72, 0x80)


def render_report_docx(bundle: dict) -> bytes:
    document = Document()

    study = bundle.get("study") or {}
    barem = bundle.get("barem_results")
    selected = set(bundle.get("sections") or [])

    def include(*keys: str) -> bool:
        return not selected or bool(selected.intersection(keys))

    if include("portada"):
        _add_cover(
            document,
            study,
            bundle.get("generated_at"),
            bundle.get("report_mode", "PROVISIONAL"),
        )
    if include("trazabilidad", "ficha_tecnica"):
        _add_methodological_status(document, bundle.get("methodological_status"))
    if include("ficha_tecnica"):
        _add_ficha_tecnica(document, study, barem)

    if include(
        "resultados_globales",
        "dimensiones",
        "subdimensiones",
        "unidades_seguras",
    ):
        document.add_heading("Resultados de baremación", level=1)
        results = (barem or {}).get("results") or []
        if results:
            _add_baremacion_table(
                document, results, (barem or {}).get("min_publishable_n")
            )
            _insert_chart(document, _build_bands_chart(results))
            _insert_chart(document, _build_mean_chart(results))
        else:
            document.add_paragraph(
                "Este estudio todavía no tiene resultados de baremación calculados "
                "(corre el scoring del estudio antes de generar el reporte)."
            )

    if include("variables_descriptivas") and bundle.get("analysis_results"):
        _add_analysis_section(document, bundle["analysis_results"])
    if include("hallazgos_premium"):
        _add_premium_section(document, bundle.get("premium_analytics") or {})
    if include("plan_accion"):
        _add_action_plan_section(document, bundle.get("action_plans") or [])
    if include("anexos", "trazabilidad"):
        _add_traceability_appendix(document, bundle.get("traceability") or {})

    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def _add_cover(
    document: Document,
    study: dict,
    generated_at: str | None,
    report_mode: str,
) -> None:
    title = document.add_heading(study.get("name") or "Reporte", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    mode_label = (
        "Reporte oficial CENSOPAS-COPSOQ"
        if report_mode == "OFFICIAL"
        else "Reporte provisional — sin equivalencia oficial"
    )
    subtitle = document.add_paragraph(mode_label)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if subtitle.runs:
        subtitle.runs[0].font.size = Pt(13)
        subtitle.runs[0].font.color.rgb = _MUTED_RGB

    date_label = _format_datetime(generated_at)
    if date_label:
        date_paragraph = document.add_paragraph(f"Generado el {date_label}")
        date_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if date_paragraph.runs:
            date_paragraph.runs[0].font.size = Pt(10)
            date_paragraph.runs[0].font.color.rgb = _MUTED_RGB

    document.add_page_break()


def _add_methodological_status(document: Document, readiness: dict | None) -> None:
    if not readiness:
        return
    document.add_heading("Estado metodológico", level=1)
    scoring_label = "Listo" if readiness.get("ready_for_scoring") else "Bloqueado"
    official_label = (
        "Habilitada"
        if readiness.get("ready_for_official_reporting")
        else "No habilitada"
    )
    document.add_paragraph(
        f"Versión: {readiness.get('version_kind', 'UNKNOWN')}. "
        f"Scoring: {scoring_label}. Equivalencia oficial: {official_label}."
    )
    if readiness.get("errors"):
        document.add_paragraph("Bloqueos: " + ", ".join(readiness["errors"]))
    if readiness.get("warnings"):
        document.add_paragraph("Advertencias: " + ", ".join(readiness["warnings"]))
    document.add_page_break()


def _add_ficha_tecnica(document: Document, study: dict, barem: dict | None) -> None:
    document.add_heading("Ficha técnica", level=1)
    rows = [
        ("Estudio", study.get("name") or "—"),
        ("Tipo de estudio", study.get("study_type") or "—"),
        ("Estado", study.get("status") or "—"),
    ]
    if barem:
        rows.append(("Respuestas completadas", str(barem.get("n_completed", 0))))
        rows.append(("N mínimo publicable", str(barem.get("min_publishable_n", "—"))))
        if barem.get("barem_name"):
            rows.append(("Baremo aplicado", barem["barem_name"]))
        if barem.get("algorithm_version"):
            rows.append(("Versión de algoritmo", barem["algorithm_version"]))

    table = document.add_table(rows=0, cols=2)
    table.style = "Light List Accent 1"
    for label, value in rows:
        cells = table.add_row().cells
        cells[0].text = label
        cells[1].text = value
        for run in cells[0].paragraphs[0].runs:
            run.font.bold = True
    document.add_paragraph()


def _add_baremacion_table(document: Document, results: list[dict], min_publishable_n: int | None) -> None:
    band_labels = [band["label"] for band in results[0].get("bands") or []]
    headers = ["Dimensión", "N válido", "Media", "Mediana", "Prioridad", *band_labels]

    table = document.add_table(rows=1, cols=len(headers))
    table.style = "Light Grid Accent 1"
    header_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        header_cells[i].text = header
        for run in header_cells[i].paragraphs[0].runs:
            run.font.bold = True

    for result in results:
        cells = table.add_row().cells
        code = result.get("construct_code")
        name = result.get("construct_name") or "—"
        cells[0].text = f"{code} · {name}" if code else name

        if result.get("suppressed"):
            hidden = f"Oculto (n<{min_publishable_n})" if min_publishable_n else "Oculto"
            for i in range(1, len(headers)):
                cells[i].text = hidden
            continue

        cells[1].text = str(result.get("n_valid", "—"))
        cells[2].text = _format_number(result.get("mean_score"))
        cells[3].text = _format_number(result.get("median_score"))
        cells[4].text = str(result["priority_rank"]) if result.get("priority_rank") is not None else "—"

        bands_by_label = {band["label"]: band for band in result.get("bands") or []}
        for i, label in enumerate(band_labels):
            band = bands_by_label.get(label)
            cell = cells[5 + i]
            if band and band.get("pct") is not None:
                cell.text = f"{band['pct']:.1f}%"
                if band.get("color_hint"):
                    _shade_cell(cell, band["color_hint"])
            else:
                cell.text = "—"

    document.add_paragraph()


def _add_analysis_section(document: Document, analysis_results: list[dict]) -> None:
    document.add_heading("Resultados de análisis estadístico", level=1)
    headers = ["Código", "Tipo", "N válido", "Valor", "Estadístico", "p", "Tamaño de efecto"]
    table = document.add_table(rows=1, cols=len(headers))
    table.style = "Light Grid Accent 1"
    header_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        header_cells[i].text = header
        for run in header_cells[i].paragraphs[0].runs:
            run.font.bold = True

    # Cap defensivo: un reporte con cientos de result_type sueltos no debería
    # convertirse en un Word de mil filas — la sección de baremación es la
    # tabla protagonista, ésta es un complemento.
    for result in analysis_results[:50]:
        cells = table.add_row().cells
        cells[0].text = result.get("result_code") or "—"
        cells[1].text = result.get("result_type") or "—"
        cells[2].text = str(result["n_valid"]) if result.get("n_valid") is not None else "—"
        cells[3].text = _format_number(result.get("numeric_value"))
        cells[4].text = _format_number(result.get("statistic_value"))
        cells[5].text = _format_number(result.get("p_value"), decimals=4)
        cells[6].text = _format_number(result.get("effect_size"))


def _add_action_plan_section(document: Document, plans: list[dict]) -> None:
    document.add_heading("Plan de acción y seguimiento", level=1)
    if not plans:
        document.add_paragraph("No hay planes de acción registrados para este estudio.")
        return
    for plan in plans:
        document.add_heading(plan.get("name") or "Plan de acción", level=2)
        approval = "Aprobado" if plan.get("approved") else "Pendiente de aprobación"
        document.add_paragraph(f"Estado: {plan.get('status') or '—'}. {approval}.")
        headers = ["Prioridad", "Constructo", "Hallazgo y acción", "Responsable", "Fecha", "Estado"]
        table = document.add_table(rows=1, cols=len(headers))
        table.style = "Light Grid Accent 1"
        for index, header in enumerate(headers):
            table.rows[0].cells[index].text = header
        for item in plan.get("items") or []:
            cells = table.add_row().cells
            cells[0].text = str(item.get("priority") or "—")
            construct = item.get("construct_code") or "—"
            if item.get("construct_name"):
                construct += f" · {item['construct_name']}"
            cells[1].text = construct
            cells[2].text = "\n".join(filter(None, [item.get("finding"), item.get("action_description")])) or "—"
            cells[3].text = item.get("responsible_label") or "—"
            cells[4].text = item.get("due_date") or "—"
            cells[5].text = item.get("status") or "—"
            for kpi in item.get("kpis") or []:
                latest = kpi.get("latest_measurement") or {}
                measured = latest.get("numeric_value")
                if measured is None:
                    measured = latest.get("text_value") or "sin medición"
                document.add_paragraph(
                    f"KPI {kpi.get('code') or '—'}: {kpi.get('name') or '—'} · "
                    f"línea base {_format_number(kpi.get('baseline_value'))} · "
                    f"meta {_format_number(kpi.get('target_value'))} · último valor {measured}."
                )
        document.add_paragraph()


def _add_premium_section(document: Document, premium: dict) -> None:
    document.add_heading("Analítica premium", level=1)
    if premium.get("status") != "AVAILABLE":
        document.add_paragraph("No hay resultados premium publicables para este estudio.")
        return
    document.add_paragraph(
        f"{premium.get('result_count', 0)} resultados publicables; "
        f"{premium.get('significant_result_count', 0)} con p ajustado o p menor a 0.05. "
        f"Métodos: {', '.join(premium.get('methods') or []) or '—'}."
    )
    headers = ["Código", "Método", "N", "Estadístico", "p ajustado", "Efecto", "IC"]
    table = document.add_table(rows=1, cols=len(headers))
    table.style = "Light Grid Accent 1"
    for index, header in enumerate(headers):
        table.rows[0].cells[index].text = header
    for result in (premium.get("results") or [])[:100]:
        cells = table.add_row().cells
        cells[0].text = result.get("result_code") or "—"
        cells[1].text = result.get("result_type") or "—"
        cells[2].text = str(result.get("n_valid") if result.get("n_valid") is not None else "—")
        cells[3].text = _format_number(result.get("statistic_value"))
        adjusted = result.get("adjusted_p_value")
        cells[4].text = _format_number(adjusted if adjusted is not None else result.get("p_value"), 4)
        cells[5].text = " · ".join(filter(None, [_format_number(result.get("effect_size")), result.get("effect_label")]))
        cells[6].text = f"[{_format_number(result.get('ci_lower'))}, {_format_number(result.get('ci_upper'))}]"
    document.add_paragraph("Limitaciones: " + " ".join(premium.get("limitations") or []))


def _add_traceability_appendix(document: Document, traceability: dict) -> None:
    document.add_heading("Anexo de trazabilidad", level=1)
    if not traceability:
        document.add_paragraph("No hay metadatos de trazabilidad disponibles.")
        return
    rows = [
        ("Versión del instrumento", traceability.get("version_kind") or "—"),
        ("Hash del manifiesto", traceability.get("manifest_hash") or "—"),
        ("Linaje", " → ".join(traceability.get("lineage") or [])),
        ("N mínimo publicable", str((traceability.get("privacy") or {}).get("min_publishable_n", "—"))),
        ("Registros individuales incluidos", "No"),
    ]
    barem = traceability.get("barem") or {}
    if barem:
        rows.extend([
            ("Baremo", f"{barem.get('name') or '—'} · {barem.get('version') or '—'}"),
            ("Hash del baremo", barem.get("content_hash") or "—"),
            ("Fuente del baremo", barem.get("source_reference") or "—"),
        ])
    table = document.add_table(rows=0, cols=2)
    table.style = "Light List Accent 1"
    for label, value in rows:
        cells = table.add_row().cells
        cells[0].text = label
        cells[1].text = value
    runs = traceability.get("analysis_runs") or []
    if runs:
        document.add_heading("Ejecuciones analíticas", level=2)
        run_table = document.add_table(rows=1, cols=5)
        run_table.style = "Light Grid Accent 1"
        for index, header in enumerate(["Tipo", "Estado", "Motor", "Algoritmo", "Hash de entrada"]):
            run_table.rows[0].cells[index].text = header
        for run in runs:
            cells = run_table.add_row().cells
            cells[0].text = run.get("analysis_type") or "—"
            cells[1].text = run.get("status") or "—"
            cells[2].text = " ".join(filter(None, [run.get("engine"), run.get("engine_version")])) or "—"
            cells[3].text = run.get("algorithm_version") or "—"
            cells[4].text = run.get("input_hash") or "—"


def _dominant_band(result: dict) -> dict | None:
    bands = [band for band in result.get("bands") or [] if band.get("pct") is not None]
    if not bands:
        return None
    return max(bands, key=lambda band: band["pct"])


def _build_bands_chart(results: list[dict]) -> io.BytesIO | None:
    plot_results = [r for r in results if not r.get("suppressed") and r.get("bands")]
    if not plot_results:
        return None

    band_count = len(plot_results[0]["bands"])
    labels = [r.get("construct_code") or r.get("construct_name") or "" for r in plot_results]
    fig_height = max(2.2, 0.5 * len(plot_results) + 1.3)
    fig, ax = plt.subplots(figsize=(6.3, fig_height), dpi=150)

    y_pos = list(range(len(plot_results)))
    left = [0.0] * len(plot_results)
    for band_index in range(band_count):
        widths, color, band_label = [], "#9CA3AF", ""
        for result in plot_results:
            bands = result.get("bands") or []
            band = bands[band_index] if band_index < len(bands) else None
            widths.append((band.get("pct") or 0) if band else 0)
            if band:
                color = band.get("color_hint") or color
                band_label = band.get("label") or band_label
        ax.barh(y_pos, widths, left=left, color=color, label=band_label, edgecolor="white", height=0.62)
        left = [total + width for total, width in zip(left, widths)]

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("% de encuestados", fontsize=9)
    ax.set_title("Distribución de bandas por dimensión", fontsize=11, fontweight="bold")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=max(band_count, 1), fontsize=8, frameon=False)
    fig.tight_layout()
    return _fig_to_png(fig)


def _build_mean_chart(results: list[dict]) -> io.BytesIO | None:
    plot_results = [r for r in results if r.get("mean_score") is not None]
    if not plot_results:
        return None

    labels = [r.get("construct_code") or r.get("construct_name") or "" for r in plot_results]
    means = [r["mean_score"] for r in plot_results]
    colors = [(_dominant_band(r) or {}).get("color_hint") or "#6B7280" for r in plot_results]

    fig_height = max(2.2, 0.45 * len(plot_results) + 1.2)
    fig, ax = plt.subplots(figsize=(6.3, fig_height), dpi=150)
    y_pos = list(range(len(plot_results)))
    ax.barh(y_pos, means, color=colors, height=0.6)
    for i, value in enumerate(means):
        ax.text(min(value + 2, 96), i, f"{value:.1f}", va="center", fontsize=8)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Puntaje promedio (0-100)", fontsize=9)
    ax.set_title("Puntaje promedio por dimensión, ordenado por prioridad", fontsize=11, fontweight="bold")
    fig.tight_layout()
    return _fig_to_png(fig)


def _fig_to_png(fig) -> io.BytesIO:
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)
    return buffer


def _insert_chart(document: Document, image: io.BytesIO | None) -> None:
    if image is None:
        return
    document.add_picture(image, width=Cm(15))
    document.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER


def _shade_cell(cell, hex_color: str) -> None:
    shading = OxmlElement("w:shd")
    shading.set(qn("w:val"), "clear")
    shading.set(qn("w:color"), "auto")
    shading.set(qn("w:fill"), hex_color.lstrip("#"))
    cell._tc.get_or_add_tcPr().append(shading)


def _format_number(value: float | None, decimals: int = 2) -> str:
    if value is None:
        return "—"
    return f"{value:.{decimals}f}"


def _format_datetime(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return value
