"""
Build the full local exam bank from the .docx question papers.

Why this exists, and why its output is gitignored
-------------------------------------------------
The compiled bank contains questions from Save My Exams, the Cambridge
Coursebook and Cambridge past papers. Those are other people's copyright, and
`algorism-app-architecture-brief.md` §5 is explicit that Save My Exams is a
personal reading licence and never a product source.

This repository and the deployed app are both public. So:

  * the bank this script writes goes to content/exam_local/, which is
    gitignored and never leaves the machine it was built on;
  * the app loads it when present and falls back to the original,
    licence-clean questions baked into the lesson file when it is not.

Addu gets the whole bank. The public demo ships only what we wrote ourselves.
Run it whenever the source documents change:

    python3 build_exam_bank.py
"""

import json
import re
import sys
import zipfile
from pathlib import Path

SRC = Path("/Users/yashags/Documents/Home Ed/Claude CoWork/Addu IGCSE/"
           "IGCSE Physics/Magnetism/Exam prep")
OUT = Path(__file__).parent / "content" / "exam_local" / "magnetism.json"

PAPERS = {
    "mcq": ("Magnetism - Multiple Choice Questions.docx",
            "Magnetism - MCQ Answer Sheet.docx"),
    "theory": ("Magnetism - Theory Questions.docx",
               "Magnetism - Theory Answer Sheet.docx"),
}

Q_HEAD = re.compile(r"^Q(\d+)\s+(.*)$")
OPTION = re.compile(r"^([A-D])[.)]\s+(.+)$")
ANSWER_LINE = re.compile(r"^Q(\d+)\.?\s+Answer:\s*([A-D])\s*(?:\((.*)\))?\s*$")
SECTION = re.compile(r"^[A-H]\.\s+.+")


def paragraphs(path):
    """Plain text paragraphs from a .docx, without needing python-docx."""
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        text = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S))
        text = re.sub(r"<[^>]+>", "", text)
        text = (text.replace("&amp;", "&").replace("&apos;", "'")
                    .replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">"))
        text = text.strip()
        if text:
            out.append(text)
    return out


def parse_mcq(qs, ans):
    """Question stems and options from the paper; letters and reasons from the key."""
    keys = {}
    lines = paragraphs(ans)
    for i, line in enumerate(lines):
        m = ANSWER_LINE.match(line)
        if m:
            n, letter, gloss = int(m.group(1)), m.group(2), (m.group(3) or "").strip()
            why = lines[i + 1] if i + 1 < len(lines) and not ANSWER_LINE.match(lines[i + 1]) else ""
            keys[n] = {"letter": letter, "gloss": gloss, "why": why}

    items, cur, section = [], None, ""
    for line in paragraphs(qs):
        head = Q_HEAD.match(line)
        if head:
            if cur:
                items.append(cur)
            cur = {"n": int(head.group(1)), "source": head.group(2).strip(),
                   "section": section, "q": "", "options": []}
            continue

        # Options must be tested before section headings: "A.  aluminium" also
        # matches the section pattern "^[A-H]\.", and testing SECTION first
        # silently ate every option in the paper.
        opt = OPTION.match(line)
        # An IGCSE MCQ has exactly four options. Past the fourth, an "A. …"
        # line is the next section heading, not a fifth choice.
        if cur and cur["q"] and opt and len(cur["options"]) < 4:
            cur["options"].append(opt.group(2).strip())
            continue
        if SECTION.match(line):
            section = line
            continue
        if not cur or line.startswith("Answer:"):
            continue
        if not cur["options"]:
            cur["q"] = (cur["q"] + " " + line).strip()
    if cur:
        items.append(cur)

    out = []
    for it in items:
        k = keys.get(it["n"])
        if not k or len(it["options"]) < 2:
            continue
        try:
            correct = "ABCD".index(k["letter"])
        except ValueError:
            continue
        if correct >= len(it["options"]):
            continue
        out.append({"n": it["n"], "source": it["source"], "section": it["section"],
                    "q": it["q"], "options": it["options"],
                    "correct": correct, "why": k["why"] or k["gloss"]})
    return out


def parse_theory(qs, ans):
    """Stems and parts from the paper; the mark scheme from the key."""
    schemes, cur_n, buf = {}, None, []
    for line in paragraphs(ans):
        head = Q_HEAD.match(line)
        if head:
            if cur_n is not None:
                schemes[cur_n] = " ".join(buf).strip()
            cur_n, buf = int(head.group(1)), []
            continue
        if cur_n is not None and not SECTION.match(line):
            buf.append(line)
    if cur_n is not None:
        schemes[cur_n] = " ".join(buf).strip()

    items, cur, section = [], None, ""
    for line in paragraphs(qs):
        if SECTION.match(line):
            section = line
            continue
        head = Q_HEAD.match(line)
        if head:
            if cur:
                items.append(cur)
            cur = {"n": int(head.group(1)), "source": head.group(2).strip(),
                   "section": section, "q": "", "parts": []}
            continue
        if not cur:
            continue
        if re.match(r"^\(?[a-z]\)|^\([ivx]+\)", line):
            cur["parts"].append(line)
        elif not cur["parts"]:
            cur["q"] = (cur["q"] + " " + line).strip()
        else:
            cur["parts"].append(line)
    if cur:
        items.append(cur)

    out = []
    for it in items:
        scheme = schemes.get(it["n"], "")
        if not it["parts"] and not it["q"]:
            continue
        marks = sum(int(m) for m in re.findall(r"\[(\d+)\]", " ".join(it["parts"]))) or None
        out.append({"n": it["n"], "source": it["source"], "section": it["section"],
                    "q": it["q"], "parts": it["parts"], "marks": marks,
                    "scheme": scheme})
    return out


def main():
    if not SRC.exists():
        sys.exit(f"Source folder not found: {SRC}")

    mcq = parse_mcq(SRC / PAPERS["mcq"][0], SRC / PAPERS["mcq"][1])
    theory = parse_theory(SRC / PAPERS["theory"][0], SRC / PAPERS["theory"][1])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "_note": "LOCAL ONLY — built from copyrighted question papers. Gitignored. "
                 "Never commit this file or deploy it.",
        "built_from": str(SRC),
        "mcq": mcq, "theory": theory,
    }, ensure_ascii=False, indent=2) + "\n")

    from collections import Counter
    src = Counter(q["source"].split("·")[0].strip() for q in mcq + theory)
    print(f"wrote {OUT}")
    print(f"  MCQ    {len(mcq)}")
    print(f"  Theory {len(theory)}  ({sum(t['marks'] or 0 for t in theory)} marks)")
    print("  sources:")
    for s, n in src.most_common():
        print(f"    {n:4}  {s}")


if __name__ == "__main__":
    main()
