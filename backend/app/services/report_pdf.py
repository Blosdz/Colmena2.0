"""Render premium del expediente CENSOPAS a PDF con ReportLab.

El PDF consume exclusivamente el bundle agregado y protegido de ReportService.
No accede a filas individuales ni recalcula la clasificación oficial.
"""

from __future__ import annotations

import io
import os
from html import escape
from pathlib import Path
from typing import Any

from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

NAVY = colors.HexColor("#12363B")
NAVY_2 = colors.HexColor("#1B4A4F")
TEAL = colors.HexColor("#1CA59F")
GOLD = colors.HexColor("#D8A12E")
INK = colors.HexColor("#18262A")
MUTED = colors.HexColor("#66777C")
SURFACE = colors.HexColor("#F3F7F7")
BORDER = colors.HexColor("#D9E3E3")
GREEN = colors.HexColor("#1D9A73")
AMBER = colors.HexColor("#E3A82E")
RED = colors.HexColor("#D95454")
VIOLET = colors.HexColor("#7869D9")


def _register_fonts() -> tuple[str, str]:
    font_dir = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    regular = font_dir / "segoeui.ttf"
    bold = font_dir / "seguisb.ttf"
    if regular.exists() and bold.exists():
        try:
            pdfmetrics.registerFont(TTFont("ColmenaSans", str(regular)))
            pdfmetrics.registerFont(TTFont("ColmenaSansBold", str(bold)))
            return "ColmenaSans", "ColmenaSansBold"
        except Exception:
            pass
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = _register_fonts()


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ColmenaTitle", parent=base["Title"], fontName=FONT_BOLD,
            fontSize=27, leading=31, textColor=INK, spaceAfter=9, alignment=TA_LEFT,
        ),
        "subtitle": ParagraphStyle(
            "ColmenaSubtitle", parent=base["BodyText"], fontName=FONT,
            fontSize=11, leading=17, textColor=MUTED, spaceAfter=10,
        ),
        "h1": ParagraphStyle(
            "ColmenaH1", parent=base["Heading1"], fontName=FONT_BOLD,
            fontSize=18, leading=22, textColor=NAVY, spaceBefore=5, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "ColmenaH2", parent=base["Heading2"], fontName=FONT_BOLD,
            fontSize=12, leading=15, textColor=NAVY_2, spaceBefore=7, spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "ColmenaBody", parent=base["BodyText"], fontName=FONT,
            fontSize=8.5, leading=12.5, textColor=INK, spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "ColmenaSmall", parent=base["BodyText"], fontName=FONT,
            fontSize=7.2, leading=10, textColor=MUTED,
        ),
        "cell": ParagraphStyle(
            "ColmenaCell", parent=base["BodyText"], fontName=FONT,
            fontSize=6.8, leading=8.6, textColor=INK,
        ),
        "cell_bold": ParagraphStyle(
            "ColmenaCellBold", parent=base["BodyText"], fontName=FONT_BOLD,
            fontSize=6.8, leading=8.6, textColor=INK,
        ),
        "center": ParagraphStyle(
            "ColmenaCenter", parent=base["BodyText"], fontName=FONT,
            fontSize=8, leading=11, textColor=INK, alignment=TA_CENTER,
        ),
        "badge": ParagraphStyle(
            "ColmenaBadge", parent=base["BodyText"], fontName=FONT_BOLD,
            fontSize=7.2, leading=9, textColor=colors.white, alignment=TA_CENTER,
        ),
    }


S = _styles()


def _p(value: Any, style: str = "body") -> Paragraph:
    text = "—" if value is None or value == "" else str(value)
    return Paragraph(escape(text).replace("\n", "<br/>"), S[style])


def _number(value: Any, digits: int = 1) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return "—"


def _table(data, widths, *, header: bool = False, small: bool = False) -> Table:
    table = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("FONTNAME", (0, 0), (-1, -1), FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 6.5 if small else 7.2),
        ("LEADING", (0, 0), (-1, -1), 8.2 if small else 9.2),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("GRID", (0, 0), (-1, -1), 0.35, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [colors.white, SURFACE]),
    ]
    if header:
        commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
        ])
    table.setStyle(TableStyle(commands))
    return table


def _page(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 10 * mm, width, 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, height - 10 * mm, 42 * mm, 1.4 * mm, fill=1, stroke=0)
    canvas.setFont(FONT_BOLD, 7)
    canvas.setFillColor(colors.white)
    canvas.drawString(14 * mm, height - 6.5 * mm, "COLMENA | INTELIGENCIA PSICOSOCIAL")
    canvas.setStrokeColor(BORDER)
    canvas.line(14 * mm, 13 * mm, width - 14 * mm, 13 * mm)
    canvas.setFont(FONT, 6.8)
    canvas.setFillColor(MUTED)
    canvas.drawString(14 * mm, 8.5 * mm, "CENSOPAS-COPSOQ · expediente agregado · privacidad protegida")
    canvas.drawRightString(width - 14 * mm, 8.5 * mm, f"Página {doc.page}")
    canvas.restoreState()


def _section(story: list, number: str, title: str, note: str | None = None) -> None:
    badge = Table([[_p(number, "badge")]], colWidths=[18 * mm], rowHeights=[7 * mm])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), TEAL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0, TEAL),
    ]))
    story.extend([Spacer(1, 3 * mm), badge, Paragraph(escape(title), S["h1"])])
    if note:
        story.append(Paragraph(escape(note), S["subtitle"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=7))


def _cover(story: list, bundle: dict) -> None:
    study = bundle.get("study") or {}
    company = bundle.get("company") or {}
    mode = bundle.get("report_mode", "PROVISIONAL")
    story.extend([Spacer(1, 22 * mm)])
    badge = Table([[_p("EXPEDIENTE TÉCNICO · BORRADOR CONTROLADO", "badge")]], colWidths=[70 * mm], rowHeights=[8 * mm])
    badge.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GOLD), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.extend([
        badge,
        Spacer(1, 7 * mm),
        Paragraph(escape(study.get("name") or "Evaluación de riesgos psicosociales"), S["title"]),
        Paragraph(escape(company.get("legal_name") or company.get("name") or "Empresa evaluada"), S["h1"]),
        Paragraph(
            "Reporte oficial CENSOPAS-COPSOQ"
            if mode == "OFFICIAL"
            else "Reporte provisional — datos sintéticos y sin equivalencia oficial",
            S["subtitle"],
        ),
        Spacer(1, 6 * mm),
    ])
    cards = [
        [_p("RUC", "cell_bold"), _p(company.get("tax_id"), "cell"), _p("Población", "cell_bold"), _p(company.get("worker_count"), "cell")],
        [_p("Actividad", "cell_bold"), _p(company.get("industry"), "cell"), _p("Versión", "cell_bold"), _p((bundle.get("methodological_status") or {}).get("version_kind"), "cell")],
        [_p("Estado", "cell_bold"), _p(study.get("status"), "cell"), _p("Privacidad", "cell_bold"), _p("Sin respuestas individuales · n mínimo protegido", "cell")],
    ]
    story.append(_table(cards, [24 * mm, 55 * mm, 24 * mm, 60 * mm]))
    story.extend([
        Spacer(1, 11 * mm),
        Table(
            [[_p(
                "Documento para revisión del profesional responsable, psicología ocupacional, "
                "seguridad y representante de la empresa. No establece diagnósticos individuales "
                "ni inferencias causales.",
                "body",
            )]],
            colWidths=[163 * mm],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
                ("BOX", (0, 0), (-1, -1), 0.8, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]),
        ),
        Spacer(1, 34 * mm),
        _p(f"Generado: {bundle.get('generated_at', '—')}", "small"),
        PageBreak(),
    ])


def _company(story: list, bundle: dict) -> None:
    company = bundle.get("company") or {}
    _section(story, "01", "Identificación, alcance y límites de control")
    locations = company.get("locations") or []
    location_names = ", ".join(item.get("name", "") for item in locations if isinstance(item, dict))
    rows = [
        [_p("Razón social", "cell_bold"), _p(company.get("legal_name") or company.get("name"), "cell"), _p("RUC", "cell_bold"), _p(company.get("tax_id"), "cell")],
        [_p("Actividad / CIIU", "cell_bold"), _p(f"{company.get('industry') or '—'} · {company.get('ciiu_code') or '—'}", "cell"), _p("Dotación", "cell_bold"), _p(company.get("worker_count"), "cell")],
        [_p("Domicilio", "cell_bold"), _p(company.get("fiscal_address"), "cell"), _p("Responsable", "cell_bold"), _p(company.get("study_lead_name"), "cell")],
        [_p("Sedes", "cell_bold"), _p(location_names or "—", "cell"), _p("Representante", "cell_bold"), _p(company.get("representative_name"), "cell")],
    ]
    story.append(_table(rows, [27 * mm, 58 * mm, 24 * mm, 54 * mm]))
    story.append(Paragraph("Semáforo de decisión", S["h2"]))
    thresholds = bundle.get("thresholds") or {}
    controls = [
        ("Cobertura objetivo", thresholds.get("coverage_target", 85), GREEN, "Meta"),
        ("Cobertura crítica", thresholds.get("coverage_critical", 65), RED, "Alerta"),
        ("Completitud objetivo", thresholds.get("completion_target", 90), TEAL, "Meta"),
        ("Exposición en vigilancia", thresholds.get("risk_warning", 35), AMBER, "Vigilancia"),
        ("Exposición crítica", thresholds.get("risk_critical", 50), RED, "Crítico"),
    ]
    data = [[_p("Indicador", "cell_bold"), _p("Límite", "cell_bold"), _p("Estado", "cell_bold")]]
    data += [[_p(label, "cell"), _p(f"{value}%", "cell_bold"), _p(status, "cell_bold")] for label, value, _, status in controls]
    table = _table(data, [83 * mm, 35 * mm, 45 * mm], header=True)
    commands = []
    for row, (_, _, color, _) in enumerate(controls, start=1):
        commands.extend([("BACKGROUND", (2, row), (2, row), color), ("TEXTCOLOR", (2, row), (2, row), colors.white)])
    table.setStyle(TableStyle(commands))
    story.extend([table, _p("Cada estado incluye etiqueta y valor; el color no es el único canal de interpretación.", "small")])


def _method(story: list, bundle: dict) -> None:
    readiness = bundle.get("methodological_status") or {}
    _section(story, "02", "Metodología, privacidad y control de calidad")
    expected, actual = readiness.get("expected") or {}, readiness.get("actual") or {}
    data = [[_p("Componente", "cell_bold"), _p("Esperado", "cell_bold"), _p("Actual", "cell_bold"), _p("Estado", "cell_bold")]]
    for key, label in [
        ("questions", "Preguntas"), ("scored", "Ítems puntuables"),
        ("dimensions", "Dimensiones"), ("subdimensions", "Subdimensiones"),
    ]:
        ok = expected.get(key) == actual.get(key)
        data.append([_p(label, "cell"), _p(expected.get(key), "cell"), _p(actual.get(key), "cell"), _p("Conforme" if ok else "Revisar", "cell_bold")])
    story.append(_table(data, [70 * mm, 28 * mm, 28 * mm, 37 * mm], header=True))
    story.extend([
        Paragraph("Criterios de publicación", S["h2"]),
        _p("Se excluyen sesiones inválidas del denominador analítico. Los grupos con n menor al mínimo publicable no se muestran. No se incorporan filas de respuesta ni identificadores personales."),
        _p("Equivalencia oficial: no habilitada para este demo. La lectura es exploratoria y requiere revisión profesional.", "small"),
    ])


def _band_color(label: str | None) -> colors.Color:
    value = (label or "").upper()
    if "ALTO" in value or "DESFAVOR" in value or "CRIT" in value:
        return RED
    if "MEDIO" in value or "INTER" in value:
        return AMBER
    return GREEN


def _risk_chart(results: list[dict], thresholds: dict | None = None) -> Drawing:
    rows = [item for item in results if not item.get("suppressed")][:10]
    height = max(90, 24 + len(rows) * 20)
    drawing = Drawing(470, height)
    bar_x, bar_width = 125, 315
    thresholds = thresholds or {}
    warning = float(thresholds.get("risk_warning", 35))
    critical = float(thresholds.get("risk_critical", 50))
    for index, item in enumerate(rows):
        y = height - 28 - index * 20
        label = item.get("construct_code") or item.get("construct_name") or ""
        drawing.add(String(0, y + 3, str(label)[:22], fontName=FONT_BOLD, fontSize=7, fillColor=INK))
        left = bar_x
        bands = item.get("bands") or []
        if bands:
            for band in bands:
                pct = float(band.get("pct") or 0)
                width = bar_width * pct / 100
                drawing.add(Rect(left, y, width, 10, fillColor=_band_color(band.get("label")), strokeColor=colors.white, strokeWidth=.3))
                left += width
        else:
            value = float(item.get("unfavorable_pct") or item.get("mean_score") or 0)
            color = GREEN if value < warning else AMBER if value < critical else RED
            drawing.add(Rect(left, y, bar_width * min(value, 100) / 100, 10, fillColor=color, strokeColor=None))
        drawing.add(Rect(bar_x, y, bar_width, 10, fillColor=None, strokeColor=BORDER, strokeWidth=.5))
    for value, color, label in ((warning, AMBER, "V"), (critical, RED, "C")):
        x = bar_x + bar_width * max(0, min(value, 100)) / 100
        drawing.add(Line(x, 7, x, height - 12, strokeColor=color, strokeWidth=.8, strokeDashArray=[3, 2]))
        drawing.add(String(x - 3, 0, label, fontName=FONT_BOLD, fontSize=6, fillColor=color))
    drawing.add(String(bar_x, 2, "0%", fontName=FONT, fontSize=6, fillColor=MUTED))
    drawing.add(String(bar_x + bar_width - 12, 2, "100%", fontName=FONT, fontSize=6, fillColor=MUTED))
    return drawing


def _results(story: list, bundle: dict) -> None:
    barem = bundle.get("barem_results") or {}
    results = barem.get("results") or bundle.get("censopas_results") or []
    _section(story, "03", "Resultados globales, dimensiones y subdimensiones", "Lectura colectiva con denominadores explícitos y supresión automática.")
    thresholds = bundle.get("thresholds") or {}
    story.append(_risk_chart(results, thresholds))
    data = [[_p("Dimensión / subdimensión", "cell_bold"), _p("N válido", "cell_bold"), _p("Media", "cell_bold"), _p("Mediana", "cell_bold"), _p("Prioridad", "cell_bold"), _p("Clasificación", "cell_bold")]]
    for item in results[:28]:
        if item.get("suppressed"):
            values = [_p(item.get("construct_name") or item.get("construct_code"), "cell"), _p("Oculto n<5", "cell_bold"), _p("—", "cell"), _p("—", "cell"), _p("—", "cell"), _p("Protegido", "cell_bold")]
        else:
            values = [
                _p(f"{item.get('construct_code') or ''} · {item.get('construct_name') or ''}", "cell"),
                _p(item.get("n_valid"), "cell"), _p(_number(item.get("mean_score")), "cell"),
                _p(_number(item.get("median_score")), "cell"), _p(item.get("priority_rank"), "cell"),
                _p(item.get("collective_classification") or ((max(item.get("bands") or [{}], key=lambda x: x.get("pct") or 0)).get("label") if item.get("bands") else "—"), "cell_bold"),
            ]
        data.append(values)
    story.append(_table(data, [68 * mm, 18 * mm, 19 * mm, 19 * mm, 17 * mm, 32 * mm], header=True, small=True))

    priorities = sorted(
        (item for item in results if not item.get("suppressed")),
        key=lambda item: item.get("priority_rank") or 999,
    )[:5]
    if priorities:
        story.append(Paragraph("Lectura ejecutiva y decisiones", S["h2"]))
        executive = [[_p("Prioridad", "cell_bold"), _p("Señal agregada", "cell_bold"), _p("Decisión sugerida", "cell_bold")]]
        warning = float(thresholds.get("risk_warning", 35))
        critical = float(thresholds.get("risk_critical", 50))
        for item in priorities:
            score = float(item.get("unfavorable_pct") or item.get("mean_score") or 0)
            status = "Crítico" if score >= critical else "Vigilancia" if score >= warning else "Dentro de meta"
            action = "Intervención prioritaria y seguimiento" if score >= critical else "Profundizar por unidad segura" if score >= warning else "Mantener controles y monitoreo"
            executive.append([
                _p(f"{item.get('priority_rank') or '—'} · {item.get('construct_code') or item.get('construct_name') or '—'}", "cell"),
                _p(f"{status} · {_number(score)}%", "cell_bold"),
                _p(action, "cell"),
            ])
        table = _table(executive, [42 * mm, 47 * mm, 74 * mm], header=True, small=True)
        for row, item in enumerate(priorities, start=1):
            score = float(item.get("unfavorable_pct") or item.get("mean_score") or 0)
            color = RED if score >= critical else AMBER if score >= warning else GREEN
            table.setStyle(TableStyle([("TEXTCOLOR", (1, row), (1, row), color)]))
        story.extend([
            table,
            _p("V = vigilancia; C = crítico. Los límites son parámetros internos del demo y no sustituyen el baremo oficial ni la validación profesional.", "small"),
        ])

def _reliability_chart(dimensions: list[dict]) -> Drawing:
    rows = dimensions[:8]
    height = max(100, 35 + len(rows) * 23)
    drawing = Drawing(470, height)
    x0, width = 130, 280
    for index, item in enumerate(rows):
        y = height - 30 - index * 23
        drawing.add(String(0, y + 4, str(item.get("code") or item.get("name") or "")[:24], fontName=FONT_BOLD, fontSize=7, fillColor=INK))
        drawing.add(Rect(x0, y + 7, width * max(0, min(float(item.get("alpha") or 0), 1)), 6, fillColor=TEAL, strokeColor=None))
        drawing.add(Rect(x0, y - 1, width * max(0, min(float(item.get("omega") or 0), 1)), 6, fillColor=VIOLET, strokeColor=None))
    for value, color, label in ((.7, AMBER, ".70"), (.8, GREEN, ".80")):
        x = x0 + width * value
        drawing.add(Line(x, 8, x, height - 12, strokeColor=color, strokeWidth=1, strokeDashArray=[3, 2]))
        drawing.add(String(x - 6, 0, label, fontName=FONT_BOLD, fontSize=6, fillColor=color))
    drawing.add(String(420, height - 20, "α", fontName=FONT_BOLD, fontSize=8, fillColor=TEAL))
    drawing.add(String(440, height - 20, "ω", fontName=FONT_BOLD, fontSize=8, fillColor=VIOLET))
    return drawing


def _intelligence(story: list, bundle: dict) -> None:
    intelligence = bundle.get("intelligence") or {}
    _section(story, "04", "Analítica avanzada, robustez y patrones")
    if not intelligence:
        story.append(_p("No hay una corrida de scoring completa para construir esta capa."))
        return
    quality, decision = intelligence.get("quality") or {}, intelligence.get("decision") or {}
    cards = [
        [_p("Muestra", "cell_bold"), _p(intelligence.get("n"), "cell"), _p("No normales", "cell_bold"), _p(quality.get("non_normal_dimensions"), "cell")],
        [_p("Atípicos", "cell_bold"), _p(f"{quality.get('outlier_sessions', 0)} ({quality.get('outlier_pct', 0)}%)", "cell"), _p("Sensibilidad máx.", "cell_bold"), _p(f"{quality.get('sensitivity_max_delta', '—')} pts", "cell")],
    ]
    story.extend([_table(cards, [31 * mm, 48 * mm, 36 * mm, 48 * mm]), Paragraph("Confiabilidad por dimensión", S["h2"]), _reliability_chart(intelligence.get("dimensions") or [])])
    dims = intelligence.get("dimensions") or []
    data = [[_p("Dimensión", "cell_bold"), _p("N", "cell_bold"), _p("α", "cell_bold"), _p("ω", "cell_bold"), _p("Normalidad p", "cell_bold"), _p("Atípicos", "cell_bold"), _p("Δ sensibilidad", "cell_bold")]]
    for item in dims:
        data.append([_p(f"{item.get('code')} · {item.get('name')}", "cell"), _p(item.get("n"), "cell"), _p(_number(item.get("alpha"), 3), "cell"), _p(_number(item.get("omega"), 3), "cell"), _p(f"{item.get('normality_status')} · {_number(item.get('normality_p'), 4)}", "cell"), _p(item.get("outlier_count"), "cell"), _p(_number(item.get("sensitivity_delta"), 2), "cell")])
    story.append(_table(data, [64 * mm, 14 * mm, 15 * mm, 15 * mm, 29 * mm, 17 * mm, 25 * mm], header=True, small=True))
    story.extend([Paragraph("Decisión automática de pruebas", S["h2"]), _p(f"{decision.get('normality_summary', '')} Comparaciones: {decision.get('recommended_comparison', '—')}. Correlaciones: {decision.get('recommended_correlation', '—')}. {decision.get('outlier_policy', '')}")])
    correlations = [item for item in intelligence.get("correlations") or [] if item.get("significant")][:12]
    if correlations:
        data = [[_p("X", "cell_bold"), _p("Y", "cell_bold"), _p("N", "cell_bold"), _p("ρ", "cell_bold"), _p("q", "cell_bold"), _p("Magnitud", "cell_bold")]]
        for item in correlations:
            data.append([_p(item.get("x_name"), "cell"), _p(item.get("y_name"), "cell"), _p(item.get("n"), "cell"), _p(_number(item.get("rho"), 3), "cell"), _p(_number(item.get("adjusted_p_value"), 4), "cell"), _p(item.get("magnitude"), "cell")])
        story.extend([Paragraph("Correlaciones significativas con ajuste FDR", S["h2"]), _table(data, [48 * mm, 48 * mm, 15 * mm, 16 * mm, 18 * mm, 25 * mm], header=True, small=True)])
    clustering = intelligence.get("clustering") or {}
    if clustering.get("status") == "AVAILABLE":
        data = [[_p("Perfil agregado", "cell_bold"), _p("N", "cell_bold"), _p("Índice", "cell_bold"), _p("Uso", "cell_bold")]]
        for item in clustering.get("profiles") or []:
            data.append([_p(item.get("label"), "cell"), _p(item.get("n"), "cell"), _p(_number(item.get("risk_index")), "cell"), _p("Priorización colectiva; nunca individual", "cell")])
        story.extend([Paragraph(f"Clústeres exploratorios · K={clustering.get('k')} · silhouette={_number(clustering.get('silhouette'), 3)}", S["h2"]), _table(data, [55 * mm, 20 * mm, 25 * mm, 63 * mm], header=True)])
    if intelligence.get("limitations"):
        story.append(Paragraph("Limitaciones", S["h2"]))
        for item in intelligence["limitations"]:
            story.append(Paragraph("• " + escape(str(item)), S["small"]))


def _action_for(name: str) -> str:
    value = (name or "").lower()
    if "lider" in value or "apoyo" in value:
        return "Fortalecer liderazgo, retroalimentación y soporte de supervisión."
    if "ritmo" in value or "exig" in value:
        return "Revisar dotación, carga, pausas y secuencia operativa con participación."
    if "conflicto" in value or "doble" in value:
        return "Rediseñar reglas de desconexión, turnos y conciliación trabajo-familia."
    if "inseguridad" in value or "estima" in value:
        return "Mejorar previsibilidad, reconocimiento y comunicación de cambios."
    return "Diseñar una intervención organizacional específica y medible."


def _actions(story: list, bundle: dict) -> None:
    _section(story, "05", "Plan preventivo y Balanced Scorecard", "Propuesta automática pendiente de validación, presupuesto, responsables y aprobación.")
    plans = bundle.get("action_plans") or []
    rows = []
    if plans:
        for plan in plans:
            for item in plan.get("items") or []:
                rows.append([item.get("construct_name") or item.get("title"), item.get("action_description"), item.get("responsible_label"), item.get("due_date"), item.get("status")])
    else:
        results = (bundle.get("barem_results") or {}).get("results") or bundle.get("censopas_results") or []
        ranked = [item for item in results if not item.get("suppressed")][:6]
        for item in ranked:
            name = item.get("construct_name") or item.get("construct_code") or "Riesgo prioritario"
            rows.append([name, _action_for(name), "Gerencia + SST", "90 días", "Pendiente"])
    data = [[_p("Prioridad", "cell_bold"), _p("Medida organizacional", "cell_bold"), _p("Responsable", "cell_bold"), _p("Plazo", "cell_bold"), _p("Estado", "cell_bold")]]
    for row in rows:
        data.append([_p(row[0], "cell"), _p(row[1], "cell"), _p(row[2], "cell"), _p(row[3], "cell"), _p(row[4], "cell_bold")])
    story.append(_table(data, [42 * mm, 70 * mm, 26 * mm, 18 * mm, 22 * mm], header=True, small=True))
    bsc = [
        [_p("Perspectiva", "cell_bold"), _p("Objetivo", "cell_bold"), _p("KPI", "cell_bold"), _p("Meta", "cell_bold"), _p("Frecuencia", "cell_bold")],
        [_p("Personas", "cell"), _p("Reducir exposición crítica", "cell"), _p("% desfavorable", "cell"), _p("−10 pp", "cell_bold"), _p("Trimestral", "cell")],
        [_p("Procesos", "cell"), _p("Cerrar medidas priorizadas", "cell"), _p("% acciones a tiempo", "cell"), _p("≥ 90%", "cell_bold"), _p("Mensual", "cell")],
        [_p("Liderazgo", "cell"), _p("Mejorar soporte", "cell"), _p("Índice de liderazgo", "cell"), _p("+8 pts", "cell_bold"), _p("Trimestral", "cell")],
        [_p("Gobernanza", "cell"), _p("Sostener seguimiento", "cell"), _p("% evidencias auditables", "cell"), _p("100%", "cell_bold"), _p("Mensual", "cell")],
    ]
    story.extend([Paragraph("Tablero de seguimiento", S["h2"]), _table(bsc, [28 * mm, 52 * mm, 42 * mm, 22 * mm, 27 * mm], header=True)])


def _trace(story: list, bundle: dict) -> None:
    trace = bundle.get("traceability") or {}
    _section(story, "06", "Trazabilidad, anexos y limitaciones")
    rows = [
        [_p("Versión del instrumento", "cell_bold"), _p(trace.get("version_kind"), "cell")],
        [_p("Hash del manifiesto", "cell_bold"), _p(trace.get("manifest_hash"), "cell")],
        [_p("Linaje", "cell_bold"), _p(" → ".join(trace.get("lineage") or []), "cell")],
        [_p("N mínimo publicable", "cell_bold"), _p((trace.get("privacy") or {}).get("min_publishable_n"), "cell")],
        [_p("Registros individuales", "cell_bold"), _p("No incluidos", "cell")],
    ]
    story.append(_table(rows, [52 * mm, 111 * mm]))
    story.extend([
        Paragraph("Declaración técnica", S["h2"]),
        _p("El análisis describe patrones colectivos transversales. Las asociaciones no implican causalidad; los clústeres no identifican personas; los outliers no se eliminan automáticamente; la equivalencia oficial permanece bloqueada hasta cargar el manifiesto y baremo autorizados."),
    ])


def _signatures(story: list, bundle: dict) -> None:
    company = bundle.get("company") or {}
    _section(story, "07", "Firmas y conformidad")
    signatories = list(company.get("signatories") or [])[:4]
    defaults = ["Profesional responsable", "Representante de la empresa", "Ingeniero/a de seguridad", "Psicólogo/a ocupacional"]
    while len(signatories) < 4:
        signatories.append({})
    cells = []
    for index, item in enumerate(signatories):
        role = item.get("role") or defaults[index]
        name = item.get("full_name") or "Nombre pendiente"
        credential = item.get("professional_id") or "Registro profesional pendiente"
        cells.append([
            Spacer(1, 20 * mm),
            HRFlowable(width="75%", thickness=.7, color=MUTED),
            _p(name, "center"), _p(role, "center"), _p(credential, "center"),
            _p("Firma y fecha", "center"),
        ])
    grid = [[cells[0], cells[1]], [cells[2], cells[3]]]
    table = Table(grid, colWidths=[81 * mm, 81 * mm], rowHeights=[55 * mm, 55 * mm])
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), .5, BORDER), ("INNERGRID", (0, 0), (-1, -1), .5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("BACKGROUND", (0, 0), (-1, -1), colors.white),
    ]))
    story.append(table)


def render_report_pdf(bundle: dict) -> bytes:
    output = io.BytesIO()
    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=14 * mm,
        leftMargin=14 * mm,
        topMargin=17 * mm,
        bottomMargin=17 * mm,
        title=(bundle.get("study") or {}).get("name") or "Expediente CENSOPAS",
        author="Colmena",
    )
    selected = set(bundle.get("sections") or [])

    def include(*keys: str) -> bool:
        return not selected or bool(selected.intersection(keys))

    story: list = []

    def new_page() -> None:
        if story and not isinstance(story[-1], PageBreak):
            story.append(PageBreak())

    if include("portada"):
        _cover(story, bundle)
    if include("ficha_tecnica", "participacion_privacidad"):
        _company(story, bundle)
        _method(story, bundle)
    if include("resultados_globales", "dimensiones", "subdimensiones", "unidades_seguras"):
        new_page()
        _results(story, bundle)
    if include("hallazgos_premium", "variables_descriptivas"):
        new_page()
        _intelligence(story, bundle)
    if include("plan_accion"):
        new_page()
        _actions(story, bundle)
    if include("anexos", "trazabilidad"):
        new_page()
        _trace(story, bundle)
    if include("portada", "anexos", "trazabilidad"):
        new_page()
        _signatures(story, bundle)
    document.build(story, onFirstPage=_page, onLaterPages=_page)
    return output.getvalue()

