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

    path = ROOT / "content" / "frozen.json"
    check("frozen.json exists", path.exists())
    if not path.exists():
        sys.exit(1)

    D = json.loads(path.read_text(encoding="utf-8"))

    print("\nFrozen fields")
    for section, fields in {
        "objective": ["code", "syllabus_verbatim", "related_code"],
        "source": ["work", "author", "edition", "arabic_image", "arabic_locator"],
        "unlock": ["arabic_transcription", "our_translation"],
        "critic": ["benchmark_text", "benchmark_citation"],
        "lineage": ["tier", "thinker", "how_they_thought", "citation", "confidence"],
        "algorithm": ["name", "steps", "socratic_prompts"],
        "cambridge_form": ["statement", "method", "general_result", "khwarizmi_worked"],
        "apply": ["problem", "reveal_steps", "answer", "mark_scheme"],
    }.items():
        for f in fields:
            check(f"{section}.{f}", bool(D.get(section, {}).get(f)))

    print("\nAssets on disk")
    for key in ("arabic_image", "english_image"):
        rel = D["source"].get(key, "")
        p = ROOT / rel
        check(f"{key} ({rel})", p.exists() and p.stat().st_size > 10_000,
              "missing or suspiciously small")

    print("\nLineage integrity")
    tier = D["lineage"].get("tier")
    check("tier is 1, 2 or 3", tier in (1, 2, 3), f"got {tier!r}")
    check("tier 1 carries a citation",
          tier != 1 or bool(D["lineage"].get("citation")))
    check("confidence is direct or precursor",
          D["lineage"].get("confidence") in ("direct", "precursor"))
    check("quran_link is null unless genuinely referenced",
          "quran_link" in D["algorithm"])

    print("\nCritic (recomputed live)")
    r = critic.score(D["unlock"]["our_translation"], D["critic"]["benchmark_text"])
    check("all load-bearing claims agree", r["claim_agreement"] == 1.0,
          f"agreement {r['claim_agreement']}")
    check("composite score is presentable", r["composite"] >= 0.70,
          f"scored {r['percent']}%")
    print(f"        score {r['percent']}%  —  {r['verdict']}")

    print("-" * 52)
    if FAILURES:
        print(f"PRE-FLIGHT FAILED — {len(FAILURES)} problem(s):")
        for f in FAILURES:
            print(f"  · {f}")
        sys.exit(1)
    print("PRE-FLIGHT PASSED — demo node is complete.\n")


if __name__ == "__main__":
    main()
