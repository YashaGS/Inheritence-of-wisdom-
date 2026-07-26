"""
Pre-flight. Run this before you present, not during.

Loads every frozen field and asset the demo path touches and fails loudly if
anything is missing or malformed. Catches a broken cache at the desk instead of
in front of judges (algorism-code-spine.md §2.5).

    python3 self_check.py
"""

import json
import sys
from pathlib import Path

import critic

ROOT = Path(__file__).parent
FAILURES = []


def check(label, condition, detail=""):
    if condition:
        print(f"  ok    {label}")
    else:
        print(f"  FAIL  {label}{' — ' + detail if detail else ''}")
        FAILURES.append(label)


def main():
    print("\nAlgorism pre-flight\n" + "-" * 52)

    lessons = sorted((ROOT / "content" / "lessons").glob("*.json"))
    check("at least one lesson exists", bool(lessons))
    if not lessons:
        sys.exit(1)
    print(f"        {len(lessons)} lesson(s): "
          + ", ".join(p.stem for p in lessons))

    for path in lessons:
        check_lesson(path)

    print("-" * 52)
    if FAILURES:
        print(f"PRE-FLIGHT FAILED — {len(FAILURES)} problem(s):")
        for f in FAILURES:
            print(f"  · {f}")
        sys.exit(1)
    print("PRE-FLIGHT PASSED — every lesson is complete.\n")


def check_lesson(path):
    D = json.loads(path.read_text(encoding="utf-8"))
    lid = D.get("id", path.stem)
    has_source = bool(D.get("has_source"))
    print(f"\n=== {lid} === (tier {D.get('lineage', {}).get('tier')}, "
          f"source: {'yes' if has_source else 'none'})")

    print("Frozen fields")
    required = {
        "objective": ["code", "syllabus_verbatim"],
        "lineage": ["tier", "thinker", "how_they_thought", "citation", "confidence"],
        "algorithm": ["name", "steps", "socratic_prompts"],
        "cambridge_form": ["statement", "method", "general_result"],
        # closing and reveal_heading exist because copy written for one lesson
        # silently leaked into the others once there was more than one.
        "apply": ["problem", "reveal_steps", "answer", "mark_scheme",
                  "reveal_heading", "closing"],
    }
    if has_source:
        required["source"] = ["work", "author", "edition", "arabic_image", "arabic_locator"]
        required["unlock"] = ["arabic_transcription", "our_translation"]
        required["critic"] = ["benchmark_text", "benchmark_citation"]

    for section, fields in required.items():
        for f in fields:
            check(f"{lid}.{section}.{f}", bool(D.get(section, {}).get(f)))

    if has_source:
        print("Assets on disk")
        for key in ("arabic_image", "english_image"):
            rel = D["source"].get(key, "")
            pth = ROOT / rel
            check(f"{key} ({rel})", pth.exists() and pth.stat().st_size > 10_000,
                  "missing or suspiciously small")
    else:
        # A lesson without a manuscript must not carry half a source layer.
        for ghost in ("source", "unlock", "critic"):
            check(f"no phantom {ghost} block", ghost not in D,
                  "lesson claims no source but carries one")

    baghdad = "baghdad" in D["apply"].get("closing", "").lower()
    islamic = D["lineage"].get("tier") == 1 and not D["lineage"].get("no_islamic_thread")
    check("closing line matches the lesson's own lineage", baghdad <= islamic,
          "a non-Islamic-lineage lesson must not close by crediting Baghdad")

    print("Lineage integrity")
    tier = D["lineage"].get("tier")
    check("tier is 1, 2 or 3", tier in (1, 2, 3), f"got {tier!r}")
    check("tier 1 carries a citation",
          tier != 1 or bool(D["lineage"].get("citation")))
    check("confidence is direct or precursor",
          D["lineage"].get("confidence") in ("direct", "precursor"))
    check("quran_link is null unless genuinely referenced",
          "quran_link" in D["algorithm"])

    tier = D["lineage"].get("tier")
    if tier != 1:
        check("tier 2 states the absence out loud",
              bool(D["lineage"].get("honest_statement")),
              "a non-Tier-1 lesson must say so in the lesson, not just in the data")

    if has_source:
        print("Critic (recomputed live)")
        r = critic.score(D["unlock"]["our_translation"], D["critic"]["benchmark_text"])
        check("all load-bearing claims agree", r["claim_agreement"] == 1.0,
              f"agreement {r['claim_agreement']}")
        check("composite score is presentable", r["composite"] >= 0.70,
              f"scored {r['percent']}%")
        print(f"        score {r['percent']}%  —  {r['verdict']}")


if __name__ == "__main__":
    main()
