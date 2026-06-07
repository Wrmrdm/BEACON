#!/usr/bin/env python3
"""Render a Markdown doc into a brand-styled BEACON PDF (reportlab).

Usage:
    python3 build_pdf.py [SRC.md] [OUT.pdf] [EYEBROW] [TITLE] [SUBTITLE]
Defaults render RESEARCH.md.
"""
import re
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, ListFlowable,
    ListItem, Table, TableStyle, HRFlowable, PageBreak, Flowable,
)
from reportlab.lib.styles import ParagraphStyle

# ---- args ----
SRC      = sys.argv[1] if len(sys.argv) > 1 else "RESEARCH.md"
OUT      = sys.argv[2] if len(sys.argv) > 2 else "BEACON-research.pdf"
EYEBROW  = sys.argv[3] if len(sys.argv) > 3 else "RESEARCH"
TITLE    = sys.argv[4] if len(sys.argv) > 4 else "Cross-border VAT for commerce SMEs"
SUBTITLE = sys.argv[5] if len(sys.argv) > 5 else (
    "Competition, the real tax process, why it&rsquo;s a mess, and the white "
    "space &mdash; for a Netherlands-based business expanding into Germany and Belgium.")
FOOTER   = "BEACON — " + EYEBROW.lower()

# ---- palette ----
PAPER, PAPER2 = HexColor("#f4efe4"), HexColor("#efe8da")
INK, INKSOFT, INKFNT = HexColor("#1b1813"), HexColor("#4f4a40"), HexColor("#8a8276")
ACCENT, RULE = HexColor("#9d4327"), HexColor("#d9d0bf")
OK = HexColor("#4f6b52")

PAGE_W, PAGE_H = A4
MARGIN_X, MARGIN_T, MARGIN_B = 22 * mm, 22 * mm, 20 * mm

SERIF, SERIF_B = "Times-Roman", "Times-Bold"
SANS, SANS_B, SANS_I = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"
MONO = "Courier"


def Sty(name, **kw):
    return ParagraphStyle(name, **kw)


body = Sty("body", fontName=SANS, fontSize=9.6, leading=15, textColor=INKSOFT, spaceAfter=7)
h1 = Sty("h1", fontName=SERIF_B, fontSize=18, leading=21, textColor=INK, spaceBefore=16, spaceAfter=8)
h2 = Sty("h2", fontName=SERIF_B, fontSize=14, leading=17, textColor=INK, spaceBefore=15, spaceAfter=6)
h3 = Sty("h3", fontName=SERIF_B, fontSize=11.5, leading=15, textColor=INK, spaceBefore=10, spaceAfter=3)
li = Sty("li", parent=body, spaceAfter=4, leading=14.5)
quote = Sty("quote", fontName=SANS, fontSize=9.3, leading=14.5, textColor=INK, spaceAfter=4)
label = Sty("label", fontName=SANS_B, fontSize=7.5, leading=10, textColor=ACCENT)
src = Sty("src", fontName=SANS, fontSize=8.4, leading=12.5, textColor=INKSOFT, spaceAfter=6)
th = Sty("th", fontName=SANS_B, fontSize=7.2, leading=9, textColor=INK)
td = Sty("td", fontName=SANS, fontSize=7.2, leading=9.2, textColor=INKSOFT)


def fmt(s):
    """Inline markdown -> reportlab mini-HTML; WinAnsi-safe glyphs + status words."""
    s = s.replace("→", "->").replace("↑", "^").replace("️", "")
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"`([^`]+)`", r'<font face="%s" size=8>\1</font>' % MONO, s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", s)
    # status emoji -> coloured words (built-in fonts can't render emoji)
    s = s.replace("✅", '<font color="#4f6b52"><b>Yes</b></font>')
    s = s.replace("❌", '<font color="#9d4327"><b>No</b></font>')
    s = s.replace("🟡", '<font color="#9d4327"><b>Partly</b></font>')
    s = s.replace("⚠", '<font color="#9d4327"><b>!</b></font>')
    return s


class Mark(Flowable):
    def __init__(self, size=20):
        super().__init__(); self.size = self.width = self.height = size

    def draw(self):
        c, s = self.canv, self.size
        cx = s * 0.5
        c.setFillColor(ACCENT); c.circle(cx, s * 0.22, s * 0.09, stroke=0, fill=1)
        c.setStrokeColor(INK); c.setLineWidth(s * 0.07); c.setLineCap(1)
        for r in (s * 0.30, s * 0.46):
            c.arc(cx - r, s * 0.30 - r, cx + r, s * 0.30 + r, startAng=35, extent=110)


def cover():
    fl = [Spacer(1, 38 * mm)]
    lock = Table([[Mark(20), Paragraph('<font name="%s" size=20>BEACON</font>' % SERIF_B,
                                       Sty("wm", textColor=INK))]], colWidths=[24, 130])
    lock.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    fl += [lock, Spacer(1, 13 * mm), Paragraph(EYEBROW, label), Spacer(1, 3 * mm),
           Paragraph(TITLE, Sty("ct", fontName=SERIF_B, fontSize=29, leading=33, textColor=INK)),
           Spacer(1, 5 * mm),
           Paragraph(SUBTITLE, Sty("cs", fontName=SANS, fontSize=11, leading=16, textColor=INKSOFT)),
           Spacer(1, 9 * mm),
           HRFlowable(width="36%", thickness=1.4, color=ACCENT, spaceAfter=6, hAlign="LEFT"),
           Paragraph("Prepared June 2026 &middot; engineering &amp; product research, not legal advice",
                     Sty("cm", fontName=SANS, fontSize=9, leading=13, textColor=INKFNT)),
           PageBreak()]
    return fl


def make_table(rows):
    header, data = rows[0], rows[1:]
    n = len(header)
    cw = PAGE_W - 2 * MARGIN_X
    widths = [cw / n] * n
    cells = [[Paragraph(fmt(c), th) for c in header]]
    for r in data:
        r = (r + [""] * n)[:n]
        cells.append([Paragraph(fmt(c), td) for c in r])
    t = Table(cells, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PAPER2),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, ACCENT),
        ("LINEBELOW", (0, 1), (-1, -2), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def is_table_row(s):
    return s.startswith("|") and s.count("|") >= 2


def is_sep_row(s):
    return is_table_row(s) and set(s.replace("|", "").replace("-", "").replace(":", "").strip()) == set()


def split_row(s):
    return [c.strip() for c in s.strip().strip("|").split("|")]


def parse(md):
    fl, lines, i = [], md.split("\n"), 0
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    i += 1
    para = []

    def flush():
        nonlocal para
        if para:
            fl.append(Paragraph(fmt(" ".join(para)), body)); para = []

    while i < len(lines):
        ln = lines[i].rstrip(); st = ln.strip()
        if not st:
            flush(); i += 1; continue

        # table
        if is_table_row(st):
            flush(); rows = []
            while i < len(lines) and is_table_row(lines[i].strip()):
                if not is_sep_row(lines[i].strip()):
                    rows.append(split_row(lines[i]))
                i += 1
            if rows:
                fl.append(Spacer(1, 2)); fl.append(make_table(rows)); fl.append(Spacer(1, 9))
            continue

        if st == "---":
            flush(); fl.append(HRFlowable(width="100%", thickness=0.6, color=RULE,
                                          spaceBefore=4, spaceAfter=8)); i += 1; continue
        if ln.startswith("### "):
            flush(); fl.append(Paragraph(fmt(ln[4:]), h3)); i += 1; continue
        if ln.startswith("## "):
            flush(); fl.append(Paragraph(fmt(ln[3:]), h2)); i += 1; continue
        if ln.startswith("# "):
            flush(); fl.append(Paragraph(fmt(ln[2:]), h1)); i += 1; continue

        # blockquote
        if st.startswith(">"):
            flush(); q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
            inner = []
            for ql in q:
                if ql.strip():
                    inner.append(Paragraph(fmt(ql.strip()), quote))
            box = Table([[inner]], colWidths=[PAGE_W - 2 * MARGIN_X])
            box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PAPER2),
                                     ("LINEBEFORE", (0, 0), (0, -1), 2, ACCENT),
                                     ("LEFTPADDING", (0, 0), (-1, -1), 12),
                                     ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                                     ("TOPPADDING", (0, 0), (-1, -1), 9),
                                     ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
            fl.append(box); fl.append(Spacer(1, 7)); continue

        # bullet list
        if re.match(r"^\s*-\s+", ln):
            flush(); items = []
            while i < len(lines) and re.match(r"^\s*-\s+", lines[i]):
                items.append(ListItem(Paragraph(fmt(re.sub(r"^\s*-\s+", "", lines[i])), li),
                                      leftIndent=14)); i += 1
            fl.append(ListFlowable(items, bulletType="bullet", start="•", bulletColor=ACCENT,
                                   bulletFontSize=7, leftIndent=12, bulletOffsetY=1))
            fl.append(Spacer(1, 4)); continue

        # numbered list
        if re.match(r"^\s*\d+\.\s+", ln):
            flush(); items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(ListItem(Paragraph(fmt(re.sub(r"^\s*\d+\.\s+", "", lines[i])), li),
                                      leftIndent=16)); i += 1
            fl.append(ListFlowable(items, bulletType="1", bulletColor=ACCENT,
                                   bulletFontName=SANS_B, bulletFontSize=9, leftIndent=14))
            fl.append(Spacer(1, 4)); continue

        if st.startswith("**") and st.count("**") >= 2 and ":" in st:
            flush(); fl.append(Paragraph(fmt(st), src)); i += 1; continue

        para.append(st); i += 1

    flush()
    return fl


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER); canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setStrokeColor(RULE); canvas.setLineWidth(0.6)
    canvas.line(MARGIN_X, MARGIN_B - 6, PAGE_W - MARGIN_X, MARGIN_B - 6)
    canvas.setFont(SANS, 7.5); canvas.setFillColor(INKFNT)
    canvas.drawString(MARGIN_X, MARGIN_B - 14, FOOTER)
    canvas.drawRightString(PAGE_W - MARGIN_X, MARGIN_B - 14, "%d" % doc.page)
    canvas.restoreState()


def build():
    with open(SRC, encoding="utf-8") as f:
        md = f.read()
    doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                          topMargin=MARGIN_T, bottomMargin=MARGIN_B, title=TITLE, author="BEACON")
    frame = Frame(MARGIN_X, MARGIN_B, PAGE_W - 2 * MARGIN_X, PAGE_H - MARGIN_T - MARGIN_B,
                  id="main", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=on_page)])
    doc.build(cover() + parse(md))
    print("wrote", OUT)


if __name__ == "__main__":
    build()
