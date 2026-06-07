#!/usr/bin/env python3
"""Render RESEARCH.md into a brand-styled BEACON PDF (reportlab)."""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, ListFlowable,
    ListItem, Table, TableStyle, HRFlowable, KeepTogether, PageBreak, Flowable,
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

SRC = "RESEARCH.md"
OUT = "BEACON-research.pdf"

# ---- palette ----
PAPER   = HexColor("#f4efe4")
PAPER2  = HexColor("#efe8da")
INK     = HexColor("#1b1813")
INKSOFT = HexColor("#4f4a40")
INKFNT  = HexColor("#8a8276")
ACCENT  = HexColor("#9d4327")
RULE    = HexColor("#d9d0bf")

PAGE_W, PAGE_H = A4
MARGIN_X = 24 * mm
MARGIN_T = 22 * mm
MARGIN_B = 20 * mm

# ---- fonts: built-in Type1 (serif headings + grotesque body) ----
SERIF, SERIF_B = "Times-Roman", "Times-Bold"
SANS, SANS_B, SANS_I = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"
MONO = "Courier"

styles = getSampleStyleSheet()


def S(name, **kw):
    return ParagraphStyle(name, **kw)

body = S("body", fontName=SANS, fontSize=9.6, leading=15, textColor=INKSOFT,
         spaceAfter=7, alignment=TA_LEFT)
h1 = S("h1", fontName=SERIF_B, fontSize=19, leading=22, textColor=INK,
       spaceBefore=18, spaceAfter=9)
h2 = S("h2", fontName=SERIF_B, fontSize=14.5, leading=18, textColor=INK,
       spaceBefore=15, spaceAfter=6)
h3 = S("h3", fontName=SERIF_B, fontSize=11.5, leading=15, textColor=INK,
       spaceBefore=10, spaceAfter=3)
li = S("li", parent=body, spaceAfter=4, leading=14.5)
quote = S("quote", fontName=SANS, fontSize=9.3, leading=14.5, textColor=INK,
          spaceAfter=4)
label = S("label", fontName=SANS_B, fontSize=7.5, leading=10, textColor=ACCENT)
src = S("src", fontName=SANS, fontSize=8.6, leading=13, textColor=INKSOFT, spaceAfter=6)


def fmt(s):
    """Inline markdown -> reportlab mini-HTML, with WinAnsi-safe glyphs."""
    s = s.replace("→", "->").replace("↑", "^")
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"`([^`]+)`", r'<font face="%s" size=8.6>\1</font>' % MONO, s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", s)
    return s


# ---- beacon mark (drawn) ----
class Mark(Flowable):
    def __init__(self, size=18):
        super().__init__()
        self.size = size
        self.width = size
        self.height = size

    def draw(self):
        c = self.canv
        s = self.size
        cx = s * 0.5
        # light point
        c.setFillColor(ACCENT)
        c.circle(cx, s * 0.22, s * 0.09, stroke=0, fill=1)
        # two radiating arcs (upward)
        c.setStrokeColor(INK)
        c.setLineWidth(s * 0.07)
        c.setLineCap(1)
        for r in (s * 0.30, s * 0.46):
            c.arc(cx - r, s * 0.30 - r, cx + r, s * 0.30 + r, startAng=35, extent=110)


def cover():
    """Return flowables for the cover."""
    fl = []
    fl.append(Spacer(1, 40 * mm))
    # mark + wordmark lockup
    lock = Table(
        [[Mark(20), Paragraph('<font name="%s" size=20>BEACON</font>' % SERIF_B,
                              S("wm", textColor=INK))]],
        colWidths=[24, 120],
    )
    lock.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    fl.append(lock)
    fl.append(Spacer(1, 14 * mm))
    fl.append(Paragraph("RESEARCH", label))
    fl.append(Spacer(1, 3 * mm))
    fl.append(Paragraph(
        "Cross-border VAT for commerce SMEs",
        S("ctitle", fontName=SERIF_B, fontSize=30, leading=34, textColor=INK)))
    fl.append(Spacer(1, 5 * mm))
    fl.append(Paragraph(
        "Competition, the real tax process, why it&rsquo;s a mess, and the white "
        "space &mdash; for a Netherlands-based business expanding into Germany "
        "and Belgium.",
        S("csub", fontName=SANS, fontSize=11, leading=16, textColor=INKSOFT)))
    fl.append(Spacer(1, 10 * mm))
    fl.append(HRFlowable(width="36%", thickness=1.4, color=ACCENT,
                         spaceBefore=0, spaceAfter=6, hAlign="LEFT"))
    fl.append(Paragraph("Prepared June 2026 &middot; wedge for the SME growth &amp; "
                        "expansion platform", S("cmeta", fontName=SANS, fontSize=9,
                                                leading=13, textColor=INKFNT)))
    fl.append(PageBreak())
    return fl


def parse(md):
    fl = []
    lines = md.split("\n")
    i = 0
    # drop everything up to and including the first H1 (used on cover)
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    if i < len(lines):
        i += 1

    def flush_para(buf):
        if buf:
            fl.append(Paragraph(fmt(" ".join(buf)), body))
        return []

    para = []
    while i < len(lines):
        ln = lines[i].rstrip()
        st = ln.strip()

        if not st:
            para = flush_para(para)
            i += 1
            continue

        if st == "---":
            para = flush_para(para)
            fl.append(Spacer(1, 2))
            fl.append(HRFlowable(width="100%", thickness=0.6, color=RULE,
                                 spaceBefore=4, spaceAfter=8))
            i += 1
            continue

        if ln.startswith("### "):
            para = flush_para(para)
            fl.append(Paragraph(fmt(ln[4:]), h3))
            i += 1
            continue
        if ln.startswith("## "):
            para = flush_para(para)
            fl.append(Paragraph(fmt(ln[3:]), h2))
            i += 1
            continue
        if ln.startswith("# "):
            para = flush_para(para)
            fl.append(Paragraph(fmt(ln[2:]), h1))
            i += 1
            continue

        # blockquote (may contain a numbered list)
        if st.startswith(">"):
            para = flush_para(para)
            q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner = []
            for ql in q:
                if not ql.strip():
                    continue
                m = re.match(r"^(\d+)\.\s+(.*)$", ql.strip())
                if m:
                    inner.append(Paragraph(
                        '<font color="#9d4327"><b>%s.</b></font>&nbsp;%s'
                        % (m.group(1), fmt(m.group(2))),
                        S("qi", parent=quote, leftIndent=12, firstLineIndent=-12)))
                else:
                    inner.append(Paragraph(fmt(ql.strip()), quote))
            box = Table([[inner]], colWidths=[PAGE_W - 2 * MARGIN_X])
            box.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), PAPER2),
                ("LINEBEFORE", (0, 0), (0, -1), 2, ACCENT),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]))
            fl.append(box)
            fl.append(Spacer(1, 7))
            continue

        # bullet list
        if re.match(r"^\s*-\s+", ln):
            para = flush_para(para)
            items = []
            while i < len(lines) and re.match(r"^\s*-\s+", lines[i]):
                txt = re.sub(r"^\s*-\s+", "", lines[i])
                items.append(ListItem(Paragraph(fmt(txt), li),
                                      value=None, leftIndent=14))
                i += 1
            fl.append(ListFlowable(items, bulletType="bullet", start="•",
                                   bulletColor=ACCENT, bulletFontSize=7,
                                   leftIndent=12, bulletOffsetY=1))
            fl.append(Spacer(1, 4))
            continue

        # numbered list
        if re.match(r"^\s*\d+\.\s+", ln):
            para = flush_para(para)
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                txt = re.sub(r"^\s*\d+\.\s+", "", lines[i])
                items.append(ListItem(Paragraph(fmt(txt), li), leftIndent=16))
                i += 1
            fl.append(ListFlowable(items, bulletType="1", bulletColor=ACCENT,
                                   bulletFontName=SANS_B, bulletFontSize=9,
                                   leftIndent=14))
            fl.append(Spacer(1, 4))
            continue

        # sources section: lines like "**Label:** text"
        if st.startswith("**") and st.count("**") >= 2 and ":" in st:
            para = flush_para(para)
            fl.append(Paragraph(fmt(st), src))
            i += 1
            continue

        para.append(st)
        i += 1

    flush_para(para)
    return fl


def on_page(canvas, doc):
    canvas.saveState()
    # paper background
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # footer rule + text
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN_X, MARGIN_B - 6, PAGE_W - MARGIN_X, MARGIN_B - 6)
    canvas.setFont(SANS, 7.5)
    canvas.setFillColor(INKFNT)
    canvas.drawString(MARGIN_X, MARGIN_B - 14, "BEACON — cross-border VAT research")
    canvas.drawRightString(PAGE_W - MARGIN_X, MARGIN_B - 14, "%d" % doc.page)
    canvas.restoreState()


def build():
    with open(SRC, encoding="utf-8") as f:
        md = f.read()
    doc = BaseDocTemplate(
        OUT, pagesize=A4,
        leftMargin=MARGIN_X, rightMargin=MARGIN_X,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title="BEACON — Cross-border VAT research", author="BEACON",
    )
    frame = Frame(MARGIN_X, MARGIN_B, PAGE_W - 2 * MARGIN_X,
                  PAGE_H - MARGIN_T - MARGIN_B, id="main",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=on_page)])
    story = cover() + parse(md)
    doc.build(story)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
