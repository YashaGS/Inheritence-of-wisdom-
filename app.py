"""
Mīrāth al-Ḥikma · Algorism
A page of al-Khwārizmī's Algebra, carried to a Cambridge IGCSE lesson.

Demo discipline: every screen reads from content/frozen.json. There is no
network call and no model call anywhere in this file. The only number computed
at runtime is the critic score, and it is computed deterministically in
critic.py from two frozen strings.
"""

import base64
import json
from pathlib import Path

import streamlit as st

import critic
import mindmap

ROOT = Path(__file__).parent
SCREENS = ["Manuscript", "Unlock", "Critic", "Mīrāth", "Miftāḥ", "Jisr", "Apply"]

st.set_page_config(
    page_title="Mīrāth al-Ḥikma · Algorism",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data
def load():
    return json.loads((ROOT / "content" / "frozen.json").read_text(encoding="utf-8"))


@st.cache_data
def img_b64(rel_path):
    p = ROOT / rel_path
    if not p.exists():
        return None
    return base64.b64encode(p.read_bytes()).decode()


CSS = """
<style>
/* No @import and no external font: a webfont fetch is a network call, and the
   demo path must survive with the wifi off. System serifs only. */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}
.block-container {padding-top: 2.2rem; padding-bottom: 5rem; max-width: 1100px;}

.stApp {
  background:
    radial-gradient(ellipse at 20% 10%, #fbf3e2 0%, transparent 55%),
    radial-gradient(ellipse at 85% 90%, #f0e2c4 0%, transparent 55%),
    #f4e9d4;
}
html, body, [class*="css"] { color: #2c2216; }

.hd { font-family: 'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif; }

.rule {
  height: 2px; margin: 0 0 1.6rem 0;
  background: linear-gradient(90deg, transparent, #b8860b 12%, #d4a933 50%, #b8860b 88%, transparent);
}
.eyebrow {
  font-family: 'Iowan Old Style',Palatino,Georgia,serif;
  letter-spacing: .30em; text-transform: uppercase;
  font-size: .70rem; color: #9a7b2e; margin-bottom: .5rem;
}
h1.title {
  font-family: 'Iowan Old Style',Palatino,Georgia,serif;
  font-size: 2.7rem; line-height: 1.12; margin: 0 0 .35rem 0;
  color: #2c2216; font-weight: 600;
}
.subtitle { font-family: Georgia,serif; font-style: italic; color: #6b5535; font-size: 1.06rem; margin-bottom: 1.4rem; }

.panel {
  background: linear-gradient(#fdf7e9, #f7ecd6);
  border: 1px solid #dcc9a0; border-radius: 3px;
  padding: 1.5rem 1.7rem; margin-bottom: 1.1rem;
  box-shadow: 0 1px 3px rgba(90,70,30,.14), inset 0 0 60px rgba(184,134,11,.045);
}
.panel h3 {
  font-family: 'Iowan Old Style',Palatino,Georgia,serif;
  font-size: 1.06rem; margin: 0 0 .8rem 0; color: #7a5c1a;
  letter-spacing: .04em; font-weight: 600;
}
.panel p, .panel li { font-family: Georgia,serif; font-size: 1.0rem; line-height: 1.68; color: #33281a; }

.arabic {
  direction: rtl; text-align: right;
  font-family: 'Geeza Pro','Al Bayan','Baghdad','Scheherazade New','Amiri','Times New Roman',serif;
  font-size: 1.5rem; line-height: 2.5; color: #241c12;
}
.translit { font-family: Georgia,serif; font-style: italic; color: #6b5535; }

.gold { color: #9a7b2e; font-weight: 600; }
.dropcap::first-letter {
  font-family: 'Iowan Old Style',Palatino,Georgia,serif;
  float: left; font-size: 3.3rem; line-height: .82;
  padding: .1rem .5rem 0 0; color: #b8860b;
}

.score-num {
  font-family: 'Iowan Old Style',Palatino,Georgia,serif;
  font-size: 4.2rem; line-height: 1; color: #1f5e3d; font-weight: 600;
}
.score-num.med { color: #8a6a12; }
.score-num.bad { color: #8b2635; }
.verdict {
  font-family: Georgia,serif; letter-spacing:.08em; text-transform: uppercase;
  font-size: .78rem; color: #1f5e3d; font-weight: 700;
}
.chip {
  display:inline-block; font-family: Georgia,serif; font-size:.82rem;
  background:#efe3c6; border:1px solid #d3bd8e; border-radius:2px;
  padding:.18rem .55rem; margin:.16rem .3rem .16rem 0; color:#4a3a1c;
}
.chip.ok { background:#e4efe1; border-color:#a9c9a0; color:#255e33; }
.cite {
  font-family: Georgia,serif; font-size:.84rem; color:#7a6338;
  border-left: 2px solid #c9a227; padding-left:.7rem; margin-top:.9rem; font-style: italic;
}
.tier1 {
  display:inline-block; background:#7a5c1a; color:#f7ecd6;
  font-family: Georgia,serif; font-size:.74rem; letter-spacing:.12em;
  text-transform:uppercase; padding:.22rem .7rem; border-radius:2px;
}
.steps { counter-reset: s; list-style:none; padding-left:0; }
.steps li {
  counter-increment: s; position: relative; padding-left: 2.5rem;
  margin-bottom: .85rem; font-family: Georgia,serif; line-height:1.6;
}
.steps li::before {
  content: counter(s); position:absolute; left:0; top:.05rem;
  width:1.7rem; height:1.7rem; border-radius:50%;
  background:#f0e2c0; border:1px solid #c9a227; color:#7a5c1a;
  font-family:Georgia,serif; font-size:.85rem;
  display:flex; align-items:center; justify-content:center;
}
.socratic {
  font-family: Georgia,serif; font-style: italic; color:#5a4726;
  border-left:2px solid #d4a933; padding:.35rem 0 .35rem .9rem; margin:.5rem 0;
}
.progress { font-family: Georgia,serif; font-size:.78rem; color:#9a8358; letter-spacing:.16em; text-transform:uppercase; }

/* ---- home: subject cards ---- */
.subject-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px;margin:.4rem 0 0}
@media(max-width:1000px){.subject-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:640px){.subject-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
/* Streamlit underlines every anchor in markdown; override it on the card and
   everything inside it, or the whole grid reads as a wall of links. */
.subject-grid a, .subject-grid a *, .ch-list a, .ch-list a *{text-decoration:none !important}
.sc{
  position:relative;display:flex;flex-direction:column;gap:.28rem;
  padding:1.3rem 1.1rem 1.15rem 1.35rem;
  background:linear-gradient(#fdf7e9,#f7ecd6);
  border:1px solid #dcc9a0;border-left:5px solid var(--sc-colour);border-radius:3px;
  box-shadow:0 1px 3px rgba(90,70,30,.14);
  transition:border-color .18s ease, transform .18s ease, box-shadow .18s ease;
}
.sc:hover{box-shadow:0 4px 12px rgba(90,70,30,.2)}
.sc:hover{border-color:var(--sc-colour);transform:translateY(-2px)}
.sc:focus-visible{outline:2px solid var(--sc-colour);outline-offset:2px}
.sc-bar{position:absolute;inset:0 auto 0 0;width:4px;background:var(--sc-colour)}
.sc-name{font-family:'Iowan Old Style',Palatino,Georgia,serif;font-size:1.24rem;color:#2c2216}
.sc-code{font-family:Georgia,serif;font-size:.8rem;color:#9a8358;letter-spacing:.04em}
.sc-meta{font-family:Georgia,serif;font-size:.86rem;color:#6b5535;margin-top:.35rem}
.sc-meta strong{color:var(--sc-colour)}
.sc-live{
  margin-top:.55rem;align-self:flex-start;font-family:Georgia,serif;font-size:.72rem;
  letter-spacing:.09em;text-transform:uppercase;background:#b8860b;color:#fdf7e9;
  padding:.2rem .55rem;border-radius:2px;
}
.sc-soon{
  margin-top:.55rem;align-self:flex-start;font-family:Georgia,serif;font-size:.72rem;
  letter-spacing:.09em;text-transform:uppercase;color:#a3937a;
  border:1px solid #dcc9a0;padding:.2rem .55rem;border-radius:2px;
}

/* ---- subject page: chapter list ---- */
.ch-list{display:flex;flex-direction:column;gap:5px}
/* four children — dot, name, scholar, status — so four columns. With three,
   the status chip has no track and wraps to its own row. */
.ch{
  display:grid;grid-template-columns:18px minmax(0,1fr) auto minmax(90px,auto);
  align-items:center;gap:.5rem 1rem;padding:.62rem .9rem;border-radius:3px;
  font-family:Georgia,serif;text-decoration:none;
}
.ch.plain{grid-template-columns:18px minmax(0,1fr) auto}
.ch.plain{background:transparent;border:1px solid transparent}
.ch.marked{background:linear-gradient(#fdf7e9,#f7ecd6);border:1px solid #dcc9a0}
.ch.live{border-color:var(--sc-colour);border-width:1.6px;background:#f9edcf}
a.ch.live{transition:transform .16s ease}
a.ch.live:hover{transform:translateX(3px)}
a.ch.live:focus-visible{outline:2px solid var(--sc-colour);outline-offset:2px}
.ch-dot{width:11px;height:11px;border-radius:50%;display:inline-block}
.ch-dot.filled{background:var(--sc-colour)}
.ch-dot.hollow{border:2px solid var(--sc-colour)}
.ch-dash{color:#c2b596;font-size:1rem;text-align:center}
.ch-name{font-size:1rem;color:#2c2216}
.ch.plain .ch-name{color:#a3937a}
.ch-who{font-size:.85rem;color:#6b5535;font-style:italic;justify-self:end;text-align:right}
.ch.plain .ch-who{color:#bcae90}
.ch-live{
  font-size:.74rem;letter-spacing:.07em;text-transform:uppercase;
  background:#b8860b;color:#fdf7e9;padding:.2rem .55rem;border-radius:2px;white-space:nowrap;
}
.ch-pending{font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:#a3937a;white-space:nowrap;justify-self:end}
.ch-live{justify-self:end}
@media(max-width:860px){
  .ch, .ch.plain{grid-template-columns:18px minmax(0,1fr)}
  .ch-who,.ch-live,.ch-pending{justify-self:start;text-align:left;grid-column:2}
}
div.stButton > button {
  font-family: Georgia,serif; background:#7a5c1a; color:#f7ecd6;
  border:1px solid #6b4f14; border-radius:2px; padding:.5rem 1.5rem;
  letter-spacing:.06em;
}
div.stButton > button:hover { background:#8f6d20; color:#fff8e8; border-color:#7a5c1a; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)
st.markdown(mindmap.colour_css(), unsafe_allow_html=True)

D = load()

if "view" not in st.session_state:
    st.session_state.view = "home"
if "subject" not in st.session_state:
    st.session_state.subject = None
if "step" not in st.session_state:
    st.session_state.step = 0
if "revealed" not in st.session_state:
    st.session_state.revealed = False
if "attempted" not in st.session_state:
    st.session_state.attempted = False

# Navigation arrives as a query param: ?s=<subject> or ?t=<lesson>. Consume it
# once and clear it, so a later rerun doesn't bounce back to the same screen.
_subject = st.query_params.get("s")
_lesson = st.query_params.get("t")
if _subject or _lesson:
    st.query_params.clear()
if _subject and mindmap.subject_by_key(_subject):
    st.session_state.view = "subject"
    st.session_state.subject = _subject
elif _lesson == "algebra":
    st.session_state.view = "lesson"
    st.session_state.step = 0
    st.session_state.revealed = False
    st.session_state.attempted = False


def header(eyebrow, title, subtitle=None):
    st.markdown(f'<div class="eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="title">{title}</h1>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="subtitle">{subtitle}</div>', unsafe_allow_html=True)
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)


# ---------------------------------------------------------------- SVG panels

def svg_completing_square(stage):
    """al-Khwārizmī's geometric proof of x² + 10x = 39, in three stages.

    stage 1: the square with ten roots attached as one strip
    stage 2: the ten split into two fives, laid on two sides — the L
    stage 3: the missing 5x5 corner supplied — a true square, 64
    """
    X, U = 150.0, 15.0          # side of x-square (px), px per unit
    ox, oy = 60, 60
    ink, gold = "#2c2216", "#b8860b"
    fill_sq = "#e9dcc0"
    fill_strip = "#dcc9a0"
    fill_corner = "#c9a227"

    s = [f'<svg viewBox="0 0 520 330" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="Georgia,serif">']
    s.append(f'<rect width="520" height="330" fill="none"/>')

    # the x² square — always present
    s.append(f'<rect x="{ox}" y="{oy}" width="{X}" height="{X}" fill="{fill_sq}" '
             f'stroke="{ink}" stroke-width="1.6"/>')
    s.append(f'<text x="{ox+X/2}" y="{oy+X/2+7}" text-anchor="middle" '
             f'font-size="21" fill="{ink}" font-style="italic">x²</text>')
    s.append(f'<text x="{ox+X/2}" y="{oy-12}" text-anchor="middle" font-size="14" '
             f'fill="#6b5535" font-style="italic">x</text>')

    if stage == 1:
        w = 10 * U
        s.append(f'<rect x="{ox+X}" y="{oy}" width="{w}" height="{X}" fill="{fill_strip}" '
                 f'stroke="{ink}" stroke-width="1.6"/>')
        s.append(f'<text x="{ox+X+w/2}" y="{oy+X/2+6}" text-anchor="middle" '
                 f'font-size="17" fill="{ink}" font-style="italic">10x</text>')
        s.append(f'<text x="{ox+X+w/2}" y="{oy-12}" text-anchor="middle" font-size="13" '
                 f'fill="#6b5535">10</text>')
        cap = "A square, and ten roots laid beside it. Not yet a square."

    else:
        w = 5 * U
        # right strip
        s.append(f'<rect x="{ox+X}" y="{oy}" width="{w}" height="{X}" fill="{fill_strip}" '
                 f'stroke="{ink}" stroke-width="1.6"/>')
        s.append(f'<text x="{ox+X+w/2}" y="{oy+X/2+6}" text-anchor="middle" '
                 f'font-size="15" fill="{ink}" font-style="italic">5x</text>')
        # bottom strip
        s.append(f'<rect x="{ox}" y="{oy+X}" width="{X}" height="{w}" fill="{fill_strip}" '
                 f'stroke="{ink}" stroke-width="1.6"/>')
        s.append(f'<text x="{ox+X/2}" y="{oy+X+w/2+6}" text-anchor="middle" '
                 f'font-size="15" fill="{ink}" font-style="italic">5x</text>')
        s.append(f'<text x="{ox+X+w/2}" y="{oy-12}" text-anchor="middle" font-size="13" '
                 f'fill="#6b5535">5</text>')

        if stage == 2:
            s.append(f'<rect x="{ox+X}" y="{oy+X}" width="{w}" height="{w}" fill="none" '
                     f'stroke="{gold}" stroke-width="1.6" stroke-dasharray="5 4"/>')
            s.append(f'<text x="{ox+X+w/2}" y="{oy+X+w/2+6}" text-anchor="middle" '
                     f'font-size="24" fill="{gold}">?</text>')
            cap = "Halve the ten. Two strips of five — an L. One corner is missing."
        else:
            s.append(f'<rect x="{ox+X}" y="{oy+X}" width="{w}" height="{w}" fill="{fill_corner}" '
                     f'stroke="{ink}" stroke-width="1.6"/>')
            s.append(f'<text x="{ox+X+w/2}" y="{oy+X+w/2+6}" text-anchor="middle" '
                     f'font-size="15" fill="#2c2216">25</text>')
            # outer brace
            s.append(f'<rect x="{ox}" y="{oy}" width="{X+w}" height="{X+w}" fill="none" '
                     f'stroke="{gold}" stroke-width="2.4"/>')
            s.append(f'<text x="{ox+(X+w)/2}" y="{oy+X+w+30}" text-anchor="middle" '
                     f'font-size="16" fill="#7a5c1a" font-style="italic">'
                     f'(x + 5)² = 39 + 25 = 64</text>')
            s.append(f'<text x="{ox+(X+w)/2}" y="{oy+X+w+52}" text-anchor="middle" '
                     f'font-size="16" fill="#1f5e3d">x + 5 = 8  →  x = 3</text>')
            cap = "Supply the corner — 25. Now it is a true square: 64. Its side is 8."

    s.append("</svg>")
    return "".join(s), cap


def svg_overlap():
    """The −4 in x² + 6x + 5, shown as the corner borrowed but not owned."""
    X, U, ox, oy = 130.0, 16.0, 60, 45
    ink, gold, red = "#2c2216", "#b8860b", "#8b2635"
    w = 3 * U
    s = [f'<svg viewBox="0 0 460 290" xmlns="http://www.w3.org/2000/svg" font-family="Georgia,serif">']
    s.append(f'<rect x="{ox}" y="{oy}" width="{X}" height="{X}" fill="#e9dcc0" stroke="{ink}" stroke-width="1.6"/>')
    s.append(f'<text x="{ox+X/2}" y="{oy+X/2+7}" text-anchor="middle" font-size="19" fill="{ink}" font-style="italic">x²</text>')
    s.append(f'<rect x="{ox+X}" y="{oy}" width="{w}" height="{X}" fill="#dcc9a0" stroke="{ink}" stroke-width="1.6"/>')
    s.append(f'<text x="{ox+X+w/2}" y="{oy+X/2+6}" text-anchor="middle" font-size="14" fill="{ink}" font-style="italic">3x</text>')
    s.append(f'<rect x="{ox}" y="{oy+X}" width="{X}" height="{w}" fill="#dcc9a0" stroke="{ink}" stroke-width="1.6"/>')
    s.append(f'<text x="{ox+X/2}" y="{oy+X+w/2+6}" text-anchor="middle" font-size="14" fill="{ink}" font-style="italic">3x</text>')
    # the borrowed corner
    s.append(f'<rect x="{ox+X}" y="{oy+X}" width="{w}" height="{w}" fill="#f2d9d9" stroke="{red}" stroke-width="1.8" stroke-dasharray="5 3"/>')
    s.append(f'<text x="{ox+X+w/2}" y="{oy+X+w/2+6}" text-anchor="middle" font-size="15" fill="{red}">9</text>')
    s.append(f'<rect x="{ox}" y="{oy}" width="{X+w}" height="{X+w}" fill="none" stroke="{gold}" stroke-width="2.4"/>')
    s.append(f'<text x="{ox+X+w+30}" y="{oy+X+w/2+5}" font-size="14" fill="{red}">borrowed 9</text>')
    s.append(f'<text x="{ox+X+w+30}" y="{oy+X+w/2+26}" font-size="14" fill="{ink}">owned only 5</text>')
    s.append(f'<text x="{ox+X+w+30}" y="{oy+X+w/2+47}" font-size="15" fill="{red}" font-weight="bold">give back 4</text>')
    s.append(f'<text x="{ox+(X+w)/2}" y="{oy+X+w+34}" text-anchor="middle" font-size="16" fill="#7a5c1a" font-style="italic">(x + 3)² − 4</text>')
    s.append("</svg>")
    return "".join(s)


def show_svg(markup, caption=None):
    st.markdown(
        f'<div class="panel" style="text-align:center">{markup}'
        + (f'<div style="font-family:Georgia,serif;font-style:italic;color:#6b5535;'
           f'font-size:.95rem;margin-top:.4rem">{caption}</div>' if caption else "")
        + "</div>",
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------ screens

def screen_manuscript():
    header(
        "Bayt al-Ḥikma · Baghdad · c. 820 CE",
        "Mīrāth al-Ḥikma",
        "One page of al-Khwārizmī. One Cambridge objective. Nothing invented in between.",
    )
    c1, c2 = st.columns([1, 1.05], gap="large")
    with c1:
        b = img_b64(D["source"]["arabic_image"])
        if b:
            st.markdown(
                f'<div class="panel" style="padding:.7rem"><img src="data:image/jpeg;base64,{b}" '
                f'style="width:100%;border:1px solid #cbb489"/></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="panel"><p><em>Manuscript scan unavailable.</em></p></div>',
                        unsafe_allow_html=True)
    with c2:
        s = D["source"]
        st.markdown(
            f'<div class="panel"><h3>The source</h3>'
            f'<p class="dropcap"><em>{s["work"]}</em> — the Compendious Book on Calculation '
            f'by Restoration and Balancing, written by <span class="gold">{s["author"]}</span> '
            f'in {s["composed"]}.</p>'
            f'<p>Its title, <em>al-jabr</em>, became the word <span class="gold">algebra</span>. '
            f'Its author\'s name, Latinised as <em>algorismus</em>, became the word '
            f'<span class="gold">algorithm</span> — and the name of this hackathon.</p>'
            f'<div class="cite">{s["edition"]}<br/>{s["arabic_locator"]} · {s["licence"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="panel"><h3>Where this is going</h3>'
            f'<p>Cambridge IGCSE Mathematics 0580, objective '
            f'<span class="gold">{D["objective"]["code"]}</span>:</p>'
            f'<p style="font-style:italic">“{D["objective"]["syllabus_verbatim"]}”</p>'
            f'<div class="cite">Syllabus for 2025–2027, p.{D["objective"]["syllabus_page"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def screen_unlock():
    header("Layer One · Unlock", "The page, read",
           "A vision pass at build time. Frozen — nothing is generated while you watch.")
    u = D["unlock"]
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(
            f'<div class="panel"><h3>Transcription — Arabic</h3>'
            f'<div class="arabic">{u["arabic_transcription"]}</div>'
            f'<div class="cite">{D["source"]["arabic_locator"]}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="panel"><h3>Translation — English</h3>'
            f'<p>{u["our_translation"]}</p>'
            f'<div class="cite">Produced by the pipeline. Not yet trusted — '
            f'the next screen tests it.</div></div>',
            unsafe_allow_html=True,
        )


def screen_critic():
    header("Layer One · Verify", "The critic",
           "The number below is computed in code from two texts. No model reports its own confidence.")
    r = critic.score(D["unlock"]["our_translation"], D["critic"]["benchmark_text"])
    band = {"high": "", "medium": " med", "fail": " bad"}[r["band"]]

    c1, c2 = st.columns([1, 1.7], gap="large")
    with c1:
        st.markdown(
            f'<div class="panel" style="text-align:center">'
            f'<div class="score-num{band}">{r["percent"]}%</div>'
            f'<div class="verdict">{r["verdict"].split("—")[0].strip()}</div>'
            f'<div style="font-family:Georgia,serif;font-size:.86rem;color:#6b5535;margin-top:.9rem">'
            f'claim agreement <span class="gold">{r["claim_agreement"]:.2f}</span><br/>'
            f'lexical overlap <span class="gold">{r["lexical_overlap"]:.2f}</span><br/>'
            f'sequence ratio <span class="gold">{r["sequence_ratio"]:.2f}</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c2:
        chips = "".join(
            f'<span class="chip{" ok" if d["agree"] else ""}">'
            f'{"✓" if d["agree"] else "✗"} {d["term"]}</span>'
            for d in r["detail"]
        )
        st.markdown(
            f'<div class="panel"><h3>Load-bearing claims, checked one by one</h3>'
            f'<p>Every number the method depends on, present in our reading and in the '
            f'benchmark translation. A fluent paraphrase that loses one of these scores '
            f'worse than clumsy prose that keeps them all.</p>'
            f'<div style="margin:.8rem 0">{chips}</div>'
            f'<p style="font-size:.94rem">{r["verdict"]}</p>'
            f'<div class="cite">Benchmark: {D["critic"]["benchmark_citation"]} — '
            f'{D["source"]["edition"]}</div></div>',
            unsafe_allow_html=True,
        )
    with st.expander("Show the benchmark text"):
        st.markdown(f'<div class="panel"><p>{D["critic"]["benchmark_text"]}</p></div>',
                    unsafe_allow_html=True)


def screen_mirath():
    header("Lesson · Mīrāth", "Whose you are",
           "The inheritance — and the tier it sits in.")
    L = D["lineage"]
    st.markdown(f'<span class="tier1">{L["tier_label"]} {L["confidence_mark"]}</span>',
                unsafe_allow_html=True)
    st.markdown("<div style='height:.9rem'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.4, 1], gap="large")
    with c1:
        st.markdown(
            f'<div class="panel"><h3>{L["thinker"]}</h3>'
            f'<p style="font-style:italic;color:#6b5535">{L["place_time"]}</p>'
            f'<p>{L["contribution"]}</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="panel"><h3>How he thought</h3>'
            f'<p class="dropcap">{L["how_they_thought"]}</p>'
            f'<div class="cite">{L["citation"]}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="panel"><h3>Why this tier</h3>'
            f'<p>Tier 1 means the thread is <span class="gold">direct</span> — not a '
            f'precursor, not a flourish. This topic is his.</p>'
            f'<p>Where no such thread exists, we say so and teach another great mind. '
            f'Where no single originator exists, we drop the hero entirely and teach '
            f'the method alone.</p>'
            f'<p style="font-size:.93rem;color:#6b5535"><em>The tier is set by hand when '
            f'the node is built. It is never decided by a model at runtime.</em></p>'
            f'</div>',
            unsafe_allow_html=True,
        )


def screen_miftah():
    header("Lesson · Miftāḥ", "The key",
           "The thinking move that cracks it — think how he thought.")
    A = D["algorithm"]
    c1, c2 = st.columns([1.15, 1], gap="large")
    with c1:
        steps = "".join(f"<li>{s}</li>" for s in A["steps"])
        st.markdown(
            f'<div class="panel"><h3>{A["name"]}</h3>'
            f'<ol class="steps">{steps}</ol></div>',
            unsafe_allow_html=True,
        )
    with c2:
        qs = "".join(f'<div class="socratic">{q}</div>' for q in A["socratic_prompts"])
        st.markdown(f'<div class="panel"><h3>Asked, not told</h3>{qs}</div>',
                    unsafe_allow_html=True)

    st.markdown('<div style="height:.4rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">His own proof — he did not assert it, he drew it</div>',
                unsafe_allow_html=True)

    if not st.session_state.revealed:
        m, cap = svg_completing_square(2)
        show_svg(m, cap)
        if st.button("I don't get it yet →", key="reveal"):
            st.session_state.revealed = True
            st.rerun()
    else:
        cols = st.columns(3, gap="small")
        for i, col in enumerate(cols, start=1):
            m, cap = svg_completing_square(i)
            with col:
                st.markdown(
                    f'<div class="panel" style="text-align:center;padding:.8rem">{m}'
                    f'<div style="font-family:Georgia,serif;font-style:italic;'
                    f'color:#6b5535;font-size:.86rem">{cap}</div></div>',
                    unsafe_allow_html=True,
                )


def screen_jisr():
    header("Lesson · Jisr", "Carried across",
           "The same move, in the form the exam demands.")
    C = D["cambridge_form"]
    c1, c2 = st.columns(2, gap="large")
    with c1:
        steps = "".join(f"<li>{s}</li>" for s in C["method"])
        st.markdown(
            f'<div class="panel"><h3>Cambridge {C["objective_code"]}</h3>'
            f'<p style="font-style:italic">“{C["statement"]}”</p>'
            f'<ol class="steps">{steps}</ol>'
            f'<p style="text-align:center;font-size:1.06rem;color:#7a5c1a">'
            f'<strong>{C["general_result"]}</strong></p>'
            f'<div class="cite">{C["command_words"]}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        w = C["khwarizmi_worked"]
        rows = "".join(f"<li>{s}</li>" for s in w["steps"])
        st.markdown(
            f'<div class="panel"><h3>His example, in modern notation</h3>'
            f'<p style="font-size:1.3rem;text-align:center;color:#2c2216">'
            f'<strong>{w["problem"]}</strong></p>'
            f'<ol class="steps">{rows}</ol>'
            f'<p style="text-align:center;color:#1f5e3d;font-size:1.1rem">'
            f'<strong>{w["answer"]}</strong></p></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="panel"><p style="font-size:.95rem">Twelve centuries apart, '
            f'the same six moves. The syllabus did not invent this method — '
            f'it inherited it.</p></div>',
            unsafe_allow_html=True,
        )


def screen_apply():
    header("Apply", "Now you do it",
           "The flow ends here — not with an explanation, with your attempt.")
    A = D["apply"]
    c1, c2 = st.columns([1, 1.1], gap="large")
    with c1:
        st.markdown(
            f'<div class="panel"><h3>Cambridge {D["objective"]["related_code"]}</h3>'
            f'<p style="font-size:1.35rem;text-align:center;color:#2c2216">'
            f'<strong>{A["problem"]}</strong></p>'
            f'<div class="socratic">{A["hint"]}</div></div>',
            unsafe_allow_html=True,
        )
        if not st.session_state.attempted:
            st.markdown('<p style="font-family:Georgia,serif;font-style:italic;'
                        'color:#6b5535">Try it on paper first. The solution is hidden '
                        'on purpose.</p>', unsafe_allow_html=True)
            if st.button("I've tried it — show me →", key="apply_reveal"):
                st.session_state.attempted = True
                st.rerun()
    with c2:
        if st.session_state.attempted:
            steps = "".join(f"<li>{s}</li>" for s in A["reveal_steps"])
            st.markdown(
                f'<div class="panel"><h3>The overlap</h3>'
                f'<ol class="steps">{steps}</ol>'
                f'<p style="text-align:center;color:#1f5e3d;font-size:1.12rem">'
                f'<strong>{A["answer"]}</strong></p>'
                f'<div class="cite">{A["mark_scheme"]}</div></div>',
                unsafe_allow_html=True,
            )
            show_svg(svg_overlap())
        else:
            st.markdown(
                '<div class="panel" style="text-align:center;padding:3.5rem 1rem">'
                '<p style="color:#a08c60;font-style:italic">The worked solution appears '
                'once you have attempted it.</p></div>',
                unsafe_allow_html=True,
            )

    if st.session_state.attempted:
        st.markdown(
            '<div class="panel" style="text-align:center;border-color:#c9a227">'
            '<p style="font-size:1.12rem">You did not watch someone solve it. '
            'You solved it — with a method written down in Baghdad twelve centuries ago.</p>'
            '<p class="gold" style="font-size:1.25rem;letter-spacing:.06em">'
            'You are its <em>wārith</em>.</p></div>',
            unsafe_allow_html=True,
        )


def screen_home():
    st.markdown('<div class="eyebrow">Mīrāth al-Ḥikma</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="title" style="font-size:3.6rem;line-height:1.05">'
                'Inheritance of Wisdom</h1>', unsafe_allow_html=True)
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="panel"><p class="dropcap" style="font-size:1.1rem">'
        'Build your thought process. Every topic on your syllabus was cracked by '
        'someone — and the way they thought is a <span class="gold">blueprint</span> '
        'you can borrow. This trains your mind on those blueprints, then puts you to '
        'work with them on the exact problems Cambridge sets.</p>'
        '<p>Where a scholar of the Muslim world stands behind a topic, you meet them '
        'first. Where one does not, we say so and hand you another great mind — or '
        'the method alone. Nothing here is invented to make a story tidier.</p></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height:1.4rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">What do you want to learn today?</div>',
                unsafe_allow_html=True)
    st.markdown(mindmap.render_subject_cards(), unsafe_allow_html=True)


def screen_subject():
    key = st.session_state.subject
    s = mindmap.subject_by_key(key)
    if not s:
        st.session_state.view = "home"
        st.rerun()
    name, code, colour, chapters = s
    d, p, total, live = mindmap.subject_stats(chapters)

    header(f"Cambridge IGCSE {code}", name,
           f"{total} chapters. {d + p} carry a thread back to the Muslim world — "
           f"and the rest are named honestly.")

    st.markdown(mindmap.render_chapters(key), unsafe_allow_html=True)

    st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(
            f'<div class="panel"><h3>Reading the marks</h3>'
            f'<p><strong>Filled circle</strong> — direct lineage: the field was shaped '
            f'in the Muslim world. <strong>Hollow circle</strong> — precursor: an early '
            f'or partial contribution, and we mark the difference rather than blur it.</p>'
            f'<p>Chapters with a dash are on the syllabus and not on the heritage map. '
            f'They are taught through the <span class="gold">algorithm of the topic</span> '
            f'— the thinking method — which exists for every chapter regardless.</p></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="panel"><h3>What is actually built</h3>'
            f'<p>{live} of {total} chapters in {name} has a finished lesson. '
            f'The others show their lineage because the curation is done — '
            f'the lesson is not.</p>'
            f'<p>Every chapter title on this page was checked word-for-word against '
            f'the Cambridge syllabus. A project whose claim is honesty does not get '
            f'to paraphrase the source.</p></div>',
            unsafe_allow_html=True,
        )
    return


RENDER = [screen_manuscript, screen_unlock, screen_critic,
          screen_mirath, screen_miftah, screen_jisr, screen_apply]

if st.session_state.view == "home":
    screen_home()
    st.stop()

if st.session_state.view == "subject":
    screen_subject()
    st.markdown('<div style="height:.6rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    if st.button("← All subjects", key="tohome"):
        st.session_state.view = "home"
        st.session_state.subject = None
        st.rerun()
    st.stop()

RENDER[st.session_state.step]()

# ------------------------------------------------------------------- nav
st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
nav1, nav2, nav3 = st.columns([1, 2.4, 1])
with nav1:
    if st.session_state.step > 0:
        if st.button("← Back", key="back"):
            st.session_state.step -= 1
            st.rerun()
    elif st.button("← Chapters", key="tosubject"):
        st.session_state.view = "subject"
        st.session_state.subject = st.session_state.subject or "maths"
        st.rerun()
with nav2:
    dots = " · ".join(
        f'<span style="color:{"#b8860b" if i == st.session_state.step else "#c9bfa4"}">{n}</span>'
        for i, n in enumerate(SCREENS)
    )
    st.markdown(f'<div class="progress" style="text-align:center">{dots}</div>',
                unsafe_allow_html=True)
with nav3:
    if st.session_state.step < len(SCREENS) - 1:
        if st.button("Next →", key="next"):
            st.session_state.step += 1
            st.rerun()
