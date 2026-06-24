from io import BytesIO
from pathlib import Path

import reportlab
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


FONT_NAME = "ZaspaniVera"
FONT_BOLD_NAME = "ZaspaniVeraBold"


def _register_fonts():
    if FONT_NAME in pdfmetrics.getRegisteredFontNames():
        return

    fonts_dir = Path(reportlab.__file__).resolve().parent / "fonts"
    pdfmetrics.registerFont(TTFont(FONT_NAME, fonts_dir / "Vera.ttf"))
    pdfmetrics.registerFont(TTFont(FONT_BOLD_NAME, fonts_dir / "VeraBd.ttf"))


def build_members_pdf(members):
    _register_fonts()
    output = BytesIO()
    document = SimpleDocTemplate(
        output,
        pagesize=landscape(A4),
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title="Raport klubowiczów",
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.fontName = FONT_BOLD_NAME
    title_style.fontSize = 18

    generated_at = timezone.localtime().strftime("%d.%m.%Y %H:%M")
    story = [
        Paragraph("Raport klubowiczów", title_style),
        Paragraph(f"Wygenerowano: {generated_at}", styles["Normal"]),
        Spacer(1, 8 * mm),
    ]

    rows = [[
        "Imię i nazwisko",
        "Login",
        "Telefon",
        "Numer karty",
        "Status",
        "Karnet",
        "Ważny do",
    ]]

    for member in members.select_related("user", "membership_plan"):
        active = member.has_active_membership
        rows.append([
            f"{member.name} {member.surname}",
            member.user.username if member.user else "-",
            member.tel_no or "-",
            member.membership_card,
            "Aktywny" if active else "Nieaktywny",
            member.membership_plan.display_name if active else "-",
            (
                timezone.localtime(member.membership_expires_at).strftime("%d.%m.%Y")
                if active
                else "-"
            ),
        ])

    table = Table(
        rows,
        repeatRows=1,
        colWidths=[43 * mm, 32 * mm, 30 * mm, 27 * mm, 25 * mm, 42 * mm, 27 * mm],
    )
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD_NAME),
        ("FONTNAME", (0, 1), (-1, -1), FONT_NAME),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6B4423")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9A7B5B")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4EEE7")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)

    document.build(story)
    return output.getvalue()
