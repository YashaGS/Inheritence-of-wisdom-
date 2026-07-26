"""
The syllabus map — the app's front page.

Shows the whole territory with every topic's lineage tier marked, and is honest
about which lessons actually exist. Exactly one node is built; the rest are
drawn as planned, not pretended.

Tier data is transcribed by hand from Miraath-al-Hikma_Heritage-Topics.md.
Per algorism-code-spine.md §5 it is curation, not generation — no model decides
a tier here.
"""

from xml.sax.saxutils import escape

# tier: 1 = Islamic scholar | 2 = other great mind | 3 = no single originator
# conf: "direct" / "precursor" — only meaningful within tier 1
# key:  set only where a lesson actually exists

SUBJECTS = [
    ("Mathematics", "0580", [
        ("Completing the square", "al-Khwārizmī", 1, "direct", "algebra"),
        ("Numerals & zero", "al-Khwārizmī", 1, "direct", None),
        ("Trigonometry", "al-Battānī · al-Ṭūsī", 1, "direct", None),
        ("Decimal fractions", "al-Uqlīdisī", 1, "precursor", None),
        ("Binomial patterns", "al-Karajī", 1, "precursor", None),
        ("Coordinate geometry", "Descartes", 2, None, None),
        ("Vectors & matrices", "no single originator", 3, None, None),
        ("Probability & statistics", "Pascal · Fermat", 2, None, None),
        ("Mensuration", "no single originator", 3, None, None),
    ]),
    ("Physics", "0625", [
        ("Light & optics", "Ibn al-Haytham", 1, "direct", None),
        ("The experimental method", "Ibn al-Haytham", 1, "direct", None),
        ("Astronomy", "al-Battānī · Ibn al-Shāṭir", 1, "direct", None),
        ("Motion & density", "Ibn Sīnā · al-Bīrūnī", 1, "precursor", None),
        ("Electricity & magnetism", "Faraday", 2, None, None),
        ("Nuclear physics", "Rutherford", 2, None, None),
        ("Thermal physics", "no single originator", 3, None, None),
        ("Energy & work", "no single originator", 3, None, None),
        ("Electrical circuits", "no single originator", 3, None, None),
    ]),
    ("Chemistry", "0620", [
        ("Lab technique & distillation", "Jābir ibn Ḥayyān", 1, "direct", None),
        ("Acids, bases & salts", "al-Rāzī", 1, "direct", None),
        ("Classification of matter", "Jābir · al-Rāzī", 1, "direct", None),
        ("Organic separation", "Muslim chemists", 1, "precursor", None),
        ("The Periodic Table", "Mendeleev", 2, None, None),
        ("Conservation of mass", "Lavoisier", 2, None, None),
        ("Stoichiometry & moles", "no single originator", 3, None, None),
        ("Electrochemistry", "no single originator", 3, None, None),
        ("Chemical energetics", "no single originator", 3, None, None),
    ]),
    ("Biology", "0610", [
        ("Blood circulation", "Ibn al-Nafīs", 1, "direct", None),
        ("Disease & immunity", "al-Rāzī · Ibn Sīnā", 1, "direct", None),
        ("The eye & vision", "Ibn al-Haytham", 1, "direct", None),
        ("Classification & ecosystems", "al-Jāḥiẓ · al-Dīnawarī", 1, "direct", None),
        ("Variation & selection", "al-Jāḥiẓ", 1, "precursor", None),
        ("Inheritance & genetics", "Mendel", 2, None, None),
        ("Biological molecules", "no single originator", 3, None, None),
        ("Enzymes", "no single originator", 3, None, None),
        ("Respiration biochemistry", "no single originator", 3, None, None),
    ]),
    ("Computer Science", "0478", [
        ("Algorithm design", "al-Khwārizmī", 1, "direct", None),
        ("Automata & robotics", "al-Jazarī · Banū Mūsā", 1, "direct", None),
        ("Data security", "al-Kindī", 1, "direct", None),
        ("Boolean logic", "al-Fārābī · Ibn Rushd", 1, "precursor", None),
        ("Data representation", "al-Khwārizmī", 1, "precursor", None),
        ("Hardware & architecture", "von Neumann", 2, None, None),
        ("Computer networks", "no single originator", 3, None, None),
        ("Databases", "no single originator", 3, None, None),
        ("Software development", "no single originator", 3, None, None),
    ]),
]

INK, GOLD, MUTED = "#2c2216", "#b8860b", "#9a8358"
CARD, CARD_LIVE = "#f7ecd6", "#f6e2b0"
EDGE, EDGE_LIVE = "#dcc9a0", "#b8860b"

MARGIN, COL_W, GAP = 34, 266, 12
ROW_H, CARD_H = 47, 41
TOP = 150


def _tier_glyph(tier, conf):
    if tier == 1:
        return ("●", GOLD) if conf == "direct" else ("○", GOLD)
    if tier == 2:
        return ("◆", "#6b7f8a")
    return ("·", MUTED)


def counts():
    """Honest coverage numbers, computed — not asserted."""
    t = {1: 0, 2: 0, 3: 0}
    live = 0
    for _, _, topics in SUBJECTS:
        for _, _, tier, _, key in topics:
            t[tier] += 1
            if key:
                live += 1
    return t, sum(t.values()), live


def render(width=1440):
    rows = max(len(t) for _, _, t in SUBJECTS)
    height = TOP + rows * ROW_H + 96

    s = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="Iowan Old Style, Palatino, Georgia, serif" '
         f'style="width:100%;height:auto">']

    # title
    s.append(f'<text x="{width/2}" y="52" text-anchor="middle" font-size="30" '
             f'fill="{INK}">The syllabus, honestly mapped</text>')
    s.append(f'<text x="{width/2}" y="80" text-anchor="middle" font-size="15" '
             f'fill="#6b5535" font-style="italic">Every topic carries a thinking method. '
             f'Not every topic carries an Islamic lineage — and we say which.</text>')
    s.append(f'<line x1="{MARGIN}" y1="100" x2="{width-MARGIN}" y2="100" '
             f'stroke="{EDGE}" stroke-width="1"/>')

    for ci, (subject, code, topics) in enumerate(SUBJECTS):
        x = MARGIN + ci * (COL_W + GAP)

        s.append(f'<text x="{x}" y="126" font-size="16" fill="{INK}">{escape(subject)}</text>')
        s.append(f'<text x="{x + COL_W}" y="126" text-anchor="end" font-size="13" '
                 f'fill="{MUTED}">{code}</text>')
        s.append(f'<line x1="{x}" y1="134" x2="{x+COL_W}" y2="134" '
                 f'stroke="{GOLD}" stroke-width="1.4" stroke-opacity=".55"/>')

        for ri, (label, who, tier, conf, key) in enumerate(topics):
            y = TOP + ri * ROW_H
            live = key is not None
            glyph, gcol = _tier_glyph(tier, conf)
            fill = CARD_LIVE if live else CARD
            edge = EDGE_LIVE if live else EDGE
            op = "1" if live else ".62"

            if live:
                s.append(f'<a href="?t={key}" target="_self">')

            s.append(f'<g opacity="{op}">')
            s.append(f'<rect x="{x}" y="{y}" width="{COL_W}" height="{CARD_H}" rx="2" '
                     f'fill="{fill}" stroke="{edge}" '
                     f'stroke-width="{1.8 if live else 1}"/>')
            s.append(f'<text x="{x+11}" y="{y+18}" font-size="12.5" fill="{gcol}">{glyph}</text>')
            s.append(f'<text x="{x+27}" y="{y+18}" font-size="13.5" fill="{INK}">'
                     f'{escape(label[:30])}</text>')
            s.append(f'<text x="{x+27}" y="{y+33}" font-size="11.5" fill="#7a6338" '
                     f'font-style="italic">{escape(who[:34])}</text>')

            if live:
                s.append(f'<rect x="{x+COL_W-52}" y="{y+8}" width="44" height="15" rx="2" '
                         f'fill="{GOLD}"/>')
                s.append(f'<text x="{x+COL_W-30}" y="{y+19}" text-anchor="middle" '
                         f'font-size="9" fill="#fdf7e9" letter-spacing="1">LIVE</text>')
            s.append("</g>")

            if live:
                s.append("</a>")

    # legend
    ly = TOP + rows * ROW_H + 34
    s.append(f'<line x1="{MARGIN}" y1="{ly-22}" x2="{width-MARGIN}" y2="{ly-22}" '
             f'stroke="{EDGE}" stroke-width="1"/>')
    legend = [
        ("●", GOLD, "Tier 1 — Islamic scholar, direct"),
        ("○", GOLD, "Tier 1 — precursor"),
        ("◆", "#6b7f8a", "Tier 2 — another great mind"),
        ("·", MUTED, "Tier 3 — no single originator"),
    ]
    lx = MARGIN
    for glyph, col, text in legend:
        s.append(f'<text x="{lx}" y="{ly}" font-size="13" fill="{col}">{glyph}</text>')
        s.append(f'<text x="{lx+16}" y="{ly}" font-size="12.5" fill="#6b5535">{text}</text>')
        lx += 300

    s.append("</svg>")
    return "".join(s)
