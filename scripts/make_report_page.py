"""Convert report_v8.md into the Jekyll page _pages/report-ai-perception.md.

Mechanical only: the prose is copied verbatim from the assembled report so the web
version cannot drift from the PDF. What changes:
  1. pandoc YAML front matter  -> Jekyll front matter + a title/download header block
  2. ![](figs_v5/x.png){width=} -> site image path + a kramdown IAL class
  3. exhibit caption paragraph  -> tagged with .report-caption
  4. blockquote "\" hard break  -> a blank quoted line (two paragraphs in the quote)
  5. a citation footer appended
Footnotes ([^n]) are left alone: kramdown collects them and renders an endnote
list with back-links at the bottom of the page.
"""
import re

SRC = ("/Users/hangyu/Library/CloudStorage/Dropbox/Topic Explore/AI diffusion impact/"
       "mywork/pilot_analysis/report/report_v8.md")
DST = ("/Users/hangyu/Library/CloudStorage/Dropbox/_professional documents/website/"
       "_pages/report-ai-perception.md")
IMGBASE = "/images/reports/ai-perception"

FRONT = """---
permalink: /reports/ai-perception/
title: "Perceived Exposure: A Pilot Report"
excerpt: "What young people in China expect AI to do to their jobs. A pilot survey of 500 graduating students and 500 workers, July 2026."
author_profile: true
body_class: report-page
---

<p class="report-subtitle">What young people in China expect AI to do to their jobs</p>

<p class="report-byline">Hang Yu · September 2026</p>

<p class="report-downloads">
  <a href="/files/reports/2026-ai-perception.pdf" class="cv-btn">Report (PDF)</a>
  <a href="/files/reports/2026-ai-perception-appendix.pdf" class="cv-btn cv-btn-secondary">Appendix (PDF)</a>
</p>

<p class="report-note">The appendix carries the question wording, sample composition and cleaning rules, the full belief–behavior matrix, robustness checks, and the comparison surveys.</p>

"""

# The web figures are redrawn (scripts/make_web_exhibits.py) with a different, validated
# palette, so the colour words the print captions use must be corrected to match what the
# reader actually sees. These are the ONLY wording changes made to the report's prose.
CAPTION_FIXES = [
    ("for students (orange) and workers (grey)",
     "for students (orange) and workers (blue)"),
    ("to rise (solid) or fall (hatched)",
     "to rise (blue) or fall (red)"),
    ("moved toward AI-related work (blue) and away from AI-exposed work (dark red)",
     "moved toward AI-related work (blue) and away from AI-exposed work (red)"),
]

FOOTER = """

---

<p class="report-cite"><strong>Suggested citation.</strong> Hang Yu, &ldquo;Perceived Exposure: A Pilot Report — What Young People in China Expect AI to Do to Their Jobs,&rdquo; September 2026, https://econhangyu.com/reports/ai-perception/.</p>

<p class="report-notes-label">Notes</p>
"""


def main():
    text = open(SRC, encoding="utf-8").read()

    # 1. strip the pandoc YAML block (the report's own title/subtitle/author/date)
    text = re.sub(r"\A---\n.*?\n---\n+", "", text, flags=re.S)

    # 2. figures -> the web-rendered SVGs (scripts/make_web_exhibits.py), tagged for CSS
    text = re.sub(
        r"!\[\]\(figs_v5/([A-Za-z0-9_]+)\.png\)\{width=[^}]*\}",
        lambda m: f"![]({IMGBASE}/{m.group(1)}.svg)\n{{: .report-figure}}",
        text,
    )

    # 3. the caption paragraph that follows each figure
    text = re.sub(
        r"^(\*\*Exhibit \d+:.*?)$",
        lambda m: m.group(1) + "\n{: .report-caption}",
        text,
        flags=re.M,
    )

    # 4. pandoc's backslash hard break inside the pull quotes
    text = text.replace("\\\n> — ", "\n>\n> — ")

    # 5. make the captions' colour words describe the redrawn web figures
    for old, new in CAPTION_FIXES:
        if old not in text:
            raise SystemExit(f"caption fix no longer matches the source: {old!r}")
        text = text.replace(old, new)

    out = FRONT + text.strip() + FOOTER
    open(DST, "w", encoding="utf-8").write(out)

    print("wrote", DST)
    print("figures tagged:", out.count("{: .report-figure}"))
    print("captions tagged:", out.count("{: .report-caption}"))
    print("footnote refs:", len(re.findall(r"\[\^\d+\](?!:)", out)),
          " defs:", len(re.findall(r"^\[\^\d+\]:", out, flags=re.M)))
    leftover = re.findall(r"figs_v5|\{width=|\\\n", out)
    print("leftover pandoc artifacts:", leftover or "none")


if __name__ == "__main__":
    main()
