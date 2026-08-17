#!/usr/bin/env python3
"""Build the printable A4 AALA 2026 detailed daily programme."""

import json
import re
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "program-data.js"
OUTPUT = ROOT / "output/pdf/AALA2026 at a glance.pdf"

WHITE = colors.HexColor("#FFFFFF")
PAPER = colors.HexColor("#F8FAF9")
INK = colors.HexColor("#243746")
MUTED = colors.HexColor("#5C6B73")
TEAL = colors.HexColor("#0E625F")
TEAL_MID = colors.HexColor("#167F7A")
TEAL_PALE = colors.HexColor("#E7F3F1")
GOLD = colors.HexColor("#D5A83D")
RULE = colors.HexColor("#CDD8D6")

ROOM_ORDER = [
    "Culture Centre Room 1", "Culture Centre Room 2", "HG01", "HG02", "HG03",
    "L205", "L206", "L207", "L305", "L306", "L307", "Poster area",
]
SHARED = {"break", "plenary", "ceremony"}


def clean(value):
    text = str(value or "")
    for old, new in {
        "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-",
        "\u2014": "-", "\u2212": "-", "\u00a0": " ",
    }.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text).strip()


def xml(value):
    return escape(clean(value), quote=True)


def register_fonts():
    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("AALARegular", font_dir / "Arial.ttf"))
    pdfmetrics.registerFont(TTFont("AALABold", font_dir / "Arial Bold.ttf"))
    pdfmetrics.registerFontFamily("AALARegular", normal="AALARegular", bold="AALABold")


def load_data():
    source = DATA.read_text(encoding="utf-8")
    match = re.fullmatch(r"\s*window\.AALA_PROGRAM\s*=\s*(\{.*\});\s*", source, re.S)
    if not match:
        raise ValueError("Could not parse program-data.js")
    return json.loads(match.group(1))


def authors(event):
    labels = []
    for author in event.get("authors", []):
        label = clean(author.get("name"))
        if event.get("id") == "AALA20260206" and author.get("affiliation"):
            label = f"{label} ({clean(author.get('affiliation'))})"
        if label:
            labels.append(label)
    return "; ".join(labels)


def paragraph(markup, width, font_size, color=INK, leading=None):
    style = ParagraphStyle(
        "a4-programme",
        fontName="AALARegular",
        fontSize=font_size,
        leading=leading or font_size * 1.18,
        textColor=color,
        alignment=TA_LEFT,
        allowWidows=0,
        allowOrphans=0,
        splitLongWords=True,
    )
    item = Paragraph(markup, style)
    _, height = item.wrap(width, 1000 * mm)
    return item, height


def event_markup(event, include_room=False):
    meta = f"<b>{xml(event.get('start'))}-{xml(event.get('end'))}</b>"
    if include_room and event.get("room"):
        meta += f" | {xml(event.get('room'))}"
    if event.get("categoryLabel"):
        meta += f" | {xml(event.get('categoryLabel'))}"
    identity = f"<i>{xml(event.get('id'))}</i><br/>" if event.get("id") else ""
    author_line = authors(event)
    author_markup = f"<br/>{xml(author_line)}" if author_line else ""
    return f'<font color="{MUTED.hexval()}">{meta}</font><br/>{identity}<b>{xml(event.get("title"))}</b>{author_markup}'


def header(c, title, subtitle, page_number, total_pages):
    width, height = landscape(A4)
    c.setFillColor(WHITE)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, height - 25 * mm, width, 25 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("AALABold", 19)
    c.drawString(12 * mm, height - 10 * mm, title)
    c.setFont("AALARegular", 10)
    c.drawString(12 * mm, height - 17 * mm, subtitle)
    c.setFillColor(GOLD)
    c.rect(0, height - 26 * mm, width, 1 * mm, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont("AALARegular", 7.5)
    c.drawString(12 * mm, 7 * mm, "University of Macau | 18-21 September 2026 | Programme details and time slots are subject to adjustment.")
    c.drawRightString(width - 12 * mm, 7 * mm, f"Page {page_number} of {total_pages}")


def draw_overview(c, day, page_number, total_pages):
    header(
        c,
        "AALA2026 at a glance",
        f"{clean(day['weekday'])}, {clean(day['date'])} | Shared programme and conference-wide activities",
        page_number,
        total_pages,
    )
    width, height = landscape(A4)
    left, right = 30 * mm, 30 * mm
    top, bottom = height - 32 * mm, 13 * mm
    col_width = width - left - right
    x = left
    c.setFillColor(TEAL_PALE)
    c.setStrokeColor(RULE)
    c.roundRect(x, bottom, col_width, top - bottom, 2 * mm, fill=1, stroke=1)
    c.setFillColor(TEAL)
    c.rect(x, top - 15 * mm, col_width, 15 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("AALABold", 13)
    c.drawString(x + 5 * mm, top - 6 * mm, clean(day["weekday"]))
    c.setFont("AALARegular", 10)
    c.drawString(x + 5 * mm, top - 11 * mm, clean(day["date"]))
    shared = [event for event in day["events"] if not event.get("posters") and event.get("category") in SHARED]
    y = top - 20 * mm
    for event in shared:
        markup = event_markup(event, include_room=True)
        item, used = paragraph(markup, col_width - 12 * mm, 9.5)
        card_h = used + 4 * mm
        c.setFillColor(WHITE)
        c.setStrokeColor(RULE)
        c.roundRect(x + 4 * mm, y - card_h, col_width - 8 * mm, card_h, 1.5 * mm, fill=1, stroke=1)
        c.setFillColor(TEAL_MID)
        c.rect(x + 4 * mm, y - 1.2 * mm, col_width - 8 * mm, 1.2 * mm, fill=1, stroke=0)
        item.drawOn(c, x + 6 * mm, y - card_h + 2 * mm)
        y -= card_h + 2 * mm
    c.showPage()


def room_height(events, width, size):
    total = 0
    for event in events:
        _, used = paragraph(event_markup(event), width - 3 * mm, size)
        total += used + 3 * mm + 1.2 * mm
    return total


def fit_room_font(events, width, available_height):
    for size in (8.0, 7.6, 7.2, 6.8, 6.4):
        if room_height(events, width, size) <= available_height:
            return size
    raise ValueError("Room content does not fit at the minimum 6.4-point size")


def draw_room_page(c, day, rooms, events, part, parts, page_number, total_pages):
    window_start = min(event["start"] for event in events)
    window_end = max(event["end"] for event in events)
    header(
        c,
        "AALA2026 at a glance",
        f"{clean(day['weekday'])}, {clean(day['date'])} | Detailed sessions {window_start}-{window_end} | {len(rooms)} rooms | Part {part} of {parts}",
        page_number,
        total_pages,
    )
    width, height = landscape(A4)
    left, right, gap = 8 * mm, 8 * mm, 1.2 * mm
    top, bottom = height - 32 * mm, 14 * mm
    col_width = (width - left - right - gap * (len(rooms) - 1)) / len(rooms)
    room_events = {
        room: sorted(
            [event for event in events if event.get("room") == room],
            key=lambda event: (event["start"], event["end"], event.get("id", "")),
        )
        for room in rooms
    }
    available = top - 13 * mm - bottom
    size = min(fit_room_font(items, col_width, available) for items in room_events.values() if items)
    for index, room in enumerate(rooms):
        x = left + index * (col_width + gap)
        c.setFillColor(TEAL)
        c.roundRect(x, top - 10 * mm, col_width, 10 * mm, 1.2 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("AALABold", 7.2 if len(rooms) >= 9 else 9.0)
        c.drawCentredString(x + col_width / 2, top - 6.4 * mm, clean(room))
        items = room_events[room]
        y = top - 13 * mm
        if not items:
            c.setFillColor(TEAL_PALE)
            c.setStrokeColor(RULE)
            c.roundRect(x, bottom, col_width, y - bottom, 1.2 * mm, fill=1, stroke=1)
            c.setFillColor(MUTED)
            c.setFont("AALARegular", 6.2)
            c.drawCentredString(x + col_width / 2, y - 7 * mm, "No session")
            continue
        for event in items:
            item, used = paragraph(event_markup(event), col_width - 3 * mm, size)
            card_h = used + 3 * mm
            c.setFillColor(WHITE)
            c.setStrokeColor(RULE)
            c.roundRect(x, y - card_h, col_width, card_h, 1.2 * mm, fill=1, stroke=1)
            c.setFillColor(TEAL_MID)
            c.rect(x, y - 1.0 * mm, col_width, 1.0 * mm, fill=1, stroke=0)
            item.drawOn(c, x + 1.5 * mm, y - card_h + 1.5 * mm)
            y -= card_h + 1.2 * mm
    c.showPage()


def draw_poster_page(c, day, poster_band, page_number, total_pages):
    header(c, "AALA2026 at a glance", f"{clean(day['weekday'])}, {clean(day['date'])} | Poster presentations | {poster_band['start']}-{poster_band['end']} | {clean(poster_band.get('room'))}", page_number, total_pages)
    width, height = landscape(A4)
    left, right, gap = 12 * mm, 12 * mm, 6 * mm
    top, bottom = height - 32 * mm, 14 * mm
    posters = poster_band.get("posters", [])
    split = (len(posters) + 1) // 2
    columns = [posters[:split], posters[split:]]
    col_width = (width - left - right - gap) / 2
    for index, items in enumerate(columns):
        x = left + index * (col_width + gap)
        y = top
        for event in items:
            item, used = paragraph(event_markup(event), col_width - 8 * mm, 8.5)
            card_h = used + 6 * mm
            c.setFillColor(WHITE)
            c.setStrokeColor(RULE)
            c.roundRect(x, y - card_h, col_width, card_h, 1.5 * mm, fill=1, stroke=1)
            c.setFillColor(TEAL_MID)
            c.rect(x, y - 1.2 * mm, col_width, 1.2 * mm, fill=1, stroke=0)
            item.drawOn(c, x + 4 * mm, y - card_h + 3 * mm)
            y -= card_h + 2.5 * mm
    c.showPage()


def session_events(day):
    return [
        event for event in day["events"]
        if not event.get("posters") and event.get("category") not in SHARED and event.get("room")
    ]


def session_groups(day, rooms):
    events = session_events(day)
    starts = sorted({event["start"] for event in events})
    width, height = landscape(A4)
    left, right, gap = 8 * mm, 8 * mm, 1.2 * mm
    top, bottom = height - 32 * mm, 14 * mm
    col_width = (width - left - right - gap * (len(rooms) - 1)) / len(rooms)
    available = top - 13 * mm - bottom
    groups = []
    current_starts = []
    for start in starts:
        proposed_starts = current_starts + [start]
        proposed_events = [event for event in events if event["start"] in proposed_starts]
        fits = all(
            room_height([event for event in proposed_events if event.get("room") == room], col_width, 6.4) <= available
            for room in rooms
        )
        if current_starts and (not fits or len(proposed_starts) > 2):
            groups.append([event for event in events if event["start"] in current_starts])
            current_starts = [start]
        else:
            current_starts = proposed_starts
    if current_starts:
        groups.append([event for event in events if event["start"] in current_starts])
    return groups


def build_specs(data):
    specs = []
    for day in data["days"]:
        specs.append(("overview", (day,)))
        events = session_events(day)
        rooms = sorted(
            {event["room"] for event in events},
            key=lambda room: ROOM_ORDER.index(room) if room in ROOM_ORDER else 99,
        )
        groups = session_groups(day, rooms) if rooms else []
        for index, events_in_group in enumerate(groups, 1):
            specs.append(("rooms", (day, rooms, events_in_group, index, len(groups))))
        for event in day["events"]:
            if event.get("posters"):
                specs.append(("posters", (day, event)))
    return specs


def main():
    register_fonts()
    data = load_data()
    specs = build_specs(data)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=landscape(A4), pageCompression=1)
    pdf.setTitle("AALA2026 at a glance")
    pdf.setAuthor("Asian Association for Language Assessment")
    pdf.setSubject("Printable A4 conference programme")
    for page_number, (kind, payload) in enumerate(specs, 1):
        if kind == "overview":
            draw_overview(pdf, *payload, page_number, len(specs))
        elif kind == "rooms":
            draw_room_page(pdf, *payload, page_number, len(specs))
        else:
            draw_poster_page(pdf, *payload, page_number, len(specs))
    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
