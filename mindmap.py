"""
The syllabus map — the app's front page.

Five subject boxes, each holding that subject's **real Cambridge chapters**.
Every chapter title here was verified verbatim against the syllabus PDFs in
resources/ — nothing is paraphrased and nothing is invented.

Chapters carrying a genuine Islamic thread are highlighted and name the scholar.
The rest are left plain: they are on the syllabus, they are not on the heritage
map, and pretending otherwise is the failure the whole project exists to avoid.

Lineage transcribed by hand from Miraath-al-Hikma_Heritage-Topics.md —
curation, not generation (algorism-code-spine.md §5).
"""

from xml.sax.saxutils import escape

DIRECT, PRECURSOR, NONE = "direct", "precursor", None

# (chapter, scholar, mark, lesson_key)
SUBJECTS = [
    ("Mathematics", "0580", "#6a4bc0", [
        ("Number", "al-Khwārizmī — numerals & zero", DIRECT, None),
        ("Algebra and graphs", "al-Khwārizmī — al-jabr", DIRECT, "algebra"),
        ("Coordinate geometry", None, NONE, None),
        ("Geometry", "ʿUmar Khayyām — cubics", PRECURSOR, None),
        ("Mensuration", None, NONE, None),
        ("Trigonometry", "al-Battānī, al-Ṭūsī", DIRECT, None),
        ("Transformations and vectors", None, NONE, None),
        ("Probability", None, NONE, None),
        ("Statistics", None, NONE, None),
    ]),
    ("Physics", "0625", "#2b7cc4", [
        ("Motion, forces and energy", "Ibn Sīnā, al-Bīrūnī", PRECURSOR, None),
        ("Thermal physics", None, NONE, None),
        ("Waves", "Ibn al-Haytham — optics", DIRECT, None),
        ("Electricity and magnetism", None, NONE, None),
        ("Nuclear physics", None, NONE, None),
        ("Space physics", "al-Battānī, Ibn al-Shāṭir", DIRECT, None),
    ]),
    ("Chemistry", "0620", "#c9453a", [
        ("States of matter", None, NONE, None),
        ("Atoms, elements and compounds", "Jābir, al-Rāzī", DIRECT, None),
        ("Stoichiometry", None, NONE, None),
        ("Electrochemistry", None, NONE, None),
        ("Chemical energetics", None, NONE, None),
        ("Chemical reactions", None, NONE, None),
        ("Acids, bases and salts", "al-Rāzī", DIRECT, None),
        ("The Periodic Table", None, NONE, None),
        ("Metals", "Jābir — classifying metals", DIRECT, None),
        ("Chemistry of the environment", None, NONE, None),
        ("Organic chemistry", "Muslim chemists — distillation", PRECURSOR, None),
        ("Experimental techniques and chemical analysis", "Jābir, al-Rāzī", DIRECT, None),
    ]),
    ("Biology", "0610", "#1f9c6e", [
        ("Characteristics and classification", "al-Jāḥiẓ, al-Dīnawarī", DIRECT, None),
        ("Organisation of the organism", None, NONE, None),
        ("Movement into and out of cells", None, NONE, None),
        ("Biological molecules", None, NONE, None),
        ("Enzymes", None, NONE, None),
        ("Plant nutrition", None, NONE, None),
        ("Human nutrition", "Ibn Sīnā — Canon", DIRECT, None),
        ("Transport in plants", None, NONE, None),
        ("Transport in animals", "Ibn al-Nafīs — circulation", DIRECT, None),
        ("Diseases and immunity", "al-Rāzī, Ibn Sīnā", DIRECT, None),
        ("Gas exchange in humans", None, NONE, None),
        ("Respiration", None, NONE, None),
        ("Excretion in humans", None, NONE, None),
        ("Coordination and response", "Ibn al-Haytham — the eye", DIRECT, None),
        ("Drugs", None, NONE, None),
        ("Reproduction", None, NONE, None),
        ("Inheritance", None, NONE, None),
        ("Variation and selection", "al-Jāḥiẓ — adaptation", PRECURSOR, None),
        ("Organisms and their environment", "al-Jāḥiẓ — food chains", DIRECT, None),
        ("Human influences on ecosystems", None, NONE, None),
        ("Biotechnology and genetic modification", None, NONE, None),
    ]),
    ("Computer Science", "0478", "#d1497f", [
        ("Data representation", "numeral heritage", PRECURSOR, None),
        ("Data transmission", "al-Kindī — cryptanalysis", DIRECT, None),
        ("Hardware", None, NONE, None),
        ("Software", None, NONE, None),
        ("The internet and its uses", None, NONE, None),
        ("Automated and emerging technologies", "al-Jazarī, Banū Mūsā", DIRECT, None),
        ("Algorithm design and problem-solving", "al-Khwārizmī", DIRECT, None),
        ("Programming", None, NONE, None),
        ("Databases", None, NONE, None),
        ("Boolean logic", "al-Fārābī, Ibn Rushd", PRECURSOR, None),
    ]),
]

INK, MUTED, FAINT = "#2c2216", "#6b5535", "#a3937a"
GOLD, EDGE, CARD, CARD2 = "#b8860b", "#dcc9a0", "#fdf7e9", "#f7ecd6"

W = 1460
MARGIN, GAP = 22, 12
HEAD_H, TOP = 54, 30
ROW_PLAIN, ROW_MARKED = 23, 33


def _fit(text, limit):
    """Truncate on a word boundary with an ellipsis — never mid-word, which
    reads as a rendering bug rather than a deliberate elision."""
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut + "\u2026"


def counts():
    d = p = plain = live = 0
    for *_, chapters in SUBJECTS:
        for _, _, mark, key in chapters:
            d += mark == DIRECT
            p += mark == PRECURSOR
            plain += mark is NONE
            live += key is not None
    return {"direct": d, "precursor": p, "plain": plain,
            "total": d + p + plain, "live": live}


def render():
    n = len(SUBJECTS)
    col_w = (W - 2 * MARGIN - (n - 1) * GAP) / n

    heights = []
    for *_, chapters in SUBJECTS:
        h = sum(ROW_MARKED if m else ROW_PLAIN for _, _, m, _ in chapters)
        heights.append(h)
    box_h = max(heights) + HEAD_H + 20
    height = TOP + box_h + 92

    s = [f'<svg viewBox="0 0 {W} {height}" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="Iowan Old Style, Palatino, Georgia, serif" '
         f'style="width:100%;height:auto">']

    for ci, (subject, code, colour, chapters) in enumerate(SUBJECTS):
        x = MARGIN + ci * (col_w + GAP)

        # subject box
        s.append(f'<rect x="{x}" y="{TOP}" width="{col_w}" height="{box_h}" rx="9" '
                 f'fill="{CARD}" stroke="{colour}" stroke-width="1.6" stroke-opacity=".55"/>')
        s.append(f'<path d="M {x+9} {TOP} h {col_w-18} a 9 9 0 0 1 9 9 v {HEAD_H-9} '
                 f'h {-col_w} v {-(HEAD_H-9)} a 9 9 0 0 1 9 -9 z" fill="{colour}"/>')
        s.append(f'<text x="{x+col_w/2}" y="{TOP+23}" text-anchor="middle" font-size="15.5" '
                 f'fill="#fdf7e9">{escape(subject)}</text>')
        s.append(f'<text x="{x+col_w/2}" y="{TOP+41}" text-anchor="middle" font-size="11.5" '
                 f'fill="#fdf7e9" fill-opacity=".85">{code}</text>')

        y = TOP + HEAD_H + 14
        for chapter, who, mark, key in chapters:
            live = key is not None
            row_h = ROW_MARKED if mark else ROW_PLAIN

            if live:
                s.append(f'<a href="?t={key}" target="_self">')

            if mark:
                s.append(f'<rect x="{x+7}" y="{y-11}" width="{col_w-14}" height="{row_h-4}" rx="3" '
                         f'fill="{CARD2 if not live else "#f6e2b0"}" stroke="{colour}" '
                         f'stroke-width="{1.6 if live else 0.9}" '
                         f'stroke-opacity="{1 if live else .5}"/>')
                if mark == DIRECT:
                    s.append(f'<circle cx="{x+17}" cy="{y}" r="4.4" fill="{colour}"/>')
                else:
                    s.append(f'<circle cx="{x+17}" cy="{y}" r="4.1" fill="none" '
                             f'stroke="{colour}" stroke-width="1.6"/>')
                s.append(f'<text x="{x+27}" y="{y+4}" font-size="10.9" fill="{INK}" '
                         f'font-weight="{600 if live else 400}">{escape(_fit(chapter, 34))}</text>')
                s.append(f'<text x="{x+27}" y="{y+16}" font-size="10" fill="{MUTED}" '
                         f'font-style="italic">{escape(_fit(who or "", 36))}</text>')
                if live:
                    s.append(f'<rect x="{x+col_w-46}" y="{y-8}" width="34" height="14" rx="2" fill="{GOLD}"/>')
                    s.append(f'<text x="{x+col_w-29}" y="{y+2.5}" text-anchor="middle" '
                             f'font-size="8" fill="#fdf7e9" letter-spacing=".8">LIVE</text>')
            else:
                s.append(f'<text x="{x+27}" y="{y+4}" font-size="10.8" fill="{FAINT}">'
                         f'{escape(_fit(chapter, 35))}</text>')

            if live:
                s.append("</a>")
            y += row_h

    # legend + footnote
    ly = TOP + box_h + 34
    s.append(f'<line x1="{MARGIN}" y1="{ly-22}" x2="{W-MARGIN}" y2="{ly-22}" '
             f'stroke="{EDGE}" stroke-width="1"/>')
    items = [("fill", "Direct lineage — the field was shaped in the Muslim world"),
             ("ring", "Precursor — an early or partial contribution, marked as such"),
             ("none", "On the syllabus, no Islamic thread — carried by Tier 2 or Tier 3")]
    lx = MARGIN + 6
    for kind, label in items:
        if kind == "fill":
            s.append(f'<circle cx="{lx}" cy="{ly-4}" r="4.6" fill="{INK}"/>')
        elif kind == "ring":
            s.append(f'<circle cx="{lx}" cy="{ly-4}" r="4.3" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        else:
            s.append(f'<text x="{lx-4}" y="{ly}" font-size="12" fill="{FAINT}">—</text>')
        s.append(f'<text x="{lx+14}" y="{ly}" font-size="12.5" fill="{MUTED}">{label}</text>')
        lx += 470

    c = counts()
    s.append(f'<text x="{W/2}" y="{ly+32}" text-anchor="middle" font-size="13" '
             f'fill="{FAINT}" font-style="italic">'
             f'{c["direct"] + c["precursor"]} of {c["total"]} Cambridge chapters carry an Islamic '
             f'thread. The other {c["plain"]} are taught through the algorithm of the topic — '
             f'Tier 2 or Tier 3 — and are no less rigorous for it.</text>')

    s.append("</svg>")
    return "".join(s)
