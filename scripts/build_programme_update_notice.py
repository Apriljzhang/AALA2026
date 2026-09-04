#!/usr/bin/env python3
"""Build the one-page AALA 2026 programme update notice."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/AALA2026-programme-update-AALA2026015-AALA2026034.pdf"
LOGO = ROOT / "aala2026-logo-transparent.png"

TEAL = colors.HexColor("#0E625F")
TEAL_PALE = colors.HexColor("#E7F3F1")
GOLD = colors.HexColor("#D5A83D")
INK = colors.HexColor("#243746")
MUTED = colors.HexColor("#5C6B73")
WHITE = colors.white

NOTICE = (
    "Programme update: <b>AALA2026015</b> will now be presented on "
    "<b>Saturday, 19 September, from 14:00-14:30 in L207</b>, while "
    "<b>AALA2026034</b> will now be presented on "
    "<b>Sunday, 20 September, from 15:30-16:00 in HG02</b>."
)


def register_fonts() -> None:
    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("AALARegular", font_dir / "Arial.ttf"))
    pdfmetrics.registerFont(TTFont("AALABold", font_dir / "Arial Bold.ttf"))
    pdfmetrics.registerFontFamily(
        "AALARegular", normal="AALARegular", bold="AALABold"
    )


def build() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    width, height = A4
    pdf = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    pdf.setTitle("AALA 2026 Programme Update")
    pdf.setAuthor("AALA 2026 Local Organising Committee")
    pdf.setSubject("Schedule update for AALA2026015 and AALA2026034")

    pdf.setFillColor(WHITE)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.rect(0, height - 57 * mm, width, 57 * mm, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.rect(0, height - 59 * mm, width, 2 * mm, fill=1, stroke=0)

    if LOGO.is_file():
        pdf.setFillColor(WHITE)
        pdf.roundRect(14 * mm, height - 50 * mm, 51 * mm, 42 * mm, 4 * mm, fill=1, stroke=0)
        logo = ImageReader(str(LOGO))
        logo_width, logo_height = logo.getSize()
        target_width = 34 * mm
        target_height = target_width * logo_height / logo_width
        pdf.drawImage(
            logo,
            14 * mm + (51 * mm - target_width) / 2,
            height - 50 * mm + (42 * mm - target_height) / 2,
            width=target_width,
            height=target_height,
            mask="auto",
            preserveAspectRatio=True,
        )

    pdf.setFillColor(WHITE)
    pdf.setFont("AALABold", 25)
    pdf.drawRightString(width - 18 * mm, height - 26 * mm, "PROGRAMME UPDATE")
    pdf.setFont("AALARegular", 11)
    pdf.drawRightString(width - 18 * mm, height - 35 * mm, "4 September 2026")

    panel_x = 18 * mm
    panel_y = 72 * mm
    panel_width = width - 36 * mm
    panel_height = 145 * mm
    pdf.setFillColor(TEAL_PALE)
    pdf.roundRect(panel_x, panel_y, panel_width, panel_height, 5 * mm, fill=1, stroke=0)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.2)
    pdf.roundRect(panel_x, panel_y, panel_width, panel_height, 5 * mm, fill=0, stroke=1)

    style = ParagraphStyle(
        "notice",
        fontName="AALARegular",
        fontSize=20,
        leading=29,
        textColor=INK,
        alignment=TA_CENTER,
        spaceAfter=0,
    )
    paragraph = Paragraph(NOTICE, style)
    text_width = panel_width - 22 * mm
    _, text_height = paragraph.wrap(text_width, panel_height)
    paragraph.drawOn(
        pdf,
        panel_x + 11 * mm,
        panel_y + (panel_height - text_height) / 2,
    )

    pdf.setFillColor(MUTED)
    pdf.setFont("AALARegular", 9)
    pdf.drawCentredString(
        width / 2,
        40 * mm,
        "AALA 2026 | 18-21 September 2026 | City University of Macau",
    )
    pdf.setFillColor(TEAL)
    pdf.setFont("AALABold", 10)
    pdf.drawCentredString(width / 2, 31 * mm, "aalaconference.com/program.html")

    pdf.showPage()
    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
