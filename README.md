# Mīrāth al-Ḥikma · Algorism

**One page of al-Khwārizmī's *Algebra*, carried to a Cambridge IGCSE lesson — with every claim traceable to an attached source.**

Built for Algorism №001, Bengaluru, 26 July 2026.

---

## The idea

A method, once written down, outlives its author. That is the definition of a good algorithm — and of an inheritance.

Children learn algebra without al-Khwārizmī, optics without Ibn al-Haytham, circulation without Ibn al-Nafīs. The science survived; the lineage was cut off. But the honest version of that story is harder than the popular one: most syllabus topics have *no* Islamic thread, and pretending otherwise is what discredits this whole space.

So this system separates two things:

- **The algorithm of the topic** — the thinking blueprint that cracks it. Universal. Exists for every objective on the syllabus.
- **The lineage** — the human behind it. Graded honestly into three tiers, and sometimes **absent**.

| Tier | Meaning | Behaviour |
|---|---|---|
| **1** | Islamic scholar, direct thread | Leads the lesson |
| **2** | Another great mind, no Islamic thread | Taught for *how they thought* |
| **3** | No single originator | Hero dropped; algorithm taught alone |

Wisdom is *ḍāllat al-muʾmin* — the believer's lost property, taken wherever it is found. The House of Wisdom was itself a translation movement. Restricting to only-Muslim thinkers would betray the tradition's own openness.

---

## What this demo does

Cambridge IGCSE Mathematics 0580, objective **E2.2.5** — *"Complete the square for expressions in the form ax² + bx + c."*

Seven screens:

**Manuscript** → **Unlock** → **Critic** → **Mīrāth** → **Miftāḥ** → **Jisr** → **Apply**

1. **Manuscript** — al-Khwārizmī's Arabic page, from Rosen's 1831 public-domain edition.
2. **Unlock** — the transcription and translation produced by a build-time vision pass.
3. **Critic** — the translation scored **against Rosen's own English on the facing page**.
4. **Mīrāth** — whose you are: the scholar, the tier, the citation.
5. **Miftāḥ** — the thinking move, taught Socratically, with his geometric proof.
6. **Jisr** — the same move in the form the exam demands.
7. **Apply** — the child solves one, withhold-then-reveal. The flow ends on their attempt.

---

## Honesty is the moat — and it is engineered, not promised

**The critic score is computed in code.** `critic.py` compares two frozen strings and returns a number. No model reports its own confidence — a model grading its own translation is precisely the failure this architecture exists to prevent.

Claim agreement is weighted at **0.60** deliberately: a fluent paraphrase that loses a number scores *worse* than clumsy prose that keeps them all. Eight load-bearing numbers are checked one by one (five, twenty-five, thirty-nine, sixty-four, eight, three, nine, ten). If any disagrees, the verdict is `DIVERGENT — do not teach from this`, regardless of how good the prose is.

Current score: **80.1% — VERIFIED**, 8/8 claims agreeing.

**The two page images are facing pages of the same passage.** Arabic p.٥ (leaf n351) is al-Khwārizmī's *"a square and ten of its roots equal thirty-nine dirhams"*; English p.8 (leaf n32) is Rosen translating exactly that. The comparison is real, not staged.

**Tier, confidence and citation are frozen fields**, set by human curation in `content/frozen.json`, never regenerated at runtime. The model's job is to narrate the node, not to decide it.

**Nothing is generated while you watch.** The demo path reads `content/frozen.json` and makes no network call and no model call. Verified by inspecting browser traffic: `localhost` only. It runs with the wifi off.

---

## Run it

```bash
pip install -r requirements.txt
python3 self_check.py     # pre-flight — fails loudly if any frozen field is missing
python3 -m streamlit run app.py
```

`self_check.py` loads every field and asset the demo touches and asserts they are present and well-formed. Run it before presenting, not during.

---

## Source

Muḥammad ibn Mūsā al-Khwārizmī, *Kitāb al-mukhtaṣar fī ḥisāb al-jabr wa-l-muqābala*, Baghdad, c. 820 CE.

Edition: Frederic Rosen, *The Algebra of Mohammed ben Musa* (London: Oriental Translation Fund, 1831). Public domain. [archive.org/details/algebraofmohamme00khuwuoft](https://archive.org/details/algebraofmohamme00khuwuoft)

Syllabus boundary: Cambridge IGCSE Mathematics 0580, syllabus for 2025–2027.

---

## Scope, stated honestly

This is one objective, end to end — the vertical slice, not the product. The frame it grows into (subject grid, chapter mind maps, per-learner calibration) is deliberately not built yet.

Roughly **70% of syllabus objectives have no Tier-1 lineage.** They are carried by the universal algorithm layer and given a Tier-2 thinker where a clear one exists. That is the design, not a shortfall.
