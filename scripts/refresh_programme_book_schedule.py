#!/usr/bin/env python3
"""Replace the programme-book schedule section with the current A4 programme."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter, Transformation
from pypdf._page import PageObject


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "output/pdf/AALA2026-programme-book.pdf"
SCHEDULE = ROOT / "output/pdf/AALA2026 at a glance.pdf"
OUTPUT = BOOK
SCHEDULE_MARKER = "AALA2026 at a glance"


def portrait_schedule_page(source):
    page = PageObject.create_blank_page(width=595.276, height=807.874)
    scale = min((595.276 - 72) / source.mediabox.height, (807.874 - 68) / source.mediabox.width)
    source.add_transformation(
        Transformation().scale(scale).rotate(90).translate(36 + source.mediabox.height * scale, 34)
    )
    page.merge_page(source)
    return page


def schedule_range(pages):
    indices = [index for index, page in enumerate(pages) if SCHEDULE_MARKER in (page.extract_text() or "")]
    if not indices:
        raise ValueError("Could not find the existing at-a-glance schedule in the programme book.")
    start = indices[0]
    end = start
    while end < len(pages) and SCHEDULE_MARKER in (pages[end].extract_text() or ""):
        end += 1
    return start, end


def main():
    if not BOOK.is_file() or not SCHEDULE.is_file():
        raise FileNotFoundError("Build the at-a-glance PDF before refreshing the programme book.")
    original = PdfReader(str(BOOK))
    schedule = PdfReader(str(SCHEDULE))
    schedule_start, schedule_end = schedule_range(original.pages)
    writer = PdfWriter()
    for page in original.pages[:schedule_start]:
        writer.add_page(page)
    for source in schedule.pages:
        writer.add_page(portrait_schedule_page(source))
    for page in original.pages[schedule_end:]:
        writer.add_page(page)
    writer.add_metadata({
        "/Title": "AALA 2026 Conference Programme Book",
        "/Author": "Asian Association for Language Assessment",
        "/Subject": "Conference programme with current at-a-glance schedule",
    })
    with OUTPUT.open("wb") as handle:
        writer.write(handle)
    print(OUTPUT)
    print(f"pages={len(writer.pages)}")


if __name__ == "__main__":
    main()
