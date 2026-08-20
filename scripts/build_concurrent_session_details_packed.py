#!/usr/bin/env python3
"""Build compact concurrent-session detail pages.

The layout shortens theme labels to T1-T4 and packs consecutive time-window
sections onto a page when the cards still fit at a readable size.
"""

from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from build_program_a4_pdf import (
    GOLD,
    MUTED,
    PAPER,
    ROOM_ORDER,
    RULE,
    TEAL,
    TEAL_PALE,
    WHITE,
    category_colours,
    clean,
    day_label,
    event_markup,
    grid_height,
    grid_layout,
    header,
    load_data,
    paragraph,
    register_fonts,
    session_events,
    session_groups,
    to_minutes,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/AALA2026-concurrent-session-details-packed.pdf"

CARD_FONT_SIZE = 6.0
POSTER_CARD_FONT_SIZE = 6.1
SECTION_LABEL_HEIGHT = 5.4 * mm
ROOM_HEADER_HEIGHT = 7.0 * mm
SECTION_GAP = 2.2 * mm
LABEL_TO_ROOMS_GAP = 0.8 * mm
ROOMS_TO_GRID_GAP = 1.2 * mm
POSTER_GRID_GAP = 1.6 * mm


def abbreviate_theme_labels(data):
    """Use T1-T4 in this trial without changing the programme source data."""
    for day in data["days"]:
        for event in day["events"]:
            category = event.get("category", "")
            if category in {"theme-1", "theme-2", "theme-3", "theme-4"}:
                event["categoryLabel"] = f"T{category[-1]}"


def detail_specs(data):
    specs = []
    for day in data["days"]:
        if day["weekday"] not in {"Saturday", "Sunday"}:
            continue
        day_specs = []
        events = session_events(day)
        rooms = sorted(
            {event["room"] for event in events},
            key=lambda room: ROOM_ORDER.index(room) if room in ROOM_ORDER else 99,
        )
        groups = session_groups(day, rooms)
        for part, group in enumerate(groups, 1):
            active_rooms = [
                room for room in rooms
                if any(event.get("room") == room for event in group)
            ]
            day_specs.append(("rooms", day, active_rooms, group, part, len(groups)))
        poster_band = poster_band_for_day(day)
        if poster_band:
            day_specs.append(("posters", day, poster_band))
        day_specs.sort(key=spec_start)
        specs.extend(day_specs)
    return specs


def poster_band_for_day(day):
    """Return a poster group with cards timed at the day's presentation slot."""
    source = next((event for event in day["events"] if event.get("posters")), None)
    if not source or not source.get("posters"):
        return None
    presentation_start = source.get("presentationStart", source["start"])
    presentation_end = source.get("presentationEnd", source["end"])
    poster_band = dict(source)
    poster_band["posters"] = [
        {
            **poster,
            "start": presentation_start,
            "end": presentation_end,
            "room": poster.get("room") or source.get("room"),
        }
        for poster in source["posters"]
    ]
    return poster_band


def spec_start(spec):
    if spec[0] == "posters":
        return to_minutes(spec[2]["presentationStart"])
    return min(to_minutes(event["start"]) for event in spec[3])


def section_dimensions(rooms, events, size=CARD_FONT_SIZE):
    width, _ = landscape(A4)
    left = right = 8 * mm
    gap = 1.2 * mm
    col_width = (width - left - right - gap * (len(rooms) - 1)) / len(rooms)
    grid_h = grid_height(events, rooms, col_width, size)
    section_h = (
        SECTION_LABEL_HEIGHT
        + LABEL_TO_ROOMS_GAP
        + ROOM_HEADER_HEIGHT
        + ROOMS_TO_GRID_GAP
        + grid_h
    )
    return col_width, grid_h, section_h


def poster_layout(poster_band):
    width, _ = landscape(A4)
    left = right = 8 * mm
    panel_width = width - left - right
    columns = 5
    card_gap = POSTER_GRID_GAP
    card_width = (panel_width - card_gap * (columns - 1)) / columns
    card_inner_width = card_width - 3 * mm
    rows = []
    posters = poster_band["posters"]
    for index in range(0, len(posters), columns):
        cards = []
        row_height = 0
        for event in posters[index:index + columns]:
            item, used = paragraph(event_markup(event), card_inner_width, POSTER_CARD_FONT_SIZE)
            card_height = used + 4.5 * mm
            cards.append((event, item, used, card_height))
            row_height = max(row_height, card_height)
        rows.append((cards, row_height))
    required = sum(row_height for _, row_height in rows) + card_gap * max(0, len(rows) - 1)
    section_height = SECTION_LABEL_HEIGHT + 1.4 * mm + required
    return panel_width, card_width, card_gap, rows, section_height


def section_height(spec):
    if spec[0] == "posters":
        return poster_layout(spec[2])[-1]
    return section_dimensions(spec[2], spec[3])[2]


def pack_specs(specs):
    """Pack adjacent groups within each day, preserving programme order."""
    _, height = landscape(A4)
    top = height - 32 * mm - 2 * mm
    bottom = 14 * mm
    available = top - bottom
    pages = []
    current_day = None
    current = []
    used = 0
    for spec in specs:
        day = spec[1]
        section_h = section_height(spec)
        if current and (day is not current_day or used + SECTION_GAP + section_h > available):
            pages.append((current_day, current))
            current = []
            used = 0
        if not current:
            current_day = day
        used += section_h if not current else SECTION_GAP + section_h
        current.append(spec)
    if current:
        pages.append((current_day, current))
    return pages


def draw_room_grid(c, rooms, events, top, size=CARD_FONT_SIZE):
    width, _ = landscape(A4)
    left = right = 8 * mm
    gap = 1.2 * mm
    col_width = (width - left - right - gap * (len(rooms) - 1)) / len(rooms)
    slots, row_heights = grid_layout(events, col_width, size)
    row_tops = []
    y = top
    for row_h in row_heights:
        row_tops.append(y)
        y -= row_h + 1.5 * mm

    for index, room in enumerate(rooms):
        x = left + index * (col_width + gap)
        c.setFillColor(TEAL)
        c.roundRect(x, top + 1.0 * mm, col_width, ROOM_HEADER_HEIGHT, 1.0 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("AALABold", 6.7 if len(rooms) >= 9 else 8.2)
        c.drawCentredString(x + col_width / 2, top + 3.6 * mm, clean(room))
        room_events = [event for event in events if event.get("room") == room]
        for slot_index, slot in enumerate(slots):
            active = [event for event in room_events if event["start"] <= slot < event["end"]]
            if active and active[0]["start"] != slot:
                continue
            if not active:
                continue
            event = active[0]
            covered = [
                i for i, candidate in enumerate(slots)
                if event["start"] <= candidate < event["end"]
            ]
            span_h = sum(row_heights[i] for i in covered) + 1.5 * mm * (len(covered) - 1)
            item, used = paragraph(event_markup(event), col_width - 3 * mm, size)
            fill, accent = category_colours(event)
            card_top = row_tops[slot_index]
            c.setFillColor(fill)
            c.setStrokeColor(RULE)
            c.roundRect(x, card_top - span_h, col_width, span_h, 1.0 * mm, fill=1, stroke=1)
            c.setFillColor(accent)
            c.rect(x, card_top - 1.0 * mm, col_width, 1.0 * mm, fill=1, stroke=0)
            item.drawOn(c, x + 1.5 * mm, card_top - used - 1.4 * mm)

    return grid_height(events, rooms, col_width, size)


def draw_section(c, spec, y):
    if spec[0] == "posters":
        return draw_poster_cards(c, spec[1], spec[2], y)

    _, day, rooms, events, part, parts = spec
    start = min(event["start"] for event in events)
    end = max(event["end"] for event in events)
    width, _ = landscape(A4)
    left = right = 8 * mm
    panel_width = width - left - right

    c.setFillColor(TEAL_PALE)
    c.setStrokeColor(RULE)
    c.roundRect(left, y - SECTION_LABEL_HEIGHT, panel_width, SECTION_LABEL_HEIGHT, 1.0 * mm, fill=1, stroke=1)
    c.setFillColor(MUTED)
    c.setFont("AALABold", 6.8)
    c.drawString(
        left + 2.0 * mm,
        y - 3.7 * mm,
        f"{start}-{end} | {len(rooms)} rooms | Part {part} of {parts}",
    )
    c.setFillColor(GOLD)
    c.rect(left, y - 0.8 * mm, panel_width, 0.8 * mm, fill=1, stroke=0)

    room_top = y - SECTION_LABEL_HEIGHT - LABEL_TO_ROOMS_GAP
    grid_top = room_top - ROOM_HEADER_HEIGHT - ROOMS_TO_GRID_GAP
    draw_room_grid(c, rooms, events, grid_top)
    _, grid_h, section_h = section_dimensions(rooms, events)
    return y - section_h


def draw_poster_cards(c, day, poster_band, top):
    """Draw poster details as five cards per row within the detail section."""
    _, card_width, card_gap, rows, section_height = poster_layout(poster_band)
    width, _ = landscape(A4)
    left = right = 8 * mm
    panel_width = width - left - right

    start = poster_band.get("presentationStart", poster_band["start"])
    end = poster_band.get("presentationEnd", poster_band["end"])
    label_height = SECTION_LABEL_HEIGHT
    c.setFillColor(TEAL_PALE)
    c.setStrokeColor(RULE)
    c.roundRect(left, top - label_height, panel_width, label_height, 1.0 * mm, fill=1, stroke=1)
    c.setFillColor(MUTED)
    c.setFont("AALABold", 6.8)
    c.drawString(
        left + 2.0 * mm,
        top - 3.7 * mm,
        f"{start}-{end} | Poster presentations | {clean(poster_band.get('room'))}",
    )
    c.setFillColor(GOLD)
    c.rect(left, top - 0.8 * mm, panel_width, 0.8 * mm, fill=1, stroke=0)

    grid_top = top - label_height - 1.4 * mm
    y = grid_top
    for cards, row_height in rows:
        for index, (event, item, used, _) in enumerate(cards):
            x = left + index * (card_width + card_gap)
            fill, accent = category_colours(event)
            c.setFillColor(fill)
            c.setStrokeColor(RULE)
            c.roundRect(x, y - row_height, card_width, row_height, 1.0 * mm, fill=1, stroke=1)
            c.setFillColor(accent)
            c.rect(x, y - 1.0 * mm, card_width, 1.0 * mm, fill=1, stroke=0)
            item.drawOn(c, x + 1.5 * mm, y - used - 2.0 * mm)
        y -= row_height + card_gap
    return top - section_height


def main():
    register_fonts()
    data = load_data()
    abbreviate_theme_labels(data)
    specs = detail_specs(data)
    pages = pack_specs(specs)
    total_pages = len(pages)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=landscape(A4), pageCompression=1)
    pdf.setTitle("AALA2026 Concurrent Session Details")
    pdf.setAuthor("Asian Association for Language Assessment")
    pdf.setSubject("Concurrent-session titles and authors by room and time")
    for page_number, (day, page_specs) in enumerate(pages, 1):
        header(
            pdf,
            "AALA2026 Concurrent Session Details",
            f"{day_label(day)} | Concurrent session details",
            page_number,
            total_pages,
        )
        _, height = landscape(A4)
        y = height - 32 * mm - 2 * mm
        for index, spec in enumerate(page_specs):
            if index:
                y -= SECTION_GAP
            y = draw_section(pdf, spec, y)
        pdf.showPage()
    pdf.save()
    print(OUTPUT)
    print(f"pages={total_pages}")


if __name__ == "__main__":
    main()
