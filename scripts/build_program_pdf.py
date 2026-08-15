#!/usr/bin/env python3
"""Build the four-page landscape AALA 2026 detailed programme PDF."""

import argparse
import json
import re
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A1, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


PAPER = colors.HexColor("#FCF9F1")
PAPER_RAISED = colors.HexColor("#FFFDF8")
PAPER_SOFT = colors.HexColor("#F2EEE4")
INK = colors.HexColor("#26384E")
INK_SOFT = colors.HexColor("#566575")
RULE = colors.HexColor("#CFC7B8")
TEAL = colors.HexColor("#167F7A")
TEAL_DARK = colors.HexColor("#0E625F")
WHITE = colors.HexColor("#FFFFFF")

CATEGORY_COLORS = {
    "theme-1": colors.HexColor("#C45F4A"),
    "theme-2": colors.HexColor("#A97919"),
    "theme-3": colors.HexColor("#36845D"),
    "theme-4": colors.HexColor("#476EB5"),
    "featured": colors.HexColor("#8B4CA1"),
    "poster": colors.HexColor("#248E91"),
    "symposium": colors.HexColor("#B64B61"),
    "plenary": colors.HexColor("#287240"),
    "workshop": colors.HexColor("#A56B22"),
    "ceremony": colors.HexColor("#4C527F"),
    "break": colors.HexColor("#648294"),
    "other": colors.HexColor("#667182"),
}

ROOMS_BY_DAY = {
    "sep18": ["Culture Centre Room 1", "Culture Centre Room 2", "HG01"],
    "sep19": ["HG01", "HG02", "HG03", "L205", "L206", "L207", "L305", "L306", "L307", "Poster area"],
    "sep20": ["HG01", "HG02", "HG03", "L205", "L206", "L207", "L305", "L306", "Poster area"],
    "sep21": ["Culture Centre Room 1"],
}

SHARED_CATEGORIES = {"break", "plenary", "ceremony"}


def register_fonts():
    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("ProgramRegular", font_dir / "Arial.ttf"))
    pdfmetrics.registerFont(TTFont("ProgramBold", font_dir / "Arial Bold.ttf"))
    pdfmetrics.registerFont(TTFont("ProgramItalic", font_dir / "Arial Italic.ttf"))
    pdfmetrics.registerFont(TTFont("ProgramBoldItalic", font_dir / "Arial Bold Italic.ttf"))
    pdfmetrics.registerFontFamily(
        "ProgramRegular",
        normal="ProgramRegular",
        bold="ProgramBold",
        italic="ProgramItalic",
        boldItalic="ProgramBoldItalic",
    )


def load_program(path):
    source = Path(path).read_text(encoding="utf-8")
    match = re.fullmatch(r"\s*window\.AALA_PROGRAM\s*=\s*(\{.*\});\s*", source, re.S)
    if not match:
        raise ValueError(f"Could not read programme data from {path}")
    return json.loads(match.group(1))


def clean(value):
    text = str(value or "")
    replacements = {
        "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-",
        "\u2014": "-", "\u2212": "-", "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text).strip()


def xml(value):
    return escape(clean(value), quote=True)


def minutes(value):
    hour, minute = map(int, value.split(":"))
    return hour * 60 + minute


def time_label(total_minutes):
    return f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"


def authors_line(event):
    authors = []
    for author in event.get("authors", []):
        affiliation = clean(author.get("affiliation"))
        label = clean(author.get("name"))
        if affiliation:
            label += f" ({affiliation})"
        if label:
            authors.append(label)
    return "; ".join(authors)


def fit_paragraph(markup, width, height, sizes, *, alignment=TA_LEFT, color=INK, leading_ratio=1.12):
    last = None
    for font_size in sizes:
        style = ParagraphStyle(
            f"fit-{font_size}-{alignment}",
            fontName="ProgramRegular",
            fontSize=font_size,
            leading=font_size * leading_ratio,
            textColor=color,
            alignment=alignment,
            allowWidows=0,
            allowOrphans=0,
            splitLongWords=True,
        )
        paragraph = Paragraph(markup, style)
        _, used_height = paragraph.wrap(width, height)
        last = (paragraph, used_height)
        if used_height <= height:
            return paragraph, used_height
    return last


def event_markup(event, *, show_meta=True, compact=False):
    parts = []
    if show_meta:
        meta = f"{xml(event.get('categoryLabel'))} | {xml(event.get('start'))}-{xml(event.get('end'))}"
        if event.get("room"):
            meta += f" | <b><i>Venue: {xml(event.get('room'))}</i></b>"
        parts.append(f'<font color="{INK_SOFT.hexval()}">{meta}</font>')
    if event.get("id"):
        parts.append(f"<i>{xml(event.get('id'))}</i>")
    parts.append(f"<b>{xml(event.get('title'))}</b>")
    if event.get("note"):
        parts.append(f"<b>{xml(event.get('note'))}</b>")
    author_text = authors_line(event)
    if author_text:
        parts.append(xml(author_text))
    spacer = "<br/>" if compact else '<br/><font size="1"> </font><br/>'
    return spacer.join(parts)


def draw_fitted(c, markup, x, y, width, height, sizes, *, alignment=TA_LEFT, color=INK, padding=1.5 * mm):
    inner_width = max(1, width - 2 * padding)
    inner_height = max(1, height - 2 * padding)
    paragraph, used_height = fit_paragraph(markup, inner_width, inner_height, sizes, alignment=alignment, color=color)
    paragraph.drawOn(c, x + padding, y + height - padding - used_height)


def draw_event(c, event, x, y, width, height, *, shared=False, compact=False):
    category = event.get("category", "other")
    accent = CATEGORY_COLORS.get(category, CATEGORY_COLORS["other"])
    c.setFillColor(PAPER_RAISED if not shared else PAPER_SOFT)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.45)
    c.rect(x, y, width, height, fill=1, stroke=1)
    c.setFillColor(accent)
    stripe = 2.0 * mm if width > 35 * mm else 1.3 * mm
    c.rect(x, y + height - stripe, width, stripe, fill=1, stroke=0)
    markup = event_markup(event, show_meta=shared, compact=compact)
    if shared:
        sizes = [10, 9, 8, 7, 6]
        align = TA_CENTER
        padding = 2.1 * mm
    elif compact:
        sizes = [6.2, 5.8, 5.4, 5.0, 4.6, 4.2]
        align = TA_LEFT
        padding = 1.2 * mm
    else:
        sizes = [7.2, 6.8, 6.4, 6.0, 5.6, 5.2, 4.8]
        align = TA_LEFT
        padding = 1.5 * mm
    draw_fitted(c, markup, x, y, width, height - stripe, sizes, alignment=align, padding=padding)


def draw_shared_events(c, events, x, y, width, height):
    if len(events) == 1:
        draw_event(c, events[0], x, y, width, height, shared=True)
        return
    gap = 1.2 * mm
    item_width = (width - gap * (len(events) - 1)) / len(events)
    for index, event in enumerate(events):
        draw_event(c, event, x + index * (item_width + gap), y, item_width, height, shared=True)


def draw_poster_column(c, event, x, y, width, height):
    posters = event.get("posters", [])
    if not posters:
        return
    header_height = 8 * mm
    c.setFillColor(CATEGORY_COLORS["poster"])
    c.setStrokeColor(RULE)
    c.rect(x, y + height - header_height, width, header_height, fill=1, stroke=1)
    draw_fitted(
        c,
        "<b>Poster presentations</b>",
        x,
        y + height - header_height,
        width,
        header_height,
        [7.2, 6.5],
        alignment=TA_CENTER,
        color=WHITE,
        padding=1.2 * mm,
    )
    item_height = (height - header_height) / len(posters)
    for index, poster in enumerate(posters):
        item_y = y + height - header_height - (index + 1) * item_height
        draw_event(c, poster, x, item_y, width, item_height, compact=True)


def day_bounds(day):
    starts = [minutes(event["start"]) for event in day["events"]]
    ends = [minutes(event["end"]) for event in day["events"]]
    return min(starts), max(ends)


def is_shared(event, rooms):
    if event.get("posters"):
        return False
    if len(rooms) == 1:
        return True
    if event.get("category") in SHARED_CATEGORIES:
        return True
    return event.get("room") not in rooms


def draw_legend(c, entries, right_x, top_y, max_width):
    c.setFont("ProgramRegular", 6.7)
    widths = []
    for entry in entries:
        widths.append(4 * mm + pdfmetrics.stringWidth(clean(entry["label"]), "ProgramRegular", 6.7) + 4 * mm)
    total = min(max_width, sum(widths))
    x = right_x - total
    for entry, width in zip(entries, widths):
        if x + width > right_x:
            break
        c.setFillColor(CATEGORY_COLORS.get(entry["key"], CATEGORY_COLORS["other"]))
        c.circle(x + 1.5 * mm, top_y - 1.5 * mm, 1.35 * mm, fill=1, stroke=0)
        c.setFillColor(INK)
        c.drawString(x + 4 * mm, top_y - 2.5 * mm, clean(entry["label"]))
        x += width


def draw_day(c, data, day, page_number, page_size):
    page_width, page_height = page_size
    left = 12 * mm
    right = 12 * mm
    top = 11 * mm
    bottom = 12 * mm
    time_width = 18 * mm
    header_height = 25 * mm
    room_header_height = 13 * mm
    footer_height = 8 * mm

    c.setFillColor(PAPER)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    title_y = page_height - top
    c.setFillColor(TEAL_DARK)
    c.setFont("ProgramBold", 18)
    c.drawString(left, title_y - 5 * mm, "AALA 2026 Detailed Programme")
    c.setFillColor(INK)
    c.setFont("ProgramBold", 12)
    c.drawString(left, title_y - 12 * mm, f"{clean(day['weekday'])}, {clean(day['date'])} 2026")
    c.setFillColor(INK_SOFT)
    c.setFont("ProgramRegular", 7.5)
    c.drawString(left, title_y - 18 * mm, clean(day["subtitle"]))
    draw_legend(c, data["legend"], page_width - right, title_y - 5 * mm, page_width * 0.57)

    rooms = ROOMS_BY_DAY[day["key"]]
    poster_index = rooms.index("Poster area") if "Poster area" in rooms else None
    main_room_count = poster_index if poster_index is not None else len(rooms)
    grid_left = left + time_width
    grid_width = page_width - left - right - time_width
    column_width = grid_width / len(rooms)
    grid_top = page_height - top - header_height - room_header_height
    grid_bottom_limit = bottom + footer_height
    start_time, end_time = day_bounds(day)
    slot_count = (end_time - start_time) // 30
    available_height = grid_top - grid_bottom_limit
    row_height = min(38 * mm, available_height / slot_count)
    grid_height = row_height * slot_count
    grid_bottom = grid_top - grid_height

    c.setFillColor(TEAL_DARK)
    c.rect(left, grid_top, time_width, room_header_height, fill=1, stroke=0)
    draw_fitted(c, "<b>Time</b>", left, grid_top, time_width, room_header_height, [8], alignment=TA_CENTER, color=WHITE)
    for index, room in enumerate(rooms):
        x = grid_left + index * column_width
        fill = CATEGORY_COLORS["poster"] if room == "Poster area" else TEAL_DARK
        c.setFillColor(fill)
        c.setStrokeColor(PAPER)
        c.rect(x, grid_top, column_width, room_header_height, fill=1, stroke=1)
        draw_fitted(c, f"<b>{xml(room)}</b>", x, grid_top, column_width, room_header_height, [8, 7.2, 6.5], alignment=TA_CENTER, color=WHITE)

    c.setStrokeColor(RULE)
    c.setLineWidth(0.35)
    for slot in range(slot_count + 1):
        y = grid_top - slot * row_height
        c.line(left, y, page_width - right, y)
        if slot < slot_count:
            c.setFillColor(INK_SOFT)
            c.setFont("ProgramBold" if slot % 2 == 0 else "ProgramRegular", 7)
            c.drawRightString(left + time_width - 2 * mm, y - 4.2 * mm, time_label(start_time + slot * 30))
    for index in range(len(rooms) + 1):
        x = grid_left + index * column_width
        c.line(x, grid_bottom, x, grid_top)
    c.line(left, grid_bottom, left, grid_top)

    def y_for(value):
        return grid_top - ((minutes(value) - start_time) / 30) * row_height

    poster_event = next((event for event in day["events"] if event.get("posters")), None)
    if poster_event and poster_index is not None:
        poster_x = grid_left + poster_index * column_width
        poster_top = y_for(poster_event["start"])
        poster_bottom = y_for(poster_event["end"])
        draw_poster_column(c, poster_event, poster_x, poster_bottom, column_width, poster_top - poster_bottom)

    shared_groups = {}
    room_events = []
    for event in day["events"]:
        if event.get("posters"):
            continue
        if is_shared(event, rooms):
            shared_groups.setdefault(event["start"], []).append(event)
        else:
            room_events.append(event)

    shared_width = column_width * main_room_count
    for start, events in shared_groups.items():
        end = max(events, key=lambda event: minutes(event["end"]))["end"]
        top_y = y_for(start)
        bottom_y = y_for(end)
        draw_shared_events(c, events, grid_left, bottom_y, shared_width, top_y - bottom_y)

    for event in room_events:
        room_index = rooms.index(event["room"])
        x = grid_left + room_index * column_width
        top_y = y_for(event["start"])
        bottom_y = y_for(event["end"])
        draw_event(c, event, x, bottom_y, column_width, top_y - bottom_y)

    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(left, 8 * mm, page_width - right, 8 * mm)
    c.setFillColor(INK_SOFT)
    c.setFont("ProgramRegular", 7)
    c.drawString(left, 4.5 * mm, "AALA 2026 | University of Macau | Titles, submission IDs, authors and affiliations")
    c.drawRightString(page_width - right, 4.5 * mm, f"Page {page_number} of {len(data['days'])}")
    c.showPage()


def build(data_path, output_path):
    register_fonts()
    data = load_program(data_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    page_size = landscape(A1)
    pdf = canvas.Canvas(str(output), pagesize=page_size, pageCompression=1)
    pdf.setTitle("AALA 2026 Detailed Programme")
    pdf.setAuthor("Asian Association for Language Assessment")
    pdf.setSubject("Four-day landscape conference timetable")
    for page_number, day in enumerate(data["days"], 1):
        draw_day(pdf, data, day, page_number, page_size)
    pdf.save()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", nargs="?", default="program-data.js")
    parser.add_argument("output", nargs="?", default="output/pdf/AALA2026-detailed-programme.pdf")
    args = parser.parse_args()
    build(args.data, args.output)
    print(args.output)


if __name__ == "__main__":
    main()
