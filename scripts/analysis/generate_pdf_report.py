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
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from ataskaitos.agent_from_human import MTEPVertinimas


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
    font_regular, font_bold, font_italic = register_fonts()

    # Load evaluation data
    data = load_evaluation(json_path)
    results = data.get("results", [])

    if not results:
        print("No evaluation results found in JSON")
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
    models = list(set(result.get("model", "N/A") for result in results))
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

    # Process each evaluation
    for idx, result in enumerate(results):
        if idx > 0:
            story.append(PageBreak())

        document_name, evaluation = parse_mtep_evaluation(result)
        file_path = result.get("file", "Unknown")
        model_name = result.get("model", "N/A")

        # Document header with file path
        story.append(Paragraph(f"Dokumentas {idx + 1}", title_style))
        story.append(Spacer(1, 0.05 * inch))

        # File path in a box
        file_para = Paragraph(
            f'<font size="9" color="#555555">{file_path}</font>',
            body_style
        )
        file_table = [[file_para]]
        t = Table(file_table, colWidths=[6.5 * inch])
        t.setStyle(
            TableStyle([
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#95a5a6")),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ecf0f1")),
                ("PADDING", (0, 0), (-1, -1), 8),
            ])
        )
        story.append(t)
        story.append(Spacer(1, 0.05 * inch))

        # Model for this document
        story.append(Paragraph(f"<b>Modelis:</b> {model_name}", body_style))
        story.append(Spacer(1, 0.1 * inch))

        # Final score (prominent)
        final_score = float(evaluation.score) if evaluation.score else 0.0
        score_color = create_score_color(final_score)

        score_para = Paragraph(
            f'<font size="20" color="{score_color}"><b>{final_score:.2f}</b></font>',
            body_style,
        )
        label_para = Paragraph("<b>GALUTINIS BALAS</b>", body_style)

        score_table = [[label_para, score_para]]
        t = Table(score_table, colWidths=[3 * inch, 3.5 * inch])
        t.setStyle(
            TableStyle([
                ("BOX", (0, 0), (-1, -1), 2, colors.grey),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8f9fa")),
                ("PADDING", (0, 0), (-1, -1), 12),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )
        story.append(t)
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
