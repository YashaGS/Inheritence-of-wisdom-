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

DIRECT, PRECURSOR, TIER2, NONE = "direct", "precursor", "tier2", None

# (chapter, inherited_work, scholar, mark, lesson_key)
#
# The work leads and the scholar attributes it. What a child inherits is the
# method that was left behind, not a name to admire — so the name never takes
# the headline position.
SUBJECTS = [
    ("Mathematics", "0580", "#6a4bc0", [
        ("Number", "Place value, zero, and the Hindu-Arabic numerals",
         "al-Khwārizmī", DIRECT, None),
        ("Algebra and graphs", "al-jabr — solving by restoring and balancing",
         "al-Khwārizmī", DIRECT, "algebra"),
        ("Coordinate geometry", None, None, NONE, None),
        ("Geometry", "The geometric solution of cubic equations",
         "ʿUmar Khayyām", PRECURSOR, None),
        ("Mensuration", None, None, NONE, None),
        ("Trigonometry", "Sine, cosine and tangent made a subject of their own",
         "al-Battānī, al-Ṭūsī", DIRECT, None),
        ("Transformations and vectors", None, None, NONE, None),
        ("Probability", None, None, NONE, None),
        ("Statistics", None, None, NONE, None),
    ]),
    ("Physics", "0625", "#2b7cc4", [
        ("Motion, forces and energy", "Impetus — the ancestor of momentum",
         "Ibn Sīnā, al-Bīrūnī", PRECURSOR, None),
        ("Thermal physics", None, None, NONE, None),
        ("Waves", "Kitāb al-Manāẓir — light travels to the eye, not from it",
         "Ibn al-Haytham", DIRECT, None),
        ("Electricity and magnetism", "The field — space itself carries the force",
         "Michael Faraday", TIER2, "magnetism"),
        ("Nuclear physics", None, None, NONE, None),
        ("Space physics", "Star catalogues and corrected planetary models",
         "al-Battānī, Ibn al-Shāṭir", DIRECT, None),
    ]),
    ("Chemistry", "0620", "#c9453a", [
        ("States of matter", None, None, NONE, None),
        ("Atoms, elements and compounds", "Substances grouped by how they behave",
         "Jābir, al-Rāzī", DIRECT, None),
        ("Stoichiometry", None, None, NONE, None),
        ("Electrochemistry", None, None, NONE, None),
        ("Chemical energetics", None, None, NONE, None),
        ("Chemical reactions", None, None, NONE, None),
        ("Acids, bases and salts", "The preparation of the mineral acids",
         "al-Rāzī", DIRECT, None),
        ("The Periodic Table", None, None, NONE, None),
        ("Metals", "Metals, spirits and salts, systematically grouped",
         "Jābir", DIRECT, None),
        ("Chemistry of the environment", None, None, NONE, None),
        ("Organic chemistry", "Distillation of organic materials",
         "Muslim chemists", PRECURSOR, None),
        ("Experimental techniques and chemical analysis",
         "The laboratory itself — distillation, filtration, crystallisation",
         "Jābir, al-Rāzī", DIRECT, "distillation"),
    ]),
    ("Biology", "0610", "#1f9c6e", [
        ("Characteristics and classification", "Kitāb al-Ḥayawān — classifying the living world",
         "al-Jāḥiẓ, al-Dīnawarī", DIRECT, None),
        ("Organisation of the organism", None, None, NONE, None),
        ("Movement into and out of cells", None, None, NONE, None),
        ("Biological molecules", None, None, NONE, None),
        ("Enzymes", None, None, NONE, None),
        ("Plant nutrition", None, None, NONE, None),
        ("Human nutrition", "The Canon of Medicine — diet as treatment",
         "Ibn Sīnā", DIRECT, None),
        ("Transport in plants", None, None, NONE, None),
        ("Transport in animals", "The pulmonary circulation, described and argued",
         "Ibn al-Nafīs", DIRECT, "circulation"),
        ("Diseases and immunity", "Smallpox distinguished from measles by observation",
         "al-Rāzī, Ibn Sīnā", DIRECT, None),
        ("Gas exchange in humans", None, None, NONE, None),
        ("Respiration", None, None, NONE, None),
        ("Excretion in humans", None, None, NONE, None),
        ("Coordination and response", "Optics — how the eye actually sees",
         "Ibn al-Haytham", DIRECT, None),
        ("Drugs", None, None, NONE, None),
        ("Reproduction", None, None, NONE, None),
        ("Inheritance", None, None, NONE, None),
        ("Variation and selection", "Adaptation, and the struggle for existence",
         "al-Jāḥiẓ", PRECURSOR, None),
        ("Organisms and their environment", "Early food chains and habitat",
         "al-Jāḥiẓ", DIRECT, None),
        ("Human influences on ecosystems", None, None, NONE, None),
        ("Biotechnology and genetic modification", None, None, NONE, None),
    ]),
    ("Computer Science", "0478", "#d1497f", [
        ("Data representation", "The place-value system every base rests on",
         "numeral heritage", PRECURSOR, None),
        ("Data transmission", "Frequency analysis — the first systematic codebreaking",
         "al-Kindī", DIRECT, "cipher"),
        ("Hardware", None, None, NONE, None),
        ("Software", None, None, NONE, None),
        ("The internet and its uses", None, None, NONE, None),
        ("Automated and emerging technologies", "Programmable machines that ran without a hand on them",
         "al-Jazarī, Banū Mūsā", DIRECT, None),
        ("Algorithm design and problem-solving", "The written, repeatable procedure itself",
         "al-Khwārizmī", DIRECT, None),
        ("Programming", None, None, NONE, None),
        ("Databases", None, None, NONE, None),
        ("Boolean logic", "Formal and conditional logic",
         "al-Fārābī, Ibn Rushd", PRECURSOR, None),
    ]),
]

SUBJECT_KEYS = ["maths", "physics", "chemistry", "biology", "cs"]

# Cambridge subtopics, extracted verbatim from the syllabus PDF and grouped by the
# chapter number in their own code (E2.x sits under chapter 2). Only Mathematics is
# populated so far; a subject with no entry simply shows its chapters.
SUBTOPICS = {
    "maths": {
        1: [("E1.1", "Types of number"), ("E1.2", "Sets"), ("E1.3", "Powers and roots"),
            ("E1.4", "Fractions, decimals and percentages"), ("E1.5", "Ordering"),
            ("E1.6", "The four operations"), ("E1.7", "Indices I"),
            ("E1.8", "Standard form"), ("E1.9", "Estimation"),
            ("E1.10", "Limits of accuracy"), ("E1.11", "Ratio and proportion"),
            ("E1.12", "Rates"), ("E1.13", "Percentages"), ("E1.14", "Using a calculator"),
            ("E1.15", "Time"), ("E1.16", "Money"),
            ("E1.17", "Exponential growth and decay"), ("E1.18", "Surds")],
        2: [("E2.1", "Introduction to algebra"), ("E2.2", "Algebraic manipulation"),
            ("E2.3", "Algebraic fractions"), ("E2.4", "Indices II"),
            ("E2.5", "Equations"), ("E2.6", "Inequalities"), ("E2.7", "Sequences"),
            ("E2.8", "Proportion"), ("E2.9", "Graphs in practical situations"),
            ("E2.10", "Graphs of functions"), ("E2.11", "Sketching curves"),
            ("E2.12", "Differentiation"), ("E2.13", "Functions")],
        3: [("E3.1", "Coordinates"), ("E3.2", "Drawing linear graphs"),
            ("E3.3", "Gradient of linear graphs"), ("E3.4", "Length and midpoint"),
            ("E3.5", "Equations of linear graphs"), ("E3.6", "Parallel lines"),
            ("E3.7", "Perpendicular lines")],
        4: [("E4.1", "Geometrical terms"), ("E4.2", "Geometrical constructions"),
            ("E4.3", "Scale drawings"), ("E4.4", "Similarity"), ("E4.5", "Symmetry"),
            ("E4.6", "Angles"), ("E4.7", "Circle theorems I"),
            ("E4.8", "Circle theorems II")],
        5: [("E5.1", "Units of measure"), ("E5.2", "Area and perimeter"),
            ("E5.3", "Circles, arcs and sectors"), ("E5.4", "Surface area and volume"),
            ("E5.5", "Compound shapes and parts of shapes")],
        6: [("E6.1", "Pythagoras’ theorem"), ("E6.2", "Right-angled triangles"),
            ("E6.3", "Exact trigonometric values"), ("E6.4", "Trigonometric functions"),
            ("E6.5", "Non-right-angled triangles"),
            ("E6.6", "Pythagoras’ theorem and trigonometry")],
        7: [("E7.1", "Transformations"), ("E7.2", "Vectors in two dimensions"),
            ("E7.3", "Magnitude of a vector"), ("E7.4", "Vector geometry")],
        8: [("E8.1", "Introduction to probability"),
            ("E8.2", "Relative and expected frequencies"),
            ("E8.3", "Probability of combined events"), ("E8.4", "Conditional probability")],
        9: [("E9.1", "Classifying statistical data"), ("E9.2", "Interpreting statistical data"),
            ("E9.3", "Averages and measures of spread"),
            ("E9.4", "Statistical charts and diagrams"), ("E9.5", "Scatter diagrams"),
            ("E9.6", "Cumulative frequency diagrams"), ("E9.7", "Histograms")],
    },
    "physics": {
        1: [("1.1", "Physical quantities and measurement techniques"), ("1.2", "Motion"), ("1.3", "Mass and weight"), ("1.4", "Density"), ("1.5", "Forces"), ("1.6", "Momentum"), ("1.7", "Energy, work and power"), ("1.8", "Pressure")],
        2: [("2.1", "Kinetic particle model of matter"), ("2.2", "Thermal properties and temperature"), ("2.3", "Transfer of thermal energy")],
        3: [("3.1", "General properties of waves"), ("3.2", "Light"), ("3.3", "Electromagnetic spectrum"), ("3.4", "Sound")],
        4: [("4.1", "Simple phenomena of magnetism"), ("4.2", "Electrical quantities"), ("4.3", "Electric circuits"), ("4.4", "Electrical safety"), ("4.5", "Electromagnetic effects")],
        5: [("5.1", "The nuclear model of the atom"), ("5.2", "Radioactivity")],
        6: [("6.1", "The Earth and the Solar System"), ("6.2", "Stars and the Universe")],
    },
    "chemistry": {
        1: [("1.1", "Solids, liquids and gases"), ("1.2", "Diffusion")],
        2: [("2.1", "Elements, compounds and mixtures"), ("2.2", "Atomic structure and the Periodic Table"), ("2.3", "Isotopes"), ("2.4", "Ions and ionic bonds"), ("2.5", "Simple molecules and covalent bonds"), ("2.6", "Giant covalent structures"), ("2.7", "Metallic bonding")],
        3: [("3.1", "Formulae"), ("3.2", "Relative masses of atoms and molecules"), ("3.3", "The mole and the Avogadro constant")],
        4: [("4.1", "Electrolysis"), ("4.2", "Hydrogen–oxygen fuel cells")],
        5: [("5.1", "Exothermic and endothermic reactions")],
        6: [("6.1", "Physical and chemical changes"), ("6.2", "Rate of reaction"), ("6.3", "Reversible reactions and equilibrium"), ("6.4", "Redox")],
        7: [("7.1", "The characteristic properties of acids and bases"), ("7.2", "Oxides"), ("7.3", "Preparation of salts")],
        8: [("8.1", "Arrangement of elements"), ("8.2", "Group I properties"), ("8.3", "Group VII properties"), ("8.4", "Transition elements"), ("8.5", "Noble gases")],
        9: [("9.1", "Properties of metals"), ("9.2", "Uses of metals"), ("9.3", "Alloys and their properties"), ("9.4", "Reactivity series"), ("9.5", "Corrosion of metals"), ("9.6", "Extraction of metals")],
        10: [("10.1", "Water"), ("10.2", "Fertilisers"), ("10.3", "Air quality and climate")],
        11: [("11.1", "Formulae, functional groups and terminology"), ("11.2", "Naming organic compounds"), ("11.3", "Fuels"), ("11.4", "Alkanes"), ("11.5", "Alkenes"), ("11.6", "Alcohols"), ("11.7", "Carboxylic acids"), ("11.8", "Polymers")],
        12: [("12.1", "Experimental design"), ("12.2", "Acid–base titrations"), ("12.3", "Chromatography"), ("12.4", "Separation and purification"), ("12.5", "Identification of ions and gases")],
    },
    "biology": {
        1: [("1.1", "Characteristics of living organisms"), ("1.2", "Concept and uses of classification systems"), ("1.3", "Features of organisms")],
        2: [("2.1", "Cell structure"), ("2.2", "Size of specimens")],
        3: [("3.1", "Diffusion"), ("3.2", "Osmosis"), ("3.3", "Active transport")],
        4: [("4.1", "Biological molecules")],
        5: [("5.1", "Enzymes")],
        6: [("6.1", "Photosynthesis"), ("6.2", "Leaf structure")],
        7: [("7.1", "Diet"), ("7.2", "Digestive system"), ("7.3", "Physical digestion"), ("7.4", "Chemical digestion"), ("7.5", "Absorption")],
        8: [("8.1", "Xylem and phloem"), ("8.2", "Water uptake"), ("8.3", "Transpiration"), ("8.4", "Translocation")],
        9: [("9.1", "Circulatory systems"), ("9.2", "Heart"), ("9.3", "Blood vessels"), ("9.4", "Blood")],
        10: [("10.1", "Diseases and immunity")],
        11: [("11.1", "Gas exchange in humans")],
        12: [("12.1", "Respiration"), ("12.2", "Aerobic respiration"), ("12.3", "Anaerobic respiration")],
        13: [("13.1", "Excretion in humans")],
        14: [("14.1", "Coordination and response"), ("14.2", "Sense organs"), ("14.3", "Hormones"), ("14.4", "Homeostasis"), ("14.5", "Tropic responses")],
        15: [("15.1", "Drugs")],
        16: [("16.1", "Asexual reproduction"), ("16.2", "Sexual reproduction"), ("16.3", "Sexual reproduction in plants"), ("16.4", "Sexual reproduction in humans"), ("16.5", "Sex hormones in humans"), ("16.6", "Sexually transmitted infections")],
        17: [("17.1", "Chromosomes, genes and proteins"), ("17.2", "Mitosis"), ("17.3", "Meiosis"), ("17.4", "Monohybrid inheritance")],
        18: [("18.1", "Variation"), ("18.2", "Adaptive features"), ("18.3", "Selection")],
        19: [("19.1", "Energy flow"), ("19.2", "Food chains and food webs"), ("19.3", "Nutrient cycles"), ("19.4", "Populations")],
        20: [("20.1", "Food supply"), ("20.2", "Habitat destruction"), ("20.3", "Pollution"), ("20.4", "Conservation")],
        21: [("21.1", "Biotechnology and genetic modification"), ("21.2", "Biotechnology"), ("21.3", "Genetic modification")],
    },
    "cs": {
        1: [("1.1", "Number systems"), ("1.2", "Text, sound and images"), ("1.3", "Data storage and compression")],
        2: [("2.1", "Types and methods of data transmission"), ("2.2", "Methods of error detection"), ("2.3", "Encryption")],
        3: [("3.1", "Computer architecture"), ("3.2", "Input and output devices"), ("3.3", "Data storage"), ("3.4", "Network hardware")],
        4: [("4.1", "Types of software and interrupts")],
        5: [("5.1", "The internet and the world wide web"), ("5.2", "Digital currency"), ("5.3", "Cyber security")],
        6: [("6.1", "Automated systems"), ("6.2", "Robotics"), ("6.3", "Artificial intelligence")],
        8: [("8.1", "Programming concepts"), ("8.2", "Arrays"), ("8.3", "File handling")],
    },
}

# Where a built lesson actually lives, so the subtopic can be named on the card.
LESSON_SUBTOPIC = {
    "algebra": ("E2.2", "Algebraic manipulation — completing the square"),
    "magnetism": ("4.1", "Simple phenomena of magnetism"),
    "cipher": ("2.3", "Encryption"),
    "distillation": ("12.4", "Separation and purification"),
    "circulation": ("9.1", "Circulatory systems"),
}
LESSON_SOURCE = {
    "algebra": "al-Khwārizmī, Kitāb al-jabr · Rosen 1831, p. 8",
    "magnetism": "Faraday, Experimental Researches in Electricity · no manuscript layer",
    "cipher": "al-Kindī, Risāla fī Istikhrāj al-Muʿammā, c. 850 CE · no manuscript layer",
    "distillation": "al-Rāzī, Kitāb al-Asrār, c. 900 CE · no manuscript layer",
    "circulation": "Ibn al-Nafīs, Sharḥ Tashrīḥ al-Qānūn, c. 1242 · no manuscript layer",
}


def subject_by_key(key):
    """Return (name, code, colour, chapters) for a subject key, or None."""
    try:
        return SUBJECTS[SUBJECT_KEYS.index(key)]
    except ValueError:
        return None


def subject_stats(chapters):
    d = sum(1 for *_, m, _ in chapters if m == DIRECT)
    p = sum(1 for *_, m, _ in chapters if m in (PRECURSOR, TIER2))
    live = sum(1 for *_, k in chapters if k)
    return d, p, len(chapters), live


def colour_css():
    """Per-subject colour rules.

    Streamlit's markdown sanitiser drops inline `style` attributes, so a custom
    property set inline (`style="--sc-colour:…"`) silently never lands. Emitting
    real classes is the only reliable route.
    """
    out = ["<style>"]
    for key, (_, _, colour, _) in zip(SUBJECT_KEYS, SUBJECTS):
        out.append(
            f".sc-{key}{{border-left:5px solid {colour} !important}}"
            f".sc-{key}:hover{{border-color:{colour}}}"
            f".sc-{key} .sc-meta strong{{color:{colour}}}"
            f".chl-{key} .ch-dot.filled{{background:{colour}}}"
            f".chl-{key} .ch-dot.hollow{{border:2px solid {colour}}}"
            f".chl-{key} .ch.live{{border-color:{colour}}}"
        )
    out.append("</style>")
    return "".join(out)


def render_subject_cards():
    """Home page — subjects only. HTML rather than SVG so the cards reflow on
    a phone and get real hover/focus states."""
    out = ['<div class="subject-grid">']
    for key, (name, code, colour, chapters) in zip(SUBJECT_KEYS, SUBJECTS):
        d, p, total, live = subject_stats(chapters)
        badge = ('<span class="sc-live">1 lesson ready</span>' if live
                 else '<span class="sc-soon">lineage mapped</span>')
        out.append(
            f'<a class="sc sc-{key}" href="?s={key}" target="_self">'
            f'<span class="sc-name">{escape(name)}</span>'
            f'<span class="sc-code">Cambridge IGCSE {code}</span>'
            f'<span class="sc-meta">{total} chapters · '
            f'<strong>{d + p}</strong> carry a lineage</span>'
            f'{badge}</a>'
        )
    out.append("</div>")
    return "".join(out)


def render_chapters(key):
    """Subject page — chapters as cards, with their Cambridge subtopics inside."""
    s = subject_by_key(key)
    if not s:
        return "<p>Unknown subject.</p>"
    name, code, colour, chapters = s
    subs = SUBTOPICS.get(key, {})

    cards = []
    for i, (chapter, work, who, mark, lesson) in enumerate(chapters, start=1):
        live = lesson is not None
        cls = "chap" + (" marked" if mark else "") + (" live" if live else "")

        if mark == DIRECT:
            badge = '<span class="ch-dot filled"></span>'
        elif mark == PRECURSOR:
            badge = '<span class="ch-dot hollow"></span>'
        else:
            badge = '<span class="ch-dash">&mdash;</span>'

        if work:
            lineage = (f'<span class="chap-work">{escape(work)}</span>'
                       f'<span class="chap-who">{escape(who)}</span>')
        else:
            lineage = ('<span class="chap-who plain">taught through the algorithm '
                       'of the topic</span>')

        status = ""
        if live:
            sub_code, sub_title = LESSON_SUBTOPIC.get(lesson, ("", ""))
            status = (f'<span class="chap-cta">Enter chapter &rarr;</span>'
                      f'<span class="chap-at">Lesson sits in '
                      f'<b>{escape(sub_code)}</b> &middot; {escape(sub_title)}</span>')
            src = LESSON_SOURCE.get(lesson)
            if src:
                status += f'<span class="chap-src">Source &middot; {escape(src)}</span>'
        elif mark:
            status = '<span class="chap-pending">lesson not built yet</span>'

        chips = "".join(
            f'<span class="sub">{escape(c)} <i>{escape(t)}</i></span>'
            for c, t in subs.get(i, [])
        )
        chip_block = f'<div class="sub-list">{chips}</div>' if chips else ""

        inner = (f'<div class="chap-head">{badge}'
                 f'<span class="chap-name">{escape(chapter)}</span>{lineage}</div>'
                 f'{chip_block}'
                 + (f'<div class="chap-foot">{status}</div>' if status else ""))

        if live:
            cards.append(f'<a class="{cls}" href="?t={lesson}" target="_self">{inner}</a>')
        else:
            cards.append(f'<div class="{cls}">{inner}</div>')

    return f'<div class="chap-list chl-{key}">' + "".join(cards) + "</div>"



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
    d = p = t2 = plain = live = 0
    for *_, chapters in SUBJECTS:
        for _, _, _, mark, key in chapters:
            d += mark == DIRECT
            p += mark == PRECURSOR
            t2 += mark == TIER2
            plain += mark is NONE
            live += key is not None
    return {"direct": d, "precursor": p, "tier2": t2, "plain": plain,
            "total": d + p + t2 + plain, "live": live}


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
