"""Creates assets/resume.pdf from your details in resume_data.py.

Run:  python make_resume.py       (needs:  pip install reportlab)
Then run python build.py again so the "Download Resume" button appears on the site.
If you already have your own resume file, skip this and save it as assets/resume.pdf.
"""
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer

import resume_data as d

OUT = Path(__file__).parent / "assets" / "resume.pdf"
ACCENT = colors.HexColor("#9a6400")
INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#555555")

name = ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=INK, alignment=TA_LEFT)
role = ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=ACCENT)
small = ParagraphStyle("small", fontName="Helvetica", fontSize=9.5, leading=14, textColor=MUTED)
h = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=ACCENT, spaceBefore=12, spaceAfter=2)
body = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.5, textColor=INK)
item = ParagraphStyle("item", parent=body, fontName="Helvetica-Bold", spaceBefore=4)
detail = ParagraphStyle("detail", parent=small, fontSize=9.5)


def P(text, style):
    return Paragraph(text, style)


def heading(text):
    return [P(text, h), HRFlowable(width="100%", thickness=0.8, color=ACCENT, spaceAfter=4)]


def link(url, text):
    return f'<a href="{escape(url)}" color="#0b57d0">{escape(text)}</a>'


story = [P(escape(d.NAME), name), P(escape(d.ROLE), role), Spacer(1, 3)]
contact = [v for v in (d.EMAIL, d.PHONE, d.LOCATION) if v]
story.append(P(" &nbsp;|&nbsp; ".join(escape(c) for c in contact), small))
if d.SCHOOL:
    story.append(P(escape(d.SCHOOL), small))
PROFILE_URLS = {
    "Facebook": "https://www.facebook.com/{u}",
    "Instagram": "https://www.instagram.com/{u}/",
    "TikTok": "https://www.tiktok.com/@{u}",
}
profile_links = [
    link(url.format(u=d.SOCIALS[key.lower()].strip().lstrip("@")), key)
    for key, url in PROFILE_URLS.items()
    if d.SOCIALS.get(key.lower(), "").strip()
]
if profile_links:
    story.append(P(" &nbsp;|&nbsp; ".join(profile_links), small))

story += heading("About") + [P(escape(d.SUMMARY), body)]

story += heading("Education & Certificates")
for e in d.EDUCATION:
    block = [P(escape(e["title"]), item), P(escape(e["detail"]), detail)]
    if e.get("link"):
        block.append(P(link(e["link"], e.get("link_text", "View")), detail))
    story.append(KeepTogether(block))

if d.EXPERIENCE:
    story += heading("Experience")
    for e in d.EXPERIENCE:
        story.append(KeepTogether([P(escape(e["title"]), item), P(escape(e["detail"]), detail)]))

if d.PROJECTS:
    story += heading("Projects")
    for pr in d.PROJECTS:
        block = [P(escape(pr["title"]), item), P(escape(pr["desc"]), body)]
        if pr.get("link"):
            block.append(P(link(pr["link"], pr["link"]), detail))
        story.append(KeepTogether(block))

story += heading("Skills")
story.append(P(escape(", ".join(label for label, _ in d.TOOLS)), body))
if d.ROLES:
    story.append(P(escape(" | ".join(d.ROLES)), small))

OUT.parent.mkdir(exist_ok=True)
doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=16 * mm,
    title=f"{d.NAME} - Resume", author=d.NAME,
)
doc.build(story)
print(f"Created {OUT}")
