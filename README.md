# Mīrāth al-Ḥikma · Algorism

**The algorithm behind every topic — how to think, how to solve.**

Five Cambridge IGCSE lessons, one per subject, each putting back the mind that worked the topic out — with every claim traceable to an attached source, and honest about the topics where there is no such mind to name.

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

**Five lessons, one in every subject** — each mapped to a verbatim Cambridge objective.

| Subject | Objective | Inherited from |
|---|---|---|
| Mathematics 0580 | **E2.2** completing the square | al-Khwārizmī |
| Physics 0625 | **4.1** magnetic fields | Faraday *(Tier 2)* |
| Chemistry 0620 | **12.4** separation and purification | Jābir, al-Rāzī |
| Biology 0610 | **9.1** circulatory systems | Ibn al-Nafīs |
| Computer Science 0478 | **2.3** encryption | al-Kindī |

Every lesson walks the same arc — **Mīrāth** (the inheritance) → **Miftāḥ** (the key) → **Jisr** (the bridge to the exam) → vocabulary → **Taṭbīq** (apply), with a pinned Ask panel throughout.

The algebra lesson additionally carries the full verification pipeline, because it is the one topic with a public-domain facing-page source:

**Mīrāth** → **Unlock** → **Critic** → **Miftāḥ** → **Shapes** → **Jisr** → **Key words** → **Practice**

1. **Mīrāth** — where it came from and why anyone bothered, with the manuscript page.
2. **Unlock** — the transcription and translation produced by a build-time vision pass.
3. **Critic** — that translation scored **against Rosen's own English on the facing page**.
4. **Miftāḥ** — the thinking move, taught Socratically, with his geometric proof.
5. **Shapes** — the five forms a quadratic arrives in, each with a diagram.
6. **Jisr** — the same move in the form the exam demands.
7. **Key words** — the command words and terminology the marks are attached to.
8. **Practice** — ten problems, each revealing independently.

---

## Honesty is the moat — and it is engineered, not promised

**The critic score is computed in code.** `critic.py` compares two frozen strings and returns a number. No model reports its own confidence — a model grading its own translation is precisely the failure this architecture exists to prevent.

Claim agreement is weighted at **0.60** deliberately: a fluent paraphrase that loses a number scores *worse* than clumsy prose that keeps them all. Eight load-bearing numbers are checked one by one (five, twenty-five, thirty-nine, sixty-four, eight, three, nine, ten). If any disagrees, the verdict is `DIVERGENT — do not teach from this`, regardless of how good the prose is.

Current score: **80.1% — VERIFIED**, 8/8 claims agreeing.

**The two page images are facing pages of the same passage.** Arabic p.٥ (leaf n351) is al-Khwārizmī's *"a square and ten of its roots equal thirty-nine dirhams"*; English p.8 (leaf n32) is Rosen translating exactly that. The comparison is real, not staged.

**Tier, confidence and citation are frozen fields**, set by human curation in `content/lessons/<id>.json`, never regenerated at runtime. The model's job is to narrate the node, not to decide it.

**Nothing is generated while you watch.** The demo path reads `content/lessons/<id>.json` and makes no network call and no model call. The Ask panel matches questions deterministically in `ask.py` — there is no model in the loop to invent a scholar into. Verified by inspecting browser traffic: `localhost` only. It runs with the wifi off.

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

Syllabus boundary: Cambridge IGCSE **Mathematics 0580** (2025–27), **Physics 0625**, **Chemistry 0620**, **Biology 0610** and **Computer Science 0478** (2026–28). Every chapter and subtopic title in the app was extracted verbatim from these PDFs.

---

## Scope, stated honestly

This is five objectives, one per subject — a vertical slice, not the product. **58 chapters and 226 Cambridge subtopics are mapped; five have finished lessons.** The map shows what is not built rather than hiding it.

The frame it grows into — per-learner calibration, simulations and hands-on practicals, past-paper drilling — is deliberately not built yet.

**Of the 58 chapters mapped, 33 have no Islamic thread at all** — and the app says so on the chapter itself rather than quietly omitting it. At the finer grain of individual objectives the share without a Tier-1 lineage is higher still.

Those are carried by the universal algorithm layer, and given a Tier-2 thinker where a clear one exists. That is the design, not a shortfall.
