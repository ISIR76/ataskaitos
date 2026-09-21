#!/usr/bin/env python
"""Generate PDF report from agent evaluation JSON.

Uses the agent's output schemas to properly parse and format evaluation results.

Usage:
    python scripts/analysis/generate_pdf_report.py <evaluation.json> [output.pdf]
    python scripts/analysis/generate_pdf_report.py docs/out/reports/agent_evaluations/agent_evaluation_latest.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfgen_canvas
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import Flowable

from ataskaitos.agent_from_human import MTEPVertinimas


class VerticalText(Flowable):
    """Flowable for rendering vertical text in table cells."""

    def __init__(self, text: str, font_name: str = "Helvetica-Bold", font_size: int = 8):
        Flowable.__init__(self)
        self.text = text
        self.font_name = font_name
        self.font_size = font_size

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.rotate(90)
        canvas.setFont(self.font_name, self.font_size)
        canvas.drawString(0, -self.font_size, self.text)
        canvas.restoreState()

    def wrap(self, availWidth, availHeight):
        # Width becomes the text height (vertical), height becomes font size (horizontal)
        text_width = pdfgen_canvas.Canvas('').stringWidth(self.text, self.font_name, self.font_size)
        return (self.font_size + 2, text_width + 4)


def register_fonts():
    """Register fonts that support Lithuanian characters."""
    try:
        # Try to register DejaVu fonts (common on Linux)
        pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/TTF/DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Oblique', '/usr/share/fonts/TTF/DejaVuSans-Oblique.ttf'))
        print("✓ Registered DejaVu fonts for Lithuanian character support")
        return 'DejaVuSans', 'DejaVuSans-Bold', 'DejaVuSans-Oblique'
    except Exception as e:
        print(f"Warning: Could not register DejaVu fonts ({e}), falling back to Helvetica")
        # Fall back to Helvetica (limited Lithuanian support)
        return 'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique'


def load_evaluation(json_path: Path) -> dict[str, Any]:
    """Load evaluation JSON and extract results."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Handle batch evaluation format
    if "results" in data:
        return data
    # Handle single evaluation format
    return {"results": [data]}


def parse_mtep_evaluation(result: dict[str, Any]) -> tuple[str, MTEPVertinimas]:
    """Parse a single MTEP evaluation result using the schema."""
    document_name = result.get("document", "Unknown")
    evaluation_data = result.get("evaluation", {})

    # Parse using Pydantic schema for validation
    evaluation = MTEPVertinimas.model_validate(evaluation_data)

    return document_name, evaluation


def create_score_color(score: float) -> str:
    """Get color hex based on score value."""
    if score >= 0.70:
        return "#27ae60"  # green
    elif score >= 0.50:
        return "#f39c12"  # orange
    elif score >= 0.30:
        return "#e67e22"  # darker orange
    else:
        return "#e74c3c"  # red


def create_pdf_report(json_path: Path, output_path: Path | None = None):
    """Generate PDF report from evaluation JSON."""
    # Register fonts
    font_regular, font_bold, _font_italic = register_fonts()

    # Load evaluation data
    data = load_evaluation(json_path)
    all_results = data.get("results", [])

    # Filter out results with errors or null evaluations
    results = [r for r in all_results if r.get("evaluation") is not None and r.get("error") is None]

    skipped_count = len(all_results) - len(results)
    if skipped_count > 0:
        print(f"⚠ Skipped {skipped_count} result(s) with errors or missing evaluations")
        for r in all_results:
            if r.get("evaluation") is None or r.get("error") is not None:
                file_name = Path(r.get("file", "Unknown")).name
                model_name = r.get("model", "N/A")
                error_msg = r.get("error", "Missing evaluation")[:80]
                print(f"  - {file_name} ({model_name}): {error_msg}")

    if not results:
        print("No valid evaluation results found in JSON")
        sys.exit(1)

    # Determine output path
    if output_path is None:
        output_path = json_path.parent / f"{json_path.stem}_report.pdf"

    # Create PDF
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=1 * inch,
        bottomMargin=0.75 * inch,
    )

    # Styles with Unicode font support
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontName=font_bold,
        fontSize=18,
        textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=12,
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontName=font_bold,
        fontSize=14,
        textColor=colors.HexColor("#2c3e50"),
        spaceAfter=10,
        spaceBefore=10,
    )

    subheading_style = ParagraphStyle(
        "CustomSubHeading",
        parent=styles["Heading3"],
        fontName=font_bold,
        fontSize=11,
        textColor=colors.HexColor("#34495e"),
        spaceAfter=4,
        spaceBefore=8,
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontName=font_regular,
        fontSize=10,
        leading=14,
        spaceAfter=8,
    )

    reason_style = ParagraphStyle(
        "ReasonText",
        parent=styles["BodyText"],
        fontName=font_regular,
        fontSize=9,
        leading=12,
        leftIndent=15,
        spaceAfter=10,
        textColor=colors.HexColor("#555555"),
    )

    # Build document content
    story = []

    # Title page
    story.append(Paragraph("MTEP Vertinimo Ataskaita", title_style))
    story.append(
        Paragraph(
            f"Sugeneruota: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            body_style
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    # Metadata - show model prominently
    # Extract unique models from results
    models = list({result.get("model", "N/A") for result in results})
    model_display = models[0] if len(models) == 1 else ", ".join(models)

    # Model name in a highlighted box
    story.append(Paragraph("Naudotas modelis", heading_style))
    model_para = Paragraph(
        f'<font size="12" color="#2c3e50"><b>{model_display}</b></font>',
        body_style
    )
    model_table = [[model_para]]
    t = Table(model_table, colWidths=[6.5 * inch])
    t.setStyle(
        TableStyle([
            ("BOX", (0, 0), (-1, -1), 2, colors.HexColor("#3498db")),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ecf0f1")),
            ("PADDING", (0, 0), (-1, -1), 12),
        ])
    )
    story.append(t)
    story.append(Spacer(1, 0.15 * inch))

    # Other metadata
    story.append(Paragraph(f"Dokumentų skaičius: {len(results)}", body_style))
    agent_name = data.get("agent", "mtep_agent")
    story.append(Paragraph(f"Agentas: {agent_name}", body_style))
    timestamp = data.get("timestamp", "N/A")
    story.append(Paragraph(f"Vertinimo laikas: {timestamp}", body_style))
    story.append(Spacer(1, 0.3 * inch))

    # Model comparison table
    story.append(PageBreak())
    story.append(Paragraph("Modelių palyginimas", title_style))
    story.append(Spacer(1, 0.1 * inch))

    # Group results by document
    docs_by_file = {}
    for result in results:
        file_path = result.get("file", "")
        file_name = Path(file_path).name
        if file_name not in docs_by_file:
            docs_by_file[file_name] = {
                "file_path": file_path,
                "y_true": 1 if "/ok/" in file_path.lower() else 0,
                "models": {}
            }
        model_name = result.get("model", "N/A")
        evaluation_data = result.get("evaluation", {})
        score = float(evaluation_data.get("score", 0.0)) if evaluation_data else 0.0
        docs_by_file[file_name]["models"][model_name] = score

    # Build comparison table
    # Header row with vertical text for model names
    header_row = ["Dokumentas", "y_true"] + [VerticalText(model, font_bold, 8) for model in sorted(models)]

    # Data rows
    comparison_data = [header_row]
    for file_name in sorted(docs_by_file.keys()):
        doc_info = docs_by_file[file_name]
        row = [file_name, str(doc_info["y_true"])]
        for model in sorted(models):
            score = doc_info["models"].get(model, None)
            row.append(f"{score:.2f}" if score is not None else "-")
        comparison_data.append(row)

    # Calculate column widths dynamically - model columns can be narrower with vertical text
    available_width = 6.5 * inch
    doc_col_width = 1.5 * inch
    ytrue_col_width = 0.4 * inch
    model_col_width = 0.4 * inch  # Fixed width for vertical text columns
    total_model_width = model_col_width * len(models)

    # If models don't fit, adjust
    if doc_col_width + ytrue_col_width + total_model_width > available_width:
        model_col_width = (available_width - doc_col_width - ytrue_col_width) / len(models)

    col_widths = [doc_col_width, ytrue_col_width] + [model_col_width] * len(models)

    t = Table(comparison_data, colWidths=col_widths)
    t.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (1, 0), font_bold),  # Dokumentas and y_true headers
            ("FONTNAME", (0, 1), (-1, -1), font_regular),  # Data rows
            ("FONTSIZE", (0, 0), (1, 0), 9),  # Doc/ytrue headers
            ("FONTSIZE", (0, 1), (-1, -1), 8),  # Data rows
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center all
            ("ALIGN", (0, 0), (0, -1), "LEFT"),  # Left align document names
            ("PADDING", (0, 0), (-1, -1), 3),  # Minimal padding
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),  # Header background
            ("VALIGN", (0, 0), (-1, 0), "BOTTOM"),  # Bottom align headers (for vertical text)
            ("VALIGN", (0, 1), (-1, -1), "MIDDLE"),  # Middle align data
        ])
    )
    story.append(t)
    story.append(Spacer(1, 0.2 * inch))

    # Process each evaluation
    for idx, result in enumerate(results):
        if idx > 0:
            story.append(PageBreak())

        evaluation = parse_mtep_evaluation(result)[1]
        file_path = result.get("file", "Unknown")
        file_name = Path(file_path).name
        model_name = result.get("model", "N/A")

        # Document header - use filename
        story.append(Paragraph(file_name, title_style))
        story.append(Spacer(1, 0.1 * inch))

        # Model and score on same line
        final_score = float(evaluation.score) if evaluation.score else 0.0
        story.append(Paragraph(f"<b>Modelis:</b> {model_name} | <b>Balas:</b> {final_score:.2f}", body_style))
        story.append(Spacer(1, 0.2 * inch))

        # Initial analysis
        story.append(Paragraph("Pradinis vertinimas", heading_style))
        story.append(Paragraph(evaluation.initial_analysis, body_style))
        story.append(Spacer(1, 0.15 * inch))

        # 5 Core criteria - scores only in table, reasons as text
        story.append(Paragraph("1. Pagrindiniai kriterijai (5)", heading_style))

        core_scores = [
            ["Naujumas", f"{float(evaluation.naujumas.score):.2f}"],
            ["Kūrybiškumas", f"{float(evaluation.kurybiskumas.score):.2f}"],
            ["Neapibrėžtumas", f"{float(evaluation.neapibreztumas.score):.2f}"],
            ["Sistemingumas", f"{float(evaluation.sistemingumas.score):.2f}"],
            ["Perduodamumas", f"{float(evaluation.perduodamumas.score):.2f}"],
        ]

        t = Table(core_scores, colWidths=[4.5 * inch, 2 * inch])
        t.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (0, -1), font_bold),
                ("FONTNAME", (1, 0), (1, -1), font_regular),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("PADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )
        story.append(t)
        story.append(Spacer(1, 0.1 * inch))

        # Reasons as paragraphs
        criteria_data = [
            ("Naujumas", evaluation.naujumas.reason),
            ("Kūrybiškumas", evaluation.kurybiskumas.reason),
            ("Neapibrėžtumas", evaluation.neapibreztumas.reason),
            ("Sistemingumas", evaluation.sistemingumas.reason),
            ("Perduodamumas", evaluation.perduodamumas.reason),
        ]

        for name, reason in criteria_data:
            story.append(Paragraph(f"<b>{name}:</b>", subheading_style))
            story.append(Paragraph(reason, reason_style))

        story.append(Spacer(1, 0.15 * inch))

        # Document structure - scores table + reasons
        story.append(Paragraph("2. Dokumento struktūra", heading_style))

        structure_scores = [
            ["Įvadas", f"{float(evaluation.ivadas.score):.2f}"],
            ["Problemos formulavimas", f"{float(evaluation.problemos_formulavimas.score):.2f}"],
            ["Uždavinio apibrėžimas", f"{float(evaluation.uzdavinio_apibrezimas.score):.2f}"],
            ["Veiklos aprašymas", f"{float(evaluation.veiklos_aprasymas.score):.2f}"],
            ["Rezultato pateikimas", f"{float(evaluation.rezultato_pateikimas.score):.2f}"],
            ["Problemos sprendimas", f"{float(evaluation.problemos_sprendimas.score):.2f}"],
            ["Loginė seka", f"{float(evaluation.logine_seka.score):.2f}"],
        ]

        t = Table(structure_scores, colWidths=[4.5 * inch, 2 * inch])
        t.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (0, -1), font_bold),
                ("FONTNAME", (1, 0), (1, -1), font_regular),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("PADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )
        story.append(t)
        story.append(Spacer(1, 0.1 * inch))

        # Reasons as paragraphs
        structure_data = [
            ("Įvadas", evaluation.ivadas.reason),
            ("Problemos formulavimas", evaluation.problemos_formulavimas.reason),
            ("Uždavinio apibrėžimas", evaluation.uzdavinio_apibrezimas.reason),
            ("Veiklos aprašymas", evaluation.veiklos_aprasymas.reason),
            ("Rezultato pateikimas", evaluation.rezultato_pateikimas.reason),
            ("Problemos sprendimas", evaluation.problemos_sprendimas.reason),
            ("Loginė seka", evaluation.logine_seka.reason),
        ]

        for name, reason in structure_data:
            story.append(Paragraph(f"<b>{name}:</b>", subheading_style))
            story.append(Paragraph(reason, reason_style))

        story.append(Spacer(1, 0.15 * inch))

        # Red flags - scores table + reasons
        story.append(Paragraph("3. Raudonos vėliavos", heading_style))

        red_flag_scores = [
            ["'Praktikos' žodžiai", f"{float(evaluation.praktikos_zodziai.score):.2f}"],
            ["Tik modeliavimas", f"{float(evaluation.tik_modeliavimas.score):.2f}"],
            ["Mokslinis naujumas", f"{float(evaluation.mokslinis_naujumas.score):.2f}"],
            ["Tinkama tema", f"{float(evaluation.tinkama_tema.score):.2f}"],
        ]

        t = Table(red_flag_scores, colWidths=[4.5 * inch, 2 * inch])
        t.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (0, -1), font_bold),
                ("FONTNAME", (1, 0), (1, -1), font_regular),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("PADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )
        story.append(t)
        story.append(Spacer(1, 0.1 * inch))

        # Reasons as paragraphs
        red_flag_data = [
            ("'Praktikos' žodžiai", evaluation.praktikos_zodziai.reason),
            ("Tik modeliavimas", evaluation.tik_modeliavimas.reason),
            ("Mokslinis naujumas", evaluation.mokslinis_naujumas.reason),
            ("Tinkama tema", evaluation.tinkama_tema.reason),
        ]

        for name, reason in red_flag_data:
            story.append(Paragraph(f"<b>{name}:</b>", subheading_style))
            story.append(Paragraph(reason, reason_style))

        story.append(Spacer(1, 0.15 * inch))

        # Result type assessment - simple score table
        story.append(Paragraph("4. Rezultato tipas", heading_style))

        result_types = [
            ["Fundamentiniai tyrimai", f"{float(evaluation.rezultato_tipas_fundamentiniai_tyrimai.score):.2f}"],
            ["Koncepcija", f"{float(evaluation.rezultato_tipas_koncepcija.score):.2f}"],
            ["Parametrai", f"{float(evaluation.rezultato_tipas_parametrai.score):.2f}"],
            ["Pirminis maketas", f"{float(evaluation.rezultato_tipas_pirminis_maketas.score):.2f}"],
            ["Realus maketas", f"{float(evaluation.rezultato_tipas_realus_maketas.score):.2f}"],
            ["Prototipas", f"{float(evaluation.rezultato_tipas_prototipas.score):.2f}"],
            ["Galutinis prototipas", f"{float(evaluation.rezultato_tipas_galutinis_prototipas.score):.2f}"],
            ["Bandomoji partija", f"{float(evaluation.rezultato_tipas_bandomoji_partija.score):.2f}"],
        ]

        t = Table(result_types, colWidths=[4.5 * inch, 2 * inch])
        t.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (0, -1), font_bold),
                ("FONTNAME", (1, 0), (1, -1), font_regular),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("PADDING", (0, 0), (-1, -1), 8),
            ])
        )
        story.append(t)
        story.append(Spacer(1, 0.15 * inch))

        # Assessment overview
        story.append(Paragraph("Vertinimo apžvalga", heading_style))
        story.append(Paragraph(evaluation.assessment_overview, body_style))
        story.append(Spacer(1, 0.2 * inch))

    # Appendix: Detailed criterion scores table
    story.append(PageBreak())
    story.append(Paragraph("Priedas: Detalūs kriterijai", title_style))
    story.append(Spacer(1, 0.1 * inch))

    # Group results by model
    results_by_model = {}
    for result in results:
        model_name = result.get("model", "N/A")
        if model_name not in results_by_model:
            results_by_model[model_name] = []
        results_by_model[model_name].append(result)

    # Create one table per model (each model on a new page)
    for model_idx, (model_name, model_results) in enumerate(sorted(results_by_model.items())):
        if model_idx > 0:
            story.append(PageBreak())

        # Model name
        story.append(Paragraph(f"Modelis: {model_name}", title_style))
        story.append(Spacer(1, 0.05 * inch))

        # Table header with vertical text and full names
        header = ["Dokumentas"] + [
            VerticalText(text, font_bold, 8) for text in
            ["Naujumas", "Kūrybiškumas", "Neapibrėžtumas", "Sistemingumas", "Perduodamumas",
             "Įvadas", "Problemos formulavimas", "Uždavinio apibrėžimas", "Veiklos aprašymas"]
        ]

        table_data = [header]

        # Add rows for each document
        for result in model_results:
            evaluation = parse_mtep_evaluation(result)[1]
            file_name = Path(result.get("file", "Unknown")).name

            row = [
                file_name,
                f"{float(evaluation.naujumas.score):.2f}",
                f"{float(evaluation.kurybiskumas.score):.2f}",
                f"{float(evaluation.neapibreztumas.score):.2f}",
                f"{float(evaluation.sistemingumas.score):.2f}",
                f"{float(evaluation.perduodamumas.score):.2f}",
                f"{float(evaluation.ivadas.score):.2f}",
                f"{float(evaluation.problemos_formulavimas.score):.2f}",
                f"{float(evaluation.uzdavinio_apibrezimas.score):.2f}",
                f"{float(evaluation.veiklos_aprasymas.score):.2f}",
            ]
            table_data.append(row)

        # Column widths - narrower for vertical text
        col_widths = [1.5*inch] + [0.55*inch]*9

        t = Table(table_data, colWidths=col_widths)
        t.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (0, 0), font_bold),  # Only Dokumentas header
                ("FONTNAME", (0, 1), (-1, -1), font_regular),  # Data rows
                ("FONTSIZE", (0, 0), (0, 0), 9),  # Dokumentas header
                ("FONTSIZE", (0, 1), (-1, -1), 8),  # Data rows
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("PADDING", (0, 0), (-1, -1), 3),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
                ("VALIGN", (0, 0), (-1, 0), "BOTTOM"),  # Bottom align headers for vertical text
                ("VALIGN", (0, 1), (-1, -1), "MIDDLE"),
            ])
        )
        story.append(t)
        story.append(Spacer(1, 0.2 * inch))

        # Red flags table
        story.append(Paragraph(f"Raudonos vėliavos - {model_name}", heading_style))
        story.append(Spacer(1, 0.05 * inch))

        red_flag_header = ["Dokumentas", "'Praktikos' žodžiai", "Tik modeliavimas", "Mokslinis naujumas", "Tinkama tema"]
        red_flag_data = [red_flag_header]

        for result in model_results:
            evaluation = parse_mtep_evaluation(result)[1]
            file_name = Path(result.get("file", "Unknown")).name

            row = [
                file_name,
                f"{float(evaluation.praktikos_zodziai.score):.2f}",
                f"{float(evaluation.tik_modeliavimas.score):.2f}",
                f"{float(evaluation.mokslinis_naujumas.score):.2f}",
                f"{float(evaluation.tinkama_tema.score):.2f}",
            ]
            red_flag_data.append(row)

        red_flag_widths = [1.5*inch] + [1.25*inch]*4

        t_red = Table(red_flag_data, colWidths=red_flag_widths)
        t_red.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), font_bold),
                ("FONTNAME", (0, 1), (-1, -1), font_regular),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("PADDING", (0, 0), (-1, -1), 3),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )
        story.append(t_red)
        story.append(Spacer(1, 0.2 * inch))

        # Result type table
        story.append(Paragraph(f"Rezultato tipas - {model_name}", heading_style))
        story.append(Spacer(1, 0.05 * inch))

        result_type_header = ["Dokumentas"] + [
            VerticalText(text, font_bold, 8) for text in
            ["Fundamentiniai tyrimai", "Koncepcija", "Parametrai", "Pirminis maketas",
             "Realus maketas", "Prototipas", "Galutinis prototipas", "Bandomoji partija"]
        ]
        result_type_data = [result_type_header]

        for result in model_results:
            evaluation = parse_mtep_evaluation(result)[1]
            file_name = Path(result.get("file", "Unknown")).name

            row = [
                file_name,
                f"{float(evaluation.rezultato_tipas_fundamentiniai_tyrimai.score):.2f}",
                f"{float(evaluation.rezultato_tipas_koncepcija.score):.2f}",
                f"{float(evaluation.rezultato_tipas_parametrai.score):.2f}",
                f"{float(evaluation.rezultato_tipas_pirminis_maketas.score):.2f}",
                f"{float(evaluation.rezultato_tipas_realus_maketas.score):.2f}",
                f"{float(evaluation.rezultato_tipas_prototipas.score):.2f}",
                f"{float(evaluation.rezultato_tipas_galutinis_prototipas.score):.2f}",
                f"{float(evaluation.rezultato_tipas_bandomoji_partija.score):.2f}",
            ]
            result_type_data.append(row)

        result_type_widths = [1.5*inch] + [0.625*inch]*8

        t_result = Table(result_type_data, colWidths=result_type_widths)
        t_result.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (0, 0), font_bold),  # Only Dokumentas header
                ("FONTNAME", (0, 1), (-1, -1), font_regular),  # Data rows
                ("FONTSIZE", (0, 0), (0, 0), 9),  # Dokumentas header
                ("FONTSIZE", (0, 1), (-1, -1), 8),  # Data rows
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("PADDING", (0, 0), (-1, -1), 3),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
                ("VALIGN", (0, 0), (-1, 0), "BOTTOM"),  # Bottom align headers for vertical text
                ("VALIGN", (0, 1), (-1, -1), "MIDDLE"),
            ])
        )
        story.append(t_result)


    # Build PDF
    doc.build(story)
    print(f"✓ PDF report generated: {output_path}")


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nError: Please provide evaluation JSON file")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    if not json_path.exists():
        print(f"Error: File not found: {json_path}")
        sys.exit(1)

    try:
        create_pdf_report(json_path, output_path)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
