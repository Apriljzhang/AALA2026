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
UPDATED = "17 August 2026"

CATEGORY_COLOURS = {
    "featured": (colors.HexColor("#FFF0D7"), colors.HexColor("#C87A12")),
    "theme-1": (colors.HexColor("#FDE1E8"), colors.HexColor("#C74364")),
    "theme-2": (colors.HexColor("#DDF1FA"), colors.HexColor("#2584A8")),
    "theme-3": (colors.HexColor("#E3F5DE"), colors.HexColor("#4F8C3A")),
    "theme-4": (colors.HexColor("#EEE5FA"), colors.HexColor("#7652A8")),
    "symposium": (colors.HexColor("#FFD9D5"), colors.HexColor("#C33B32")),
    "editors-forum": (colors.HexColor("#FFD9D5"), colors.HexColor("#C33B32")),
    "sponsor": (colors.HexColor("#FFF3C8"), colors.HexColor("#9A7514")),
    "poster": (colors.HexColor("#F1E8F7"), colors.HexColor("#85539C")),
    "plenary": (colors.HexColor("#DDF0E3"), colors.HexColor("#34784A")),
    "ceremony": (colors.HexColor("#DDF0E3"), colors.HexColor("#34784A")),
    "break": (colors.HexColor("#FFF2C6"), colors.HexColor("#A27B16")),
    "workshop": (colors.HexColor("#DDF3F6"), colors.HexColor("#267C87")),
    "other": (colors.HexColor("#E3F3F5"), colors.HexColor("#377F87")),
}

ROOM_ORDER = [
    "Culture Centre Room 1", "Culture Centre Room 2", "HG01", "HG02", "HG03",
    "L205", "L206", "L207", "L305", "L306", "L307", "Poster area",
]
SHARED = {"break", "plenary", "ceremony"}


def category_colours(event):
    return CATEGORY_COLOURS.get(event.get("category"), (WHITE, TEAL_MID))


def day_label(day):
    labels = {"Saturday": "Day 1 - 19 September", "Sunday": "Day 2 - 20 September"}
    return labels.get(day.get("weekday"), f"{clean(day.get('weekday'))}, {clean(day.get('date'))}")


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
    c.drawString(12 * mm, 7 * mm, f"City University of Macau | 18-21 September 2026 | Updated {UPDATED} | Programme details and time slots are subject to adjustment.")
    c.drawRightString(width - 12 * mm, 7 * mm, f"Page {page_number} of {total_pages}")


def concurrent_blocks(day):
    events = session_events(day)
    if not events:
        return []
    occupied = []
    for minute in range(
        min(to_minutes(event["start"]) for event in events),
        max(to_minutes(event["end"]) for event in events),
        30,
    ):
        active = [
            event for event in events
            if to_minutes(event["start"]) <= minute < to_minutes(event["end"])
        ]
        if len(active) >= 2:
            occupied.append(minute)
    groups = []
    for minute in occupied:
        if not groups or minute != groups[-1][-1] + 30:
            groups.append([minute])
        else:
            groups[-1].append(minute)
    blocks = []
    for group in groups:
        start = group[0]
        end = group[-1] + 30
        rooms = sorted(
            {
                event["room"] for event in events
                if to_minutes(event["start"]) < end and to_minutes(event["end"]) > start
            },
            key=lambda room: ROOM_ORDER.index(room) if room in ROOM_ORDER else 99,
        )
        blocks.append({
            "id": "",
            "title": "Concurrent sessions",
            "abstract": "",
            "authors": [],
            "category": "other",
            "categoryLabel": f"{len(rooms)} rooms",
            "room": ", ".join(rooms),
            "start": from_minutes(start),
            "end": from_minutes(end),
        })
    return blocks


def draw_overview(c, day, page_number, total_pages):
    header(
        c,
        "AALA2026 at a glance",
        f"{day_label(day)} | Shared sessions, including plenary sessions",
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
    timeline = shared + concurrent_blocks(day)
    original_order = {id(event): index for index, event in enumerate(day["events"])}
    timeline.sort(key=lambda event: (to_minutes(event["start"]), original_order.get(id(event), len(day["events"]))))
    y = top - 20 * mm
    note = "Detailed room assignments are shown on the following pages."
    for font_size in (9.5, 9.0, 8.5, 8.0, 7.5):
        card_specs = []
        for event in timeline:
            markup = event_markup(event, include_room=True)
            item, used = paragraph(markup, col_width - 12 * mm, font_size)
            card_specs.append((event, item, used + 3.2 * mm))
        note_item, note_h = paragraph(f"<b>{xml(note)}</b>", col_width - 12 * mm, font_size, color=TEAL)
        required = sum(card_h + 1.2 * mm for _, _, card_h in card_specs) + note_h + 4 * mm
        if required <= y - bottom:
            break
    else:
        raise ValueError(f"Overview timeline does not fit: {day['date']}")
    for event, item, card_h in card_specs:
        fill, accent = category_colours(event)
        c.setFillColor(fill)
        c.setStrokeColor(RULE)
        c.roundRect(x + 4 * mm, y - card_h, col_width - 8 * mm, card_h, 1.5 * mm, fill=1, stroke=1)
        c.setFillColor(accent)
        c.rect(x + 4 * mm, y - 1.2 * mm, col_width - 8 * mm, 1.2 * mm, fill=1, stroke=0)
        item.drawOn(c, x + 6 * mm, y - card_h + 1.6 * mm)
        y -= card_h + 1.2 * mm
    c.setFillColor(TEAL_PALE)
    c.setStrokeColor(TEAL_MID)
    c.roundRect(x + 4 * mm, y - note_h - 3 * mm, col_width - 8 * mm, note_h + 3 * mm, 1.5 * mm, fill=1, stroke=1)
    note_item.drawOn(c, x + 6 * mm, y - note_h - 1.5 * mm)
    c.showPage()


def card_height(event, width, size, include_room=False):
    _, used = paragraph(event_markup(event, include_room=include_room), width - 3 * mm, size)
    return used + 3 * mm


def to_minutes(value):
    hour, minute = map(int, value.split(":"))
    return hour * 60 + minute


def from_minutes(value):
    return f"{value // 60:02d}:{value % 60:02d}"


def time_slots(events):
    start = min(to_minutes(event["start"]) for event in events)
    end = max(to_minutes(event["end"]) for event in events)
    return [from_minutes(value) for value in range(start, end, 30)]


def grid_layout(events, width, size):
    slots = time_slots(events)
    gap = 1.5 * mm
    row_heights = []
    for slot in slots:
        short_events = [
            event for event in events
            if event["start"] == slot and to_minutes(event["end"]) - to_minutes(event["start"]) <= 30
        ]
        row_heights.append(max([14 * mm] + [card_height(event, width, size) for event in short_events]))
    for event in events:
        covered = [index for index, slot in enumerate(slots) if event["start"] <= slot < event["end"]]
        if not covered:
            continue
        available = sum(row_heights[index] for index in covered) + gap * (len(covered) - 1)
        needed = card_height(event, width, size)
        if needed > available:
            extra = (needed - available) / len(covered)
            for index in covered:
                row_heights[index] += extra
    return slots, row_heights


def grid_height(events, rooms, width, size):
    slots, heights = grid_layout(events, width, size)
    return sum(heights) + 1.5 * mm * max(0, len(slots) - 1)


def fit_grid_font(events, rooms, width, available_height):
    for size in (8.0, 7.6, 7.2, 6.8, 6.4):
        if grid_height(events, rooms, width, size) <= available_height:
            return size
    raise ValueError("Time-grid content does not fit at the minimum 6.4-point size")


def draw_room_page(c, day, rooms, events, part, parts, page_number, total_pages):
    window_start = min(event["start"] for event in events)
    window_end = max(event["end"] for event in events)
    header(
        c,
        "AALA2026 at a glance",
        f"{day_label(day)} | Concurrent sessions {window_start}-{window_end} | {len(rooms)} rooms | Part {part} of {parts}",
        page_number,
        total_pages,
    )
    width, height = landscape(A4)
    left, right, gap = 8 * mm, 8 * mm, 1.2 * mm
    top, bottom = height - 32 * mm, 14 * mm
    col_width = (width - left - right - gap * (len(rooms) - 1)) / len(rooms)
    available = top - 13 * mm - bottom
    size = fit_grid_font(events, rooms, col_width, available)
    for index, room in enumerate(rooms):
        x = left + index * (col_width + gap)
        c.setFillColor(TEAL)
        c.roundRect(x, top - 10 * mm, col_width, 10 * mm, 1.2 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("AALABold", 7.2 if len(rooms) >= 9 else 9.0)
        c.drawCentredString(x + col_width / 2, top - 6.4 * mm, clean(room))
    slots, row_heights = grid_layout(events, col_width, size)
    row_tops = []
    y = top - 13 * mm
    for row_h in row_heights:
        row_tops.append(y)
        y -= row_h + 1.5 * mm
    for index, room in enumerate(rooms):
        x = left + index * (col_width + gap)
        room_events = [event for event in events if event.get("room") == room]
        for slot_index, slot in enumerate(slots):
            active = [event for event in room_events if event["start"] <= slot < event["end"]]
            if active and active[0]["start"] != slot:
                continue
            top_y = row_tops[slot_index]
            if active:
                event = active[0]
                covered = [i for i, candidate in enumerate(slots) if event["start"] <= candidate < event["end"]]
                span_h = sum(row_heights[i] for i in covered) + 1.5 * mm * (len(covered) - 1)
                item, used = paragraph(event_markup(event), col_width - 3 * mm, size)
                fill, accent = category_colours(event)
                c.setFillColor(fill)
                c.setStrokeColor(RULE)
                c.roundRect(x, top_y - span_h, col_width, span_h, 1.2 * mm, fill=1, stroke=1)
                c.setFillColor(accent)
                c.rect(x, top_y - 1.0 * mm, col_width, 1.0 * mm, fill=1, stroke=0)
                item.drawOn(c, x + 1.5 * mm, top_y - used - 1.5 * mm)
            else:
                row_h = row_heights[slot_index]
                c.setFillColor(TEAL_PALE)
                c.setStrokeColor(RULE)
                c.roundRect(x, top_y - row_h, col_width, row_h, 1.2 * mm, fill=1, stroke=1)
                c.setFillColor(MUTED)
                c.setFont("AALARegular", 5.8)
                c.drawCentredString(x + col_width / 2, top_y - 5 * mm, f"No {slot} session")
    c.showPage()


def workshop_panel(c, day, x, panel_width, top, bottom):
    all_events = [event for event in day["events"] if not event.get("posters")]
    session_rooms = sorted(
        {event["room"] for event in session_events(day)},
        key=lambda room: ROOM_ORDER.index(room) if room in ROOM_ORDER else 99,
    )
    columns = ["Shared activities"] + session_rooms
    gap = 1.8 * mm
    col_width = (panel_width - gap * (len(columns) - 1)) / len(columns)
    c.setFillColor(TEAL)
    c.roundRect(x, top - 12 * mm, panel_width, 12 * mm, 1.8 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("AALABold", 11)
    c.drawString(x + 4 * mm, top - 5.2 * mm, f"{clean(day['weekday'])}, {clean(day['date'])}")
    c.setFont("AALARegular", 7.5)
    c.drawString(x + 4 * mm, top - 9.4 * mm, "Shared activities and workshops")
    heading_y = top - 15 * mm
    for index, column in enumerate(columns):
        col_x = x + index * (col_width + gap)
        c.setFillColor(TEAL_MID)
        c.roundRect(col_x, heading_y - 9 * mm, col_width, 9 * mm, 1.2 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("AALABold", 7.0 if len(columns) > 3 else 8.2)
        c.drawCentredString(col_x + col_width / 2, heading_y - 5.8 * mm, clean(column))

    def column_for(event):
        return event["room"] if event.get("category") not in SHARED else "Shared activities"

    available = heading_y - 12 * mm - bottom
    starts = sorted({event["start"] for event in all_events})
    for size in (8.5, 8.0, 7.5, 7.0, 6.5):
        needed = 0
        for start in starts:
            row = [event for event in all_events if event["start"] == start]
            needed += max(card_height(event, col_width, size, include_room=event.get("category") in SHARED) for event in row) + 1.5 * mm
        if needed <= available:
            break
    y = heading_y - 12 * mm
    for start in starts:
        row = [event for event in all_events if event["start"] == start]
        row_h = max(card_height(event, col_width, size, include_room=event.get("category") in SHARED) for event in row)
        for index, column in enumerate(columns):
            col_x = x + index * (col_width + gap)
            matching = [event for event in row if column_for(event) == column]
            c.setStrokeColor(RULE)
            fill, accent = category_colours(matching[0]) if matching else (TEAL_PALE, TEAL_MID)
            c.setFillColor(fill)
            c.roundRect(col_x, y - row_h, col_width, row_h, 1.2 * mm, fill=1, stroke=1)
            if matching:
                event = matching[0]
                item, used = paragraph(
                    event_markup(event, include_room=event.get("category") in SHARED),
                    col_width - 3 * mm,
                    size,
                )
                c.setFillColor(accent)
                c.rect(col_x, y - 1.0 * mm, col_width, 1.0 * mm, fill=1, stroke=0)
                item.drawOn(c, col_x + 1.5 * mm, y - used - 1.5 * mm)
            else:
                c.setFillColor(MUTED)
                c.setFont("AALARegular", 5.8)
                c.drawCentredString(col_x + col_width / 2, y - 5 * mm, f"No {start} activity")
        y -= row_h + 1.5 * mm


def draw_workshop_page(c, friday, monday, page_number, total_pages):
    header(
        c,
        "AALA2026 at a glance",
        "18 & 21 September | Workshops, registration and shared activities",
        page_number,
        total_pages,
    )
    width, height = landscape(A4)
    left, right, gap = 8 * mm, 8 * mm, 5 * mm
    top, bottom = height - 32 * mm, 14 * mm
    friday_width = (width - left - right - gap) * 0.64
    monday_width = width - left - right - gap - friday_width
    workshop_panel(c, friday, left, friday_width, top, bottom)
    workshop_panel(c, monday, left + friday_width + gap, monday_width, top, bottom)
    c.showPage()


def draw_poster_page(c, day, poster_band, page_number, total_pages):
    header(c, "AALA2026 at a glance", f"{day_label(day)} | Poster presentations | {poster_band['start']}-{poster_band['end']} | {clean(poster_band.get('room'))}", page_number, total_pages)
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
            fill, accent = category_colours(event)
            c.setFillColor(fill)
            c.setStrokeColor(RULE)
            c.roundRect(x, y - card_h, col_width, card_h, 1.5 * mm, fill=1, stroke=1)
            c.setFillColor(accent)
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
    current_end = "00:00"
    for start in starts:
        start_events = [event for event in events if event["start"] == start]
        starts_long_event = any(to_minutes(event["end"]) - to_minutes(event["start"]) > 30 for event in start_events)
        must_continue = bool(current_starts) and start < current_end
        proposed_starts = current_starts + [start]
        proposed_events = [event for event in events if event["start"] in proposed_starts]
        fits = grid_height(proposed_events, rooms, col_width, 6.4) <= available
        should_break = current_starts and not must_continue and (len(current_starts) >= 2 or starts_long_event or not fits)
        if should_break:
            groups.append([event for event in events if event["start"] in current_starts])
            current_starts = [start]
            current_end = max(event["end"] for event in start_events)
        else:
            current_starts = proposed_starts
            current_end = max([current_end] + [event["end"] for event in start_events])
        current_events = [event for event in events if event["start"] in current_starts]
        if grid_height(current_events, rooms, col_width, 6.4) > available:
            raise ValueError(f"Session group does not fit: {day['date']} {current_starts}")
    if current_starts:
        groups.append([event for event in events if event["start"] in current_starts])
    return groups


def build_specs(data):
    friday = next(day for day in data["days"] if day["weekday"] == "Friday")
    monday = next(day for day in data["days"] if day["weekday"] == "Monday")
    specs = [("workshops", (friday, monday))]
    for day in data["days"]:
        if day["weekday"] in {"Friday", "Monday"}:
            continue
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
        if kind == "workshops":
            draw_workshop_page(pdf, *payload, page_number, len(specs))
        elif kind == "overview":
            draw_overview(pdf, *payload, page_number, len(specs))
        elif kind == "rooms":
            draw_room_page(pdf, *payload, page_number, len(specs))
        else:
            draw_poster_page(pdf, *payload, page_number, len(specs))
    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
