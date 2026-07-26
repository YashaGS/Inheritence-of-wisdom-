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

import ask
import critic
import mindmap

ROOT = Path(__file__).parent
# A lesson with a primary source walks all seven screens. One without a
# manuscript skips Unlock and Critic rather than inventing a source to verify.
SCREENS_SOURCE = ["Manuscript", "Unlock", "Critic", "Mīrāth", "Miftāḥ", "Jisr", "Apply"]
SCREENS_PLAIN = ["Mīrāth", "Miftāḥ", "Jisr", "Apply"]
# A lesson with a story opens on it: the story carries the manuscript and the
# lineage together, so Manuscript and Mīrāth are not separate stops.
SCREENS_FULL = ["Mīrāth", "Unlock", "Critic", "Miftāḥ", "Shapes", "Jisr", "Key words", "Practice"]
SCREENS_STORY = ["Mīrāth", "Miftāḥ", "Jisr", "Key words", "Practice"]

st.set_page_config(
    page_title="Mīrāth al-Ḥikma · Algorism",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load(lesson_id):
    path = ROOT / "content" / "lessons" / f"{lesson_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def lesson_ids():
    return sorted(p.stem for p in (ROOT / "content" / "lessons").glob("*.json"))


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
.tier1.t2 { background:#4a5f6b; }
.panel.honest { border-left:4px solid #4a5f6b; background:linear-gradient(#fbf5e6,#f4ead2); }
.panel.honest h3 { color:#3f5561; }
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

/* ---- key words ---- */
.kwrow{
  display:grid;grid-template-columns:minmax(88px,auto) 1fr;gap:.2rem .9rem;
  padding:.5rem 0;border-top:1px solid #e8dcc0;
}
.kwrow:first-of-type{border-top:0}
.kw-cmd{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;font-size:.98rem;
  color:#7a5c1a;font-weight:600;
}
.kw-term{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;font-size:.98rem;color:#2c2216;
}
.kw-def{font-family:Georgia,serif;font-size:.9rem;line-height:1.55;color:#5a4726}
.kw-def strong{color:#7a5c1a}
@media(max-width:700px){
  .kwrow{grid-template-columns:1fr}
  .kw-def{grid-column:1}
}

/* ---- worked examples ---- */
.ex-q{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;font-size:1.34rem;
  color:#2c2216;text-align:center;margin:0 0 .9rem;
}
.ex-a{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;font-size:1.08rem;
  color:#1f5e3d;text-align:center;margin:.4rem 0 0;
}

/* ---- practice ---- */
.prac-count{font-family:Georgia,serif;font-size:.9rem;color:#7a5c1a;font-weight:600}
.prac-hint{font-family:Georgia,serif;font-size:.9rem;color:#6b5535;font-style:italic}
.prac{
  display:flex;align-items:baseline;gap:.75rem;flex-wrap:wrap;
  background:linear-gradient(#fdf7e9,#f7ecd6);border:1px solid #dcc9a0;
  border-radius:3px;padding:.8rem 1rem;margin-bottom:.55rem;min-height:3.5rem;
}
.prac-n{
  flex:0 0 auto;width:1.6rem;height:1.6rem;border-radius:50%;
  background:#f0e2c0;border:1px solid #c9a227;color:#7a5c1a;
  font-family:Georgia,serif;font-size:.82rem;
  display:flex;align-items:center;justify-content:center;
}
.prac-q{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;font-size:1.1rem;color:#2c2216;flex:1 1 auto;
}
.prac-t{
  font-family:Georgia,serif;font-size:.74rem;color:#a3937a;font-style:italic;flex:1 1 100%;
}
.prac-a{
  background:#f2e6c9;border:1px solid #dcc9a0;border-left:3px solid #1f5e3d;
  border-radius:3px;padding:.8rem 1rem;margin-bottom:.55rem;min-height:3.5rem;
  display:flex;flex-direction:column;gap:.25rem;
}
.pf{font-family:'Iowan Old Style',Palatino,Georgia,serif;font-size:1.04rem;color:#5a4726}
.pa{font-family:Georgia,serif;font-size:.92rem;color:#1f5e3d}

/* ---- subtopic landing ---- */
.landing-q{border-left:4px solid #b8860b}
.landing-q .statement{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;
  font-size:1.72rem;line-height:1.3;color:#2c2216;margin:0;text-wrap:balance;
}
.landing-cta p{font-size:.98rem;color:#5a4726;margin:0}

/* ---- story: the primary-source quote ---- */
blockquote.pq{
  margin:.9rem 0 0;padding:.9rem 1.2rem;border-left:3px solid #b8860b;
  background:#f6ecd4;font-family:Georgia,serif;font-style:italic;
  font-size:1.02rem;line-height:1.7;color:#3f3220;
}

/* ---- pinned Ask panel (sidebar) ---- */
section[data-testid="stSidebar"]{
  background:linear-gradient(#f7ecd6,#f1e3c4);border-right:1px solid #dcc9a0;
}
section[data-testid="stSidebar"] .block-container{padding-top:2rem}
.ask-head{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;font-size:1.5rem;
  color:#2c2216;margin:0 0 .2rem;
}
.ask-note{
  font-family:Georgia,serif;font-size:.78rem;color:#8a7550;font-style:italic;
  line-height:1.5;margin:0 0 1rem;
}
section[data-testid="stSidebar"] div.stButton > button{
  background:#fdf7e9;color:#4a3a1c;border:1px solid #dcc9a0;
  font-family:Georgia,serif;font-size:.86rem;text-align:left;
  padding:.5rem .7rem;line-height:1.35;letter-spacing:0;
}
section[data-testid="stSidebar"] div.stButton > button:hover{
  background:#f6e2b0;border-color:#b8860b;color:#2c2216;
}
section[data-testid="stSidebar"] input{
  font-family:Georgia,serif;background:#fdf7e9;border:1px solid #dcc9a0;color:#2c2216;
}
.ask-a{
  margin-top:1rem;background:#fdf7e9;border:1px solid #dcc9a0;
  border-left:3px solid #1f5e3d;border-radius:3px;padding:.85rem 1rem;
}
.ask-a.refused{border-left-color:#8b2635;background:#faf1e4}
.ask-q{
  font-family:Georgia,serif;font-size:.8rem;font-style:italic;color:#8a7550;
  margin-bottom:.45rem;
}
.ask-a p{font-family:Georgia,serif;font-size:.92rem;line-height:1.6;color:#33281a;margin:0}

.tagline{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;
  font-size:1.28rem;line-height:1.4;color:#6b5535;
  margin:.45rem 0 1.1rem;text-wrap:balance;
}
.tagline em{font-style:italic;color:#9a7b2e}

/* ---- home: hero statement ---- */
.hero{margin:0 0 2rem;max-width:64ch}
.hero .punch{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;
  font-size:clamp(1.6rem,3.1vw,2.25rem);line-height:1.22;font-weight:600;
  color:#2c2216;margin:0 0 1.1rem;text-wrap:balance;
}
.hero .punch em{font-style:normal;color:#9a7b2e}
.hero p{font-family:Georgia,serif;font-size:1.04rem;line-height:1.7;color:#33281a;margin:0 0 .85rem}
.hero .names{color:#6b5535}
.hero .names b{color:#7a5c1a;font-weight:600}
/* Rubrication, not a highlighter pen: a gold wash sitting under the baseline,
   the way an illuminated manuscript marks the line that matters. */
.hero .mark{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;
  font-size:1.16rem;font-weight:600;color:#2c2216;
  background:linear-gradient(180deg,transparent 62%,rgba(184,134,11,.32) 62%);
  padding:0 .12em;box-decoration-break:clone;-webkit-box-decoration-break:clone;
}
.hero .kicker{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;
  font-size:1.16rem;line-height:1.5;color:#2c2216;
  border-left:3px solid #b8860b;padding:.5rem 0 .5rem 1rem;margin:1.2rem 0 0;
}

/* ---- home: three expandable brief cards ---- */
.brief-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:0 0 2rem}
@media(max-width:900px){.brief-grid{grid-template-columns:1fr}}
.brief{
  background:linear-gradient(#fdf7e9,#f7ecd6);border:1px solid #dcc9a0;
  border-top:3px solid #b8860b;border-radius:3px;padding:1.25rem 1.3rem 1rem;
  box-shadow:0 1px 3px rgba(90,70,30,.14);
}
.brief h4{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;font-size:1.08rem;
  margin:0 0 .55rem;color:#7a5c1a;font-weight:600;
}
.brief p{font-family:Georgia,serif;font-size:.95rem;line-height:1.62;color:#33281a;margin:0 0 .7rem}
.brief .lead{color:#2c2216}
.brief details{margin-top:.2rem}
.brief details p:last-child{margin-bottom:0}
.brief summary{
  font-family:Georgia,serif;font-size:.82rem;letter-spacing:.08em;text-transform:uppercase;
  color:#9a7b2e;cursor:pointer;list-style:none;padding:.3rem 0;user-select:none;
}
.brief summary::-webkit-details-marker{display:none}
.brief summary::after{content:" ↓";font-size:.9em}
.brief details[open] summary::after{content:" ↑"}
.brief summary:hover{color:#b8860b}
.brief summary:focus-visible{outline:2px solid #b8860b;outline-offset:2px}
.brief details[open] summary{margin-bottom:.5rem;border-bottom:1px solid #e5d6b4}
.brief strong{color:#7a5c1a}

.strip{
  display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:1.6rem 0 0;
}
@media(max-width:900px){.strip{grid-template-columns:1fr}}
.strip .s{
  background:linear-gradient(#fdf7e9,#f7ecd6);border:1px solid #dcc9a0;border-radius:3px;
  padding:1.1rem 1.2rem;
}
.strip .s b{
  display:block;font-family:'Iowan Old Style',Palatino,Georgia,serif;
  font-size:1rem;color:#7a5c1a;margin-bottom:.3rem;letter-spacing:.05em;
}
.strip .s span{font-family:Georgia,serif;font-size:.9rem;line-height:1.58;color:#33281a}
.contrast{
  background:linear-gradient(#fdf7e9,#f7ecd6);border:1px solid #c9a227;border-radius:3px;
  padding:1.4rem 1.6rem;margin:1.6rem 0 0;
}
.contrast p{font-family:Georgia,serif;font-size:1.02rem;line-height:1.66;margin:0 0 .6rem;color:#33281a}
.contrast p:last-child{margin-bottom:0}
.contrast .promise{font-size:1.12rem;color:#2c2216}

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

/* ---- home: the lesson arc ---- */
.arc{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:.4rem 0 2rem}
@media(max-width:820px){.arc{grid-template-columns:repeat(2,minmax(0,1fr))}}
.arc .step{
  position:relative;background:linear-gradient(#fdf7e9,#f7ecd6);
  border:1px solid #dcc9a0;border-radius:3px;padding:.95rem 1rem;
}
.arc .step .ar{
  font-family:'Geeza Pro','Al Bayan','Amiri',serif;direction:rtl;
  font-size:1.32rem;color:#7a5c1a;display:block;line-height:1.5;
}
.arc .step .tr{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;font-size:1.02rem;
  color:#2c2216;display:block;margin-top:.1rem;
}
.arc .step .en{
  font-family:Georgia,serif;font-size:.8rem;color:#9a8358;font-style:italic;
  display:block;margin-bottom:.35rem;
}
.arc .step .what{font-family:Georgia,serif;font-size:.86rem;color:#6b5535;line-height:1.5;display:block;margin-top:.3rem}
.arc .step::after{
  content:"→";position:absolute;right:-11px;top:50%;transform:translateY(-50%);
  color:#c9a227;font-size:1rem;z-index:2;
}
.arc .step:last-child::after{content:""}
@media(max-width:820px){.arc .step::after{content:""}}

/* ---- subject page: chapter cards ---- */
.chap-list{display:flex;flex-direction:column;gap:10px}
.chap{
  display:block;padding:1.05rem 1.2rem;border-radius:3px;text-decoration:none;
  background:transparent;border:1px solid transparent;
}
.chap.marked{background:linear-gradient(#fdf7e9,#f7ecd6);border-color:#dcc9a0}
.chap.live{border-width:1.8px;background:#f9edcf}
a.chap.live{transition:transform .16s ease,box-shadow .16s ease}
a.chap.live:hover{transform:translateX(3px);box-shadow:0 3px 10px rgba(90,70,30,.18)}
a.chap.live:focus-visible{outline:2px solid #b8860b;outline-offset:2px}
.chap-head{display:flex;align-items:baseline;gap:.7rem;flex-wrap:wrap}
.chap-name{
  font-family:'Iowan Old Style',Palatino,Georgia,serif;
  font-size:1.42rem;line-height:1.25;color:#2c2216;
}
.chap:not(.marked) .chap-name{color:#a3937a;font-size:1.3rem}
/* The work is the inheritance and takes the headline weight; the scholar is
   attribution and sits quieter. Never the other way round. */
.chap-work{
  font-family:Georgia,serif;font-size:1rem;color:#5a4726;line-height:1.4;
  flex:1 1 100%;margin-top:.15rem;
}
.chap-who{
  font-family:Georgia,serif;font-size:.82rem;font-style:italic;color:#a3937a;
  flex:1 1 100%;
}
.chap-who::before{content:"left by ";font-style:normal;color:#bcae90}
.chap-who.plain{color:#bcae90}
.chap-who.plain::before{content:""}
.sub-list{display:flex;flex-wrap:wrap;gap:5px;margin:.7rem 0 0}
.sub{
  font-family:Georgia,serif;font-size:.76rem;color:#6b5535;
  background:#f2e6c9;border:1px solid #e0cfa6;border-radius:2px;padding:.14rem .45rem;
}
.sub i{color:#8a7550;font-style:italic}
.chap:not(.marked) .sub{background:#f3ecdc;border-color:#e6dcc4;color:#a3937a}
.chap:not(.marked) .sub i{color:#b3a586}
.chap-foot{display:flex;flex-wrap:wrap;align-items:center;gap:.6rem;margin:.85rem 0 0}
.chap-cta{
  font-family:Georgia,serif;font-size:.78rem;letter-spacing:.07em;text-transform:uppercase;
  background:#b8860b;color:#fdf7e9;padding:.26rem .7rem;border-radius:2px;
}
.chap-at{font-family:Georgia,serif;font-size:.82rem;color:#6b5535}
.chap-at b{color:#7a5c1a}
.chap-src{
  font-family:Georgia,serif;font-size:.78rem;color:#7a6338;font-style:italic;
  border-left:2px solid #c9a227;padding-left:.55rem;
}
.chap-pending{
  font-family:Georgia,serif;font-size:.76rem;letter-spacing:.06em;
  text-transform:uppercase;color:#a3937a;
}

/* ---- subject page: chapter list (legacy rows) ---- */
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
.ch-dot.tier2{background:#4a5f6b}
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

if "lesson" not in st.session_state:
    st.session_state.lesson = "algebra"

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
elif _lesson and _lesson in lesson_ids():
    st.session_state.lesson = _lesson
    st.session_state.view = "landing"
    st.session_state.step = 0
    st.session_state.revealed = False
    st.session_state.attempted = False

D = load(st.session_state.lesson)
HAS_SOURCE = bool(D.get("has_source"))
HAS_STORY = "story" in D
SCREENS = (SCREENS_FULL if (HAS_STORY and HAS_SOURCE) else
           SCREENS_STORY if HAS_STORY else
           SCREENS_SOURCE if HAS_SOURCE else SCREENS_PLAIN)


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


def svg_bar_magnet():
    """Field around one bar magnet: arrowed loops, N to S, densest at the poles."""
    ink, gold, red, blue = "#2c2216", "#b8860b", "#8b2635", "#2b5f8a"
    cx, cy, mw, mh = 260, 150, 130, 34
    s = ['<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" '
         'font-family="Georgia,serif">',
         '<defs><marker id="ar" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="5" '
         f'markerHeight="5" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{ink}"/>'
         '</marker></defs>']
    for k, (spread, op) in enumerate([(38, .95), (74, .8), (112, .62), (152, .45)]):
        for sgn in (-1, 1):
            y = cy + sgn * spread
            s.append(
                f'<path d="M {cx + mw/2 - 4} {cy} C {cx + mw/2 + spread*0.9} {cy}, '
                f'{cx + spread*0.5} {y}, {cx} {y} C {cx - spread*0.5} {y}, '
                f'{cx - mw/2 - spread*0.9} {cy}, {cx - mw/2 + 4} {cy}" '
                f'fill="none" stroke="{ink}" stroke-width="1.5" stroke-opacity="{op}" '
                f'marker-mid="url(#ar)"/>')
            s.append(
                f'<path d="M {cx + 26} {y} L {cx - 4} {y}" stroke="{ink}" '
                f'stroke-width="1.5" stroke-opacity="{op}" marker-end="url(#ar)"/>')
    s.append(f'<rect x="{cx - mw/2}" y="{cy - mh/2}" width="{mw/2}" height="{mh}" '
             f'fill="{blue}"/>')
    s.append(f'<rect x="{cx}" y="{cy - mh/2}" width="{mw/2}" height="{mh}" fill="{red}"/>')
    s.append(f'<text x="{cx - mw/4}" y="{cy+6}" text-anchor="middle" font-size="16" '
             f'fill="#fdf7e9">S</text>')
    s.append(f'<text x="{cx + mw/4}" y="{cy+6}" text-anchor="middle" font-size="16" '
             f'fill="#fdf7e9">N</text>')
    s.append(f'<text x="{cx}" y="{cy+mh/2+126}" text-anchor="middle" font-size="13" '
             f'fill="#6b5535" font-style="italic">Crowded at the poles — that is where '
             f'the field is strongest</text>')
    s.append("</svg>")
    return "".join(s)


def svg_neutral_point():
    """Two N poles facing: lines turn aside, and a neutral point sits between."""
    ink, gold, red = "#2c2216", "#b8860b", "#8b2635"
    cy, gap = 150, 92
    lx, rx, mw, mh = 150, 370, 96, 32
    s = ['<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" '
         'font-family="Georgia,serif">',
         '<defs><marker id="ar2" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="5" '
         f'markerHeight="5" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{ink}"/>'
         '</marker></defs>']
    mid = (lx + rx) / 2
    for sgn in (-1, 1):
        for k, off in enumerate([26, 54, 86]):
            op = .9 - k * .2
            s.append(
                f'<path d="M {lx + mw/2} {cy} C {mid - 30} {cy + sgn*off*0.35}, '
                f'{mid - 14} {cy + sgn*off}, {mid} {cy + sgn*(off + 26)}" '
                f'fill="none" stroke="{ink}" stroke-width="1.5" stroke-opacity="{op}" '
                f'marker-end="url(#ar2)"/>')
            s.append(
                f'<path d="M {rx - mw/2} {cy} C {mid + 30} {cy + sgn*off*0.35}, '
                f'{mid + 14} {cy + sgn*off}, {mid} {cy + sgn*(off + 26)}" '
                f'fill="none" stroke="{ink}" stroke-width="1.5" stroke-opacity="{op}" '
                f'marker-end="url(#ar2)"/>')
    for x in (lx, rx):
        s.append(f'<rect x="{x - mw/2}" y="{cy - mh/2}" width="{mw}" height="{mh}" '
                 f'fill="{red}"/>')
        s.append(f'<text x="{x}" y="{cy+6}" text-anchor="middle" font-size="15" '
                 f'fill="#fdf7e9">N</text>')
    s.append(f'<circle cx="{mid}" cy="{cy}" r="6" fill="{gold}" stroke="{ink}" '
             f'stroke-width="1.5"/>')
    s.append(f'<text x="{mid}" y="{cy - 16}" text-anchor="middle" font-size="13" '
             f'fill="#7a5c1a">neutral point</text>')
    s.append(f'<text x="{mid}" y="{cy + 118}" text-anchor="middle" font-size="13" '
             f'fill="#6b5535" font-style="italic">Two equal pushes cancel. '
             f'A compass here has no direction to take.</text>')
    s.append("</svg>")
    return "".join(s)


# English letter frequencies, standard published values (percentages).
ENG_FREQ = [("e", 12.7), ("t", 9.1), ("a", 8.2), ("o", 7.5), ("i", 7.0), ("n", 6.7),
            ("s", 6.3), ("h", 6.1), ("r", 6.0), ("d", 4.3), ("l", 4.0), ("c", 2.8)]
CIPHER_SYMS = ["✦", "◈", "▲", "●", "◆", "■", "✚", "◐", "★", "▼", "☰", "◇"]


def svg_frequency():
    """The two rankings side by side. The disguise changes the labels and leaves
    the shape untouched — which is the whole lesson, in one picture."""
    ink, gold, muted = "#2c2216", "#b8860b", "#6b5535"
    W, top_y, bot_y, bar_w, gap = 520, 118, 262, 30, 8
    x0, scale = 34, 6.4
    s = [f'<svg viewBox="0 0 {W} 310" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="Georgia,serif">']

    s.append(f'<text x="{x0}" y="22" font-size="12.5" fill="{muted}" '
             f'font-style="italic">What you intercepted — symbols you cannot read</text>')
    s.append(f'<text x="{x0}" y="{bot_y - 96}" font-size="12.5" fill="{muted}" '
             f'font-style="italic">What English does — frequencies anyone can look up</text>')

    for i, ((letter, freq), sym) in enumerate(zip(ENG_FREQ, CIPHER_SYMS)):
        x = x0 + i * (bar_w + gap)
        h = freq * scale
        # ciphertext bars hang down from the top axis
        s.append(f'<rect x="{x}" y="{top_y - h}" width="{bar_w}" height="{h}" '
                 f'fill="{gold}" fill-opacity=".72"/>')
        s.append(f'<text x="{x + bar_w/2}" y="{top_y + 15}" text-anchor="middle" '
                 f'font-size="14" fill="{ink}">{sym}</text>')
        # english bars grow down from the lower axis
        s.append(f'<rect x="{x}" y="{bot_y}" width="{bar_w}" height="{h}" '
                 f'fill="{ink}" fill-opacity=".55"/>')
        s.append(f'<text x="{x + bar_w/2}" y="{bot_y - 6}" text-anchor="middle" '
                 f'font-size="14" fill="{ink}" font-style="italic">{letter}</text>')
        if i < 2:
            s.append(f'<line x1="{x + bar_w/2}" y1="{top_y + 22}" '
                     f'x2="{x + bar_w/2}" y2="{bot_y - 22}" stroke="{gold}" '
                     f'stroke-width="1.4" stroke-dasharray="3 3"/>')

    s.append(f'<line x1="{x0 - 6}" y1="{top_y}" x2="{W - 20}" y2="{top_y}" '
             f'stroke="{ink}" stroke-width="1"/>')
    s.append(f'<line x1="{x0 - 6}" y1="{bot_y}" x2="{W - 20}" y2="{bot_y}" '
             f'stroke="{ink}" stroke-width="1"/>')
    s.append(f'<text x="{W/2}" y="303" text-anchor="middle" font-size="13" '
             f'fill="{muted}" font-style="italic">Same shape. The cipher changed the '
             f'labels and could not touch the pattern.</text>')
    s.append("</svg>")
    return "".join(s)


INK, GOLD, RED, DIM = "#2c2216", "#b8860b", "#8b2635", "#dcc9a0"
SQ, STRIP, CORNER = "#e9dcc0", "#dcc9a0", "#c9a227"


def _frame(w=430, h=250):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Georgia,serif">')


def svg_type_even(b=10, side=118, unit=7.4):
    """b even and positive: two equal strips, one square corner."""
    h = b / 2 * unit
    ox, oy = 46, 34
    s = [_frame()]
    s.append(f'<rect x="{ox}" y="{oy}" width="{side}" height="{side}" fill="{SQ}" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<text x="{ox+side/2}" y="{oy+side/2+6}" text-anchor="middle" font-size="18" fill="{INK}" font-style="italic">x²</text>')
    s.append(f'<rect x="{ox+side}" y="{oy}" width="{h}" height="{side}" fill="{STRIP}" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<text x="{ox+side+h/2}" y="{oy+side/2+5}" text-anchor="middle" font-size="13" fill="{INK}" font-style="italic">{b//2}x</text>')
    s.append(f'<rect x="{ox}" y="{oy+side}" width="{side}" height="{h}" fill="{STRIP}" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<text x="{ox+side/2}" y="{oy+side+h/2+5}" text-anchor="middle" font-size="13" fill="{INK}" font-style="italic">{b//2}x</text>')
    s.append(f'<rect x="{ox+side}" y="{oy+side}" width="{h}" height="{h}" fill="{CORNER}" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<text x="{ox+side+h/2}" y="{oy+side+h/2+5}" text-anchor="middle" font-size="12" fill="{INK}">{(b//2)**2}</text>')
    s.append(f'<rect x="{ox}" y="{oy}" width="{side+h}" height="{side+h}" fill="none" stroke="{GOLD}" stroke-width="2.2"/>')
    s.append(f'<text x="{ox+(side+h)/2}" y="{oy+side+h+26}" text-anchor="middle" font-size="14" fill="#7a5c1a" font-style="italic">(x + {b//2})² — one square, one corner added</text>')
    s.append("</svg>")
    return "".join(s)


def svg_type_odd(b=5, side=118, unit=13):
    """b odd: the half is a fraction, the corner is a fraction squared."""
    h = b / 2 * unit
    ox, oy = 46, 34
    s = [_frame()]
    s.append(f'<rect x="{ox}" y="{oy}" width="{side}" height="{side}" fill="{SQ}" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<text x="{ox+side/2}" y="{oy+side/2+6}" text-anchor="middle" font-size="18" fill="{INK}" font-style="italic">x²</text>')
    for x, y, w, ht in ((ox+side, oy, h, side), (ox, oy+side, side, h)):
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{ht}" fill="{STRIP}" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<text x="{ox+side+h/2}" y="{oy+side/2+5}" text-anchor="middle" font-size="12" fill="{INK}" font-style="italic">5x/2</text>')
    s.append(f'<text x="{ox+side/2}" y="{oy+side+h/2+5}" text-anchor="middle" font-size="12" fill="{INK}" font-style="italic">5x/2</text>')
    s.append(f'<rect x="{ox+side}" y="{oy+side}" width="{h}" height="{h}" fill="{CORNER}" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<text x="{ox+side+h/2}" y="{oy+side+h/2+4}" text-anchor="middle" font-size="11" fill="{INK}">25/4</text>')
    s.append(f'<rect x="{ox}" y="{oy}" width="{side+h}" height="{side+h}" fill="none" stroke="{GOLD}" stroke-width="2.2"/>')
    s.append(f'<text x="{ox+(side+h)/2}" y="{oy+side+h+26}" text-anchor="middle" font-size="14" fill="#7a5c1a" font-style="italic">(x + 5/2)² — a fractional side is still a side</text>')
    s.append("</svg>")
    return "".join(s)


def svg_type_negative(b=6, side=150, unit=13):
    """b negative: the square is built inside, by cutting strips away."""
    h = b / 2 * unit
    ox, oy = 52, 30
    inner = side - h
    s = [_frame(430, 262)]
    s.append(f'<rect x="{ox}" y="{oy}" width="{side}" height="{side}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    s.append(f'<text x="{ox+side+8}" y="{oy+12}" font-size="12" fill="#8a7550" font-style="italic">x</text>')
    s.append(f'<rect x="{ox}" y="{oy}" width="{inner}" height="{inner}" fill="{SQ}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<text x="{ox+inner/2}" y="{oy+inner/2+6}" text-anchor="middle" font-size="15" fill="{INK}" font-style="italic">(x − 3)²</text>')
    s.append(f'<rect x="{ox+inner}" y="{oy}" width="{h}" height="{inner}" fill="{RED}" fill-opacity=".22" stroke="{RED}" stroke-width="1.3"/>')
    s.append(f'<rect x="{ox}" y="{oy+inner}" width="{inner}" height="{h}" fill="{RED}" fill-opacity=".22" stroke="{RED}" stroke-width="1.3"/>')
    s.append(f'<rect x="{ox+inner}" y="{oy+inner}" width="{h}" height="{h}" fill="{RED}" fill-opacity=".38" stroke="{RED}" stroke-width="1.3"/>')
    s.append(f'<text x="{ox+inner+h/2}" y="{oy+inner+h/2+4}" text-anchor="middle" font-size="11" fill="{RED}">9</text>')
    s.append(f'<text x="{ox+side/2}" y="{oy+side+26}" text-anchor="middle" font-size="14" fill="#7a5c1a" font-style="italic">Cut 3 from each side. The corner is counted twice — add 9 back.</text>')
    s.append("</svg>")
    return "".join(s)


def svg_type_scaled(side=96, unit=8):
    """a ≠ 1: a copies of the same shape, so divide before completing."""
    ox, oy, h = 40, 40, 3 * unit
    s = [_frame(430, 236)]
    for k in (0, 1):
        x = ox + k * (side + h + 26)
        s.append(f'<rect x="{x}" y="{oy}" width="{side}" height="{side}" fill="{SQ}" stroke="{INK}" stroke-width="1.4"/>')
        s.append(f'<text x="{x+side/2}" y="{oy+side/2+5}" text-anchor="middle" font-size="15" fill="{INK}" font-style="italic">x²</text>')
        s.append(f'<rect x="{x+side}" y="{oy}" width="{h}" height="{side}" fill="{STRIP}" stroke="{INK}" stroke-width="1.4"/>')
        s.append(f'<rect x="{x}" y="{oy+side}" width="{side}" height="{h}" fill="{STRIP}" stroke="{INK}" stroke-width="1.4"/>')
        s.append(f'<rect x="{x+side}" y="{oy+side}" width="{h}" height="{h}" fill="{CORNER}" stroke="{INK}" stroke-width="1.4"/>')
        s.append(f'<rect x="{x}" y="{oy}" width="{side+h}" height="{side+h}" fill="none" stroke="{GOLD}" stroke-width="2"/>')
    s.append(f'<text x="{ox+side+h+13}" y="{oy+side/2+6}" text-anchor="middle" font-size="20" fill="{INK}">+</text>')
    s.append(f'<text x="215" y="{oy+side+h+34}" text-anchor="middle" font-size="14" fill="#7a5c1a" font-style="italic">Two identical shapes. Take the 2 out, then complete one.</text>')
    s.append("</svg>")
    return "".join(s)


def svg_type_zero(w=210, h=96):
    """RHS zero: a rectangle of zero area must have a zero side."""
    ox, oy = 60, 46
    s = [_frame(430, 216)]
    s.append(f'<rect x="{ox}" y="{oy}" width="{w}" height="{h}" fill="{STRIP}" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<text x="{ox+w/2}" y="{oy+h/2+6}" text-anchor="middle" font-size="15" fill="{INK}">area = 0</text>')
    s.append(f'<text x="{ox+w/2}" y="{oy-12}" text-anchor="middle" font-size="13" fill="{INK}" font-style="italic">x + 3</text>')
    s.append(f'<text x="{ox-16}" y="{oy+h/2+5}" text-anchor="middle" font-size="13" fill="{INK}" font-style="italic">2x</text>')
    s.append(f'<text x="{ox+w/2}" y="{oy+h+30}" text-anchor="middle" font-size="14" fill="#7a5c1a" font-style="italic">A rectangle with no area has a side of length zero.</text>')
    s.append(f'<text x="{ox+w/2}" y="{oy+h+52}" text-anchor="middle" font-size="13" fill="{RED}">Only works because the other side is 0 — not 39.</text>')
    s.append("</svg>")
    return "".join(s)


EXAMPLE_FIGURES = {"even": svg_type_even, "odd": svg_type_odd,
                   "negative": svg_type_negative, "scaled": svg_type_scaled,
                   "zero": svg_type_zero}


def svg_still():
    """The alembic: heat, vapour rises, condenses, drips out. al-anbiq."""
    ink, gold, red, blue = "#2c2216", "#b8860b", "#8b2635", "#2b6f9a"
    s = ['<svg viewBox="0 0 480 280" xmlns="http://www.w3.org/2000/svg" font-family="Georgia,serif">']
    s.append(f'<path d="M 70 200 a 46 46 0 1 0 92 0 z" fill="#e9dcc0" stroke="{ink}" stroke-width="1.6"/>')
    s.append(f'<rect x="98" y="120" width="36" height="46" fill="none" stroke="{ink}" stroke-width="1.6"/>')
    s.append(f'<path d="M 98 120 q 18 -30 36 0" fill="#f2e6c9" stroke="{ink}" stroke-width="1.6"/>')
    s.append(f'<text x="116" y="230" text-anchor="middle" font-size="12" fill="{ink}">mixture</text>')
    s.append(f'<path d="M 116 236 l -9 16 M 116 236 l 9 16" stroke="{red}" stroke-width="2"/>')
    s.append(f'<text x="116" y="268" text-anchor="middle" font-size="11.5" fill="{red}">heat</text>')
    for k, y in enumerate((150, 136, 122)):
        s.append(f'<path d="M 108 {y} q 8 -7 16 0" fill="none" stroke="{blue}" stroke-width="1.4" stroke-opacity="{.8-k*.18}"/>')
    s.append(f'<path d="M 134 108 L 300 150" stroke="{ink}" stroke-width="1.6" fill="none"/>')
    s.append(f'<path d="M 134 122 L 300 164" stroke="{ink}" stroke-width="1.6" fill="none"/>')
    s.append(f'<text x="212" y="126" text-anchor="middle" font-size="11.5" fill="{blue}">vapour cools →</text>')
    s.append(f'<path d="M 300 150 L 330 158 L 330 172 L 300 164 z" fill="#e9dcc0" stroke="{ink}" stroke-width="1.5"/>')
    s.append(f'<circle cx="342" cy="186" r="3" fill="{blue}"/><circle cx="342" cy="200" r="2.4" fill="{blue}"/>')
    s.append(f'<path d="M 322 214 a 34 30 0 1 0 44 0 z" fill="#eef4f7" stroke="{ink}" stroke-width="1.6"/>')
    s.append(f'<text x="344" y="252" text-anchor="middle" font-size="12" fill="{ink}">pure liquid</text>')
    s.append(f'<text x="240" y="36" text-anchor="middle" font-size="15" fill="#7a5c1a" font-style="italic">The alembic — <tspan font-size="14">al-anbīq</tspan></text>')
    s.append(f'<text x="240" y="58" text-anchor="middle" font-size="12.5" fill="#6b5535">One property exploited: boiling point. Nothing is changed chemically.</text>')
    s.append("</svg>")
    return "".join(s)


def svg_heart():
    """Solid septum, so blood must detour through the lungs."""
    ink, red, blue, gold = "#2c2216", "#a83232", "#2b6f9a", "#b8860b"
    s = ['<svg viewBox="0 0 480 300" xmlns="http://www.w3.org/2000/svg" font-family="Georgia,serif">',
         '<defs><marker id="bl" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="5" markerHeight="5" '
         f'orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{ink}"/></marker></defs>']
    s.append(f'<rect x="150" y="90" width="80" height="150" rx="10" fill="#dce9f2" stroke="{ink}" stroke-width="1.6"/>')
    s.append(f'<rect x="250" y="90" width="80" height="150" rx="10" fill="#f6dede" stroke="{ink}" stroke-width="1.6"/>')
    s.append(f'<rect x="230" y="86" width="20" height="158" fill="{gold}" stroke="{ink}" stroke-width="1.8"/>')
    s.append(f'<text x="240" y="266" text-anchor="middle" font-size="13" fill="#7a5c1a">septum — solid</text>')
    s.append(f'<text x="190" y="120" text-anchor="middle" font-size="12.5" fill="{blue}">RIGHT</text>')
    s.append(f'<text x="290" y="120" text-anchor="middle" font-size="12.5" fill="{red}">LEFT</text>')
    s.append(f'<path d="M 234 150 L 246 150" stroke="{ink}" stroke-width="3"/>')
    s.append(f'<path d="M 228 138 L 252 162 M 252 138 L 228 162" stroke="#8b2635" stroke-width="2.6"/>')
    s.append(f'<text x="240" y="184" text-anchor="middle" font-size="11.5" fill="#8b2635">no way through</text>')
    s.append(f'<ellipse cx="240" cy="46" rx="86" ry="28" fill="#eaf3ea" stroke="{ink}" stroke-width="1.5"/>')
    s.append(f'<text x="240" y="51" text-anchor="middle" font-size="14" fill="{ink}">lungs</text>')
    s.append(f'<path d="M 178 90 C 150 60, 178 26, 200 34" fill="none" stroke="{blue}" stroke-width="2.2" marker-end="url(#bl)"/>')
    s.append(f'<path d="M 282 34 C 306 26, 332 60, 304 90" fill="none" stroke="{red}" stroke-width="2.2" marker-end="url(#bl)"/>')
    s.append(f'<text x="126" y="70" font-size="11.5" fill="{blue}">out</text>')
    s.append(f'<text x="336" y="70" font-size="11.5" fill="{red}">back</text>')
    s.append(f'<text x="240" y="292" text-anchor="middle" font-size="12.5" fill="#6b5535" font-style="italic">Close the wall and only one route remains.</text>')
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

def landing_data():
    """Every lesson gets a landing page, whether or not it declares one.

    Only algebra carried a hand-written `landing` block, and routing all
    lessons through this screen crashed the rest with a KeyError. The fallback
    is built from fields every lesson already has.
    """
    Ld = dict(D.get("landing") or {})
    obj = D.get("objective", {})
    Ld.setdefault("chapter_code", obj.get("code", ""))
    Ld.setdefault("chapter", D.get("chapter", ""))
    Ld.setdefault("statement", obj.get("syllabus_verbatim", obj.get("title", "")))
    Ld.setdefault("cta", "Unlock the wisdom")
    Ld.setdefault("teaser", "Before the method, the reason. Where this came from, "
                            "why anyone bothered, and where you are already using it "
                            "without knowing.")
    return Ld


def screen_landing():
    Ld = landing_data()
    st.markdown(f'<div class="eyebrow">{Ld["chapter_code"]} · {Ld["chapter"]}</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.5, 1], gap="large")
    with c1:
        st.markdown(
            f'<div class="panel landing-q"><div class="eyebrow" '
            f'style="margin-bottom:.7rem">What the exam asks you to do</div>'
            f'<p class="statement">{Ld["statement"]}</p></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="panel landing-cta"><p>{Ld["teaser"]}</p></div>',
            unsafe_allow_html=True,
        )
        if st.button(f'{Ld["cta"]} →', key="unlock_wisdom", type="primary"):
            st.session_state.view = "lesson"
            st.session_state.step = 0
            st.rerun()
        if st.button("← Chapters", key="landing_back"):
            st.session_state.view = "subject"
            st.rerun()


def screen_story():
    S = D["story"]
    L = D["lineage"]
    header("Lesson · Mīrāth", S["title"],
           "Where this came from, and why anyone bothered.")

    b = img_b64(D["source"]["arabic_image"]) if HAS_SOURCE else None
    c1, c2 = st.columns([1, 1.25], gap="large") if b else (None, st.container())
    if b:
        with c1:
            st.markdown(
                f'<div class="panel" style="padding:.7rem"><img src="data:image/jpeg;base64,{b}" '
                f'style="width:100%;border:1px solid #cbb489"/>'
                f'<div class="cite" style="margin:.6rem .4rem 0">'
                f'{D["source"]["edition"]}<br/>{D["source"]["arabic_locator"]}</div></div>',
                unsafe_allow_html=True,
            )
    with c2:
        words = "".join(f"<p>{w}</p>" for w in S["the_word"])
        st.markdown(f'<div class="panel"><h3>The word</h3>{words}</div>',
                    unsafe_allow_html=True)

    W = S.get("why_he_wrote_it") or S.get("why") or {}
    if W:
        # Only algebra has a verified primary quote. The others get no
        # blockquote rather than an invented one.
        quote = (f'<blockquote class="pq">{W["quote"]}</blockquote>'
                 if W.get("quote") else "")
        st.markdown(
            f'<div class="panel"><h3>Why it exists</h3>'
            f'<p>{W["lead"]}</p>{quote}'
            f'<div class="cite">{W["citation"]}</div>'
            f'<p style="margin-top:1rem">{W["after"]}</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="eyebrow">Where it lives now</div>', unsafe_allow_html=True)
    cols = st.columns(2, gap="large")
    for i, (title, body) in enumerate(S["where_now"]):
        with cols[i % 2]:
            st.markdown(
                f'<div class="panel" style="min-height:8.4rem"><h3>{title}</h3>'
                f'<p style="font-size:.97rem">{body}</p></div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        f'<div class="panel" style="border-color:#c9a227">'
        f'<h3>{L["thinker"]} · {L["place_time"]}</h3>'
        f'<p class="dropcap">{L["how_they_thought"]}</p>'
        f'<div class="cite">{L["citation"]} · {L["tier_label"]} '
        f'{L["confidence_mark"]}</div></div>',
        unsafe_allow_html=True,
    )


def screen_examples():
    E = D["examples"]
    header("Lesson · Miftāḥ", "Five shapes, one move", E["intro"])

    for item in E["items"]:
        fig = EXAMPLE_FIGURES.get(item["key"])
        st.markdown(f'<div class="eyebrow">{item["label"]}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.1], gap="large")
        with c1:
            steps = "".join(f"<li>{x}</li>" for x in item["steps"])
            st.markdown(
                f'<div class="panel"><p class="ex-q">{item["problem"]}</p>'
                f'<ol class="steps">{steps}</ol>'
                f'<p class="ex-a">{item["answer"]}</p>'
                f'<div class="cite">{item["note"]}</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            if fig:
                st.markdown(f'<div class="panel" style="padding:.8rem">{fig()}</div>',
                            unsafe_allow_html=True)
        st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)


def screen_practice():
    P = D["practice"]
    header("Apply", "Now you do it", P["intro"])

    if "solved" not in st.session_state:
        st.session_state.solved = set()

    done = len(st.session_state.solved)
    total = len(P["items"])
    st.markdown(
        f'<div class="panel" style="padding:.9rem 1.2rem">'
        f'<span class="prac-count">{done} of {total} revealed</span>'
        f'<span class="prac-hint"> — work it on paper first. Revealing before '
        f'you have tried teaches you nothing.</span></div>',
        unsafe_allow_html=True,
    )

    for i, item in enumerate(P["items"]):
        c1, c2 = st.columns([1.25, 1], gap="large")
        with c1:
            st.markdown(
                f'<div class="prac"><span class="prac-n">{i + 1}</span>'
                f'<span class="prac-q">{item["q"]}</span>'
                f'<span class="prac-t">{item["type"]}</span></div>',
                unsafe_allow_html=True,
            )
        with c2:
            if i in st.session_state.solved:
                st.markdown(
                    f'<div class="prac-a"><span class="pf">{item["form"]}</span>'
                    f'<span class="pa">{item["ans"]}</span></div>',
                    unsafe_allow_html=True,
                )
            elif st.button("Check", key=f"prac_{i}"):
                st.session_state.solved.add(i)
                st.rerun()

    if done == total:
        st.markdown(
            '<div class="panel" style="text-align:center;border-color:#c9a227">'
            '<p style="font-size:1.1rem">Ten problems, five shapes, one method — '
            'the one he wrote down so it would outlast him.</p>'
            '<p class="gold" style="font-size:1.2rem">You are its <em>wārith</em>.</p>'
            '</div>', unsafe_allow_html=True)


def screen_keywords():
    K = D["keywords"]
    header("Lesson · Jisr", "The words the marks are attached to",
           "IGCSE is marked on precise terminology and on obeying the command word.")

    c1, c2 = st.columns([1, 1.2], gap="large")
    with c1:
        rows = "".join(
            f'<div class="kwrow"><span class="kw-cmd">{c}</span>'
            f'<span class="kw-def">{d}</span></div>' for c, d in K["command_words"])
        st.markdown(f'<div class="panel"><h3>Command words</h3>'
                    f'<p style="font-size:.94rem;color:#6b5535">What the question is '
                    f'actually asking you to do. Answering the wrong one scores zero '
                    f'however correct the content.</p>{rows}</div>',
                    unsafe_allow_html=True)
    with c2:
        rows = "".join(
            f'<div class="kwrow"><span class="kw-term">{t}</span>'
            f'<span class="kw-def">{d}</span></div>' for t, d in K["terms"])
        st.markdown(f'<div class="panel"><h3>Key terms</h3>'
                    f'<p style="font-size:.94rem;color:#6b5535">Examiners mark the word, '
                    f'not the paraphrase. These are the ones that carry marks.</p>'
                    f'{rows}</div>', unsafe_allow_html=True)


def render_ask_panel():
    """Pinned beside every lesson screen. Deterministic: see ask.py."""
    A = D.get("ask")
    if not A:
        return
    with st.sidebar:
        st.markdown('<div class="ask-head">Ask</div>', unsafe_allow_html=True)
        st.markdown(f'<p class="ask-note">{A["grounding_note"]}</p>',
                    unsafe_allow_html=True)

        for i, q in enumerate(A["suggested"]):
            if st.button(q, key=f"sq_{i}", use_container_width=True):
                st.session_state.asked = q

        # A form rather than a bare text_input: a form always commits on
        # submit, instead of depending on Enter-key or blur behaviour that
        # differs between browsers. On stage that difference is not worth it.
        with st.form("ask_form", clear_on_submit=False):
            typed = st.text_input("Or ask your own",
                                  placeholder="Type your own question…",
                                  label_visibility="collapsed")
            if st.form_submit_button("Ask", use_container_width=True) and typed.strip():
                st.session_state.asked = typed.strip()

        q = st.session_state.get("asked")
        if q:
            text, matched = ask.answer(q, A)
            st.markdown(
                f'<div class="ask-a{"" if matched else " refused"}">'
                f'<div class="ask-q">{q}</div><p>{text}</p></div>',
                unsafe_allow_html=True,
            )


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
    L = D["lineage"]
    tier = L.get("tier", 1)

    if tier == 1:
        header("Lesson · Mīrāth", "Whose you are",
               "The inheritance — and the tier it sits in.")
    else:
        header("Lesson · Mīrāth", "No thread here — and we say so",
               "Wisdom is taken wherever it is found.")

    st.markdown(
        f'<span class="tier1{"" if tier == 1 else " t2"}">{L["tier_label"]}'
        f'{" " + L.get("confidence_mark", "") if tier == 1 else ""}</span>',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:.9rem'></div>", unsafe_allow_html=True)

    if L.get("honest_statement"):
        st.markdown(
            f'<div class="panel honest"><h3>Before anything else</h3>'
            f'<p>{L["honest_statement"]}</p></div>',
            unsafe_allow_html=True,
        )

    c1, c2 = st.columns([1.4, 1], gap="large")
    with c1:
        st.markdown(
            f'<div class="panel"><h3>{L["thinker"]}</h3>'
            f'<p style="font-style:italic;color:#6b5535">{L["place_time"]}</p>'
            f'<p>{L["contribution"]}</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="panel"><h3>How they thought</h3>'
            f'<p class="dropcap">{L["how_they_thought"]}</p>'
            f'<div class="cite">{L["citation"]}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        if tier == 1:
            body = ('<p>Tier 1 means the thread is <span class="gold">direct</span> — not a '
                    'precursor, not a flourish. This topic is theirs.</p>'
                    '<p>Where no such thread exists, we say so and teach another great mind. '
                    'Where no single originator exists, we drop the hero entirely and teach '
                    'the method alone.</p>')
        else:
            body = ('<p>Tier 2 is not a retreat from the mission — it is its fullest form. '
                    '<em>al-ḥikma ḍāllat al-muʾmin</em>: wisdom is the believer\'s lost '
                    'property, to be taken wherever it is found.</p>'
                    '<p>The House of Wisdom was itself a translation movement. al-Khwārizmī '
                    'built on Hindu numerals and Greek geometry. Learning from Faraday '
                    '<em>is</em> thinking the way al-Khwārizmī thought.</p>')
        if L.get("why_it_matters"):
            body += f'<p class="gold">{L["why_it_matters"]}</p>'
        st.markdown(
            f'<div class="panel"><h3>Why this tier</h3>{body}'
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
    if D["id"] == "distillation":
        st.markdown('<div class="eyebrow">The apparatus they built — and the word '
                    'English kept</div>', unsafe_allow_html=True)
        show_svg(svg_still(), "Find the difference, then build the thing that exploits it")
        return

    if D["id"] == "circulation":
        st.markdown('<div class="eyebrow">What a solid wall forces to be true</div>',
                    unsafe_allow_html=True)
        show_svg(svg_heart(), "Galen said blood seeped through. Ibn al-Nafīs looked, and it does not.")
        return

    if D["id"] == "cipher":
        st.markdown('<div class="eyebrow">He stopped reading the message and '
                    'counted it instead</div>', unsafe_allow_html=True)
        show_svg(svg_frequency(),
                 "Rank the ciphertext, rank the language, line them up")
        return

    if D["id"] == "magnetism":
        st.markdown('<div class="eyebrow">He could not write the equations — so he '
                    'drew the answer</div>', unsafe_allow_html=True)
        show_svg(svg_bar_magnet(),
                 "The field around a bar magnet, exactly as Faraday first pictured it")
        return

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
        if D["objective"].get("bridge"):
            st.markdown(
                f'<div class="panel"><h3>Why this counts as inherited</h3>'
                f'<p>{D["objective"]["bridge"]}</p></div>',
                unsafe_allow_html=True,
            )
    with c2:
        w = C.get("khwarizmi_worked") or C.get("worked")
        rows = "".join(f"<li>{s}</li>" for s in w["steps"])
        st.markdown(
            f'<div class="panel"><h3>Worked through</h3>'
            f'<p style="font-size:1.3rem;text-align:center;color:#2c2216">'
            f'<strong>{w["problem"]}</strong></p>'
            f'<ol class="steps">{rows}</ol>'
            f'<p style="text-align:center;color:#1f5e3d;font-size:1.1rem">'
            f'<strong>{w["answer"]}</strong></p></div>',
            unsafe_allow_html=True,
        )
        n_steps = len(w.get("steps", []))
        st.markdown(
            f'<div class="panel"><p style="font-size:.95rem">Centuries apart, the same '
            f'{n_steps} moves. The syllabus did not invent this method — '
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
                f'<div class="panel"><h3>{A.get("reveal_heading", "The solution")}</h3>'
                f'<ol class="steps">{steps}</ol>'
                f'<p style="text-align:center;color:#1f5e3d;font-size:1.12rem">'
                f'<strong>{A["answer"]}</strong></p>'
                f'<div class="cite">{A["mark_scheme"]}</div></div>',
                unsafe_allow_html=True,
            )
            figure = {"magnetism": svg_neutral_point, "cipher": svg_frequency,
                      "distillation": svg_still, "circulation": svg_heart}.get(
                D["id"], svg_overlap)
            show_svg(figure())
        else:
            st.markdown(
                '<div class="panel" style="text-align:center;padding:3.5rem 1rem">'
                '<p style="color:#a08c60;font-style:italic">The worked solution appears '
                'once you have attempted it.</p></div>',
                unsafe_allow_html=True,
            )

    if st.session_state.attempted:
        st.markdown(
            f'<div class="panel" style="text-align:center;border-color:#c9a227">'
            f'<p style="font-size:1.12rem">You did not watch someone solve it. '
            f'You solved it — {A.get("closing", "using a method someone wrote down so it would outlive them")}.</p>'
            f'<p class="gold" style="font-size:1.25rem;letter-spacing:.06em">'
            f'You are its <em>wārith</em>.</p></div>',
            unsafe_allow_html=True,
        )


HERO = """
<div class="hero">
  <p class="punch">The mind is the greatest asset any of us will ever hold.<br/>
  Your child is inheriting a fortune —
  the wisdom of the greatest thinkers who ever lived.<br/>
  Unlock the blueprint, and mould the one thing that lasts:
  <em>how they think</em>.</p>

  <p class="names">Algebra without <b>al-jabr</b>. Algorithm without <b>al-Khwārizmī</b>.
  Circulation without <b>Ibn al-Nafīs</b>. Fields without <b>Faraday</b>.
  Your child has inherited every one of these, and been introduced to none of them.</p>

  <p>Every rule in that textbook was once somebody's breakthrough. School hands over the
  finished product and throws away the working — and a finished product is the one thing
  a mind cannot learn from.</p>

  <p>Children arrive as natural explorers. Then we spend eleven years handing them
  conclusions, and wonder where the curiosity went. Give them the raw material instead:
  <strong>how those minds actually moved</strong>. How to think. How to break a problem
  open.</p>

  <p>That is the real inheritance, and the only kind that cannot be spent, lost or
  taken — a method, written down, outlives the one who found it. And it has to be handed
  over <strong>now</strong>, while the mind is still being shaped.</p>

  <p>None of this is reverence for the past — it is <strong>equipment for what comes
  next</strong>.<br/>
  <span class="mark">The problems waiting for your child have not been solved by
  anyone.</span><br/>
  Meeting them will take exactly what al-Khwārizmī needed in front of a blank page:
  <strong>a mind that knows how to begin</strong>.</p>

  <p class="kicker">Then we stop talking, and the page turns to them:
  <strong>now you think</strong> — use the faculties you were given.<br/>
  Same syllabus. Same exam. A child who walks out knowing
  <strong>the knowledge is theirs</strong>.</p>
</div>
"""

BRIEF = """
<div class="brief-grid">

  <div class="brief">
    <h4>What this is</h4>
    <p class="lead">Your mind is the one asset that compounds for life — and the only
    one nobody can take from you.</p>
    <details>
      <summary>Read more</summary>
      <p>Every topic in your syllabus was once an unsolved problem. Someone cracked it,
      and the way they thought left a <strong>blueprint</strong> — a repeatable set of
      moves that still works centuries later.</p>
      <p>Written down, a method outlives the person who found it. That is what makes it
      an inheritance.</p>
      <p>This is where you inherit it: the wisdom of great thinkers and visionaries,
      handed over as <strong>method</strong>, not memorised as fact.</p>
    </details>
  </div>

  <div class="brief">
    <h4>Why we're doing this</h4>
    <p class="lead">Curricula teach concepts as though they fell from the sky. Algebra
    with no <em>al-jabr</em>. The concept survives — the mind that made it is deleted.</p>
    <details>
      <summary>Read more</summary>
      <p>Algorithm with no al-Khwārizmī. Circulation with no Ibn al-Nafīs. Fields with
      no Faraday, inheritance with no Mendel.</p>
      <p>What a child absorbs from that is worse than a missing fact: that knowledge is
      something which happens elsewhere, made by other people, in another time — never
      something they could do themselves.</p>
      <p>The usual fix is <strong>a module bolted on the side</strong> — a "great
      thinkers" unit admired once, sitting beside the real subject, never examined. That
      is precisely the mistake. A module parked alongside announces that the lineage is
      optional.</p>
      <p>So we don't bolt it on. <strong>We put the depth back inside the syllabus point
      itself.</strong> One track. The same chapter your school teaches — with the mind
      restored to it.</p>
    </details>
  </div>

  <div class="brief">
    <h4>What it does</h4>
    <p class="lead">Hands over how to think and how to solve — as raw material, not a
    finished answer. Four things, every lesson.</p>
    <details>
      <summary>Read more</summary>
      <p><strong>A mind map of the method</strong> — not of the topic, of the
      <em>thinking</em>. The shape of how to approach it, held in your head rather than
      re-read off a page.</p>
      <p><strong>A blueprint for the solution</strong> — the exact sequence of moves that
      cracks this kind of problem, taken from the person who first made them.</p>
      <p><strong>Systems thinking</strong> — where this idea sits, what it connects to,
      what breaks if you pull it out. Nothing on a syllabus is really an island.</p>
      <p><strong>Questions before answers</strong> — you are asked, not told. The
      solution stays hidden until you have tried.</p>
      <p>Struggle first, answer second. That is how a blueprint becomes a habit instead
      of a note.</p>
    </details>
  </div>

</div>
"""

ARC = """
<div class="eyebrow">Every lesson walks the same four moves</div>
<div class="arc">
  <div class="step">
    <span class="ar">ميراث</span>
    <span class="tr">Mīrāth</span>
    <span class="en">inheritance</span>
    <span class="what">Whose you are. The mind behind the topic, and how strong
    the thread to them really is.</span>
  </div>
  <div class="step">
    <span class="ar">مفتاح</span>
    <span class="tr">Miftāḥ</span>
    <span class="en">key</span>
    <span class="what">What they left you. The thinking move that opens the
    problem — think how they thought.</span>
  </div>
  <div class="step">
    <span class="ar">جسر</span>
    <span class="tr">Jisr</span>
    <span class="en">bridge</span>
    <span class="what">Carrying it across. The same move in the exact form
    Cambridge asks for, at full-mark depth.</span>
  </div>
  <div class="step">
    <span class="ar">تطبيق</span>
    <span class="tr">Taṭbīq</span>
    <span class="en">apply</span>
    <span class="what">Now you think. A real exam problem, with the solution
    withheld until you have tried it.</span>
  </div>
</div>
"""

BELOW_PICKER = """
<div class="contrast">
  <p><strong>School says:</strong> here is the rule, here is a worked example, here are
  thirty more like it.<br/>
  <strong>We say:</strong> here is the mind behind the rule, here is how it moved —
  now move yours.</p>
  <p class="promise">The outcome a parent should be able to claim:
  <strong>my child mastered the syllabus — and knows the knowledge is theirs.</strong></p>
  <p style="font-size:.94rem;color:#6b5535">Where a great thinker stands behind a topic,
  you meet them first — and where that thread runs back to the Muslim world, it leads.
  Where nobody single-handedly stands behind it, we say so and teach the method alone.
  Nothing is invented to make a story tidier.</p>
</div>

<div class="strip">
  <div class="s"><b>Unlock</b><span>We go to the primary source and read it ourselves —
  transcribed, translated, then scored against a trusted benchmark before a word of it
  is taught.</span></div>
  <div class="s"><b>Understand</b><span>What survives that check becomes a chain of
  citation. Every claim keeps its source and its confidence.</span></div>
  <div class="s"><b>Transmit</b><span>Only then is the lesson written — from verified
  material, at exactly the depth the exam demands.</span></div>
</div>
"""


def screen_home():
    st.markdown('<div class="eyebrow">Mīrāth al-Ḥikma</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="title" style="font-size:3.6rem;line-height:1.05">'
                'Inheritance of Wisdom</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">The algorithm behind every topic — '
                '<em>how to think, how to solve</em></p>', unsafe_allow_html=True)
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    st.markdown(HERO, unsafe_allow_html=True)
    st.markdown(BRIEF, unsafe_allow_html=True)

    st.markdown(ARC, unsafe_allow_html=True)

    st.markdown('<div class="eyebrow">What do you want to learn today?</div>',
                unsafe_allow_html=True)
    st.markdown(mindmap.render_subject_cards(), unsafe_allow_html=True)
    st.markdown(BELOW_PICKER, unsafe_allow_html=True)


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


if HAS_STORY and HAS_SOURCE:
    RENDER = [screen_story, screen_unlock, screen_critic, screen_miftah,
              screen_examples, screen_jisr, screen_keywords, screen_practice]
elif HAS_STORY:
    RENDER = [screen_story, screen_miftah, screen_jisr,
              screen_keywords, screen_practice]
elif HAS_SOURCE:
    RENDER = [screen_manuscript, screen_unlock, screen_critic,
              screen_mirath, screen_miftah, screen_jisr, screen_apply]
else:
    RENDER = [screen_mirath, screen_miftah, screen_jisr, screen_apply]

if st.session_state.view == "landing":
    screen_landing()
    st.stop()

render_ask_panel()

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
