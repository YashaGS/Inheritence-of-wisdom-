"""
Deterministic critic.

Per algorism-code-spine.md §2.3: the confidence score is computed IN CODE from
two texts. A model never reports its own confidence — that is the exact failure
mode the whole architecture exists to prevent.

No network. No model call. Same inputs -> same number, every time.
"""

import re
from difflib import SequenceMatcher

# Number words that carry the mathematical claims in this passage. If the
# translation and the benchmark disagree on any of these, the reading is wrong
# in a way that matters, regardless of how fluent the prose is.
LOAD_BEARING = [
    "five", "twenty-five", "thirty-nine", "sixty-four",
    "eight", "three", "nine", "ten",
]

_STOP = {
    "the", "of", "a", "an", "is", "it", "to", "and", "in", "that", "this",
    "which", "you", "your", "by", "for", "be", "as", "with", "its", "what",
    "when", "so", "then", "are", "was", "were", "at", "on", "from", "he",
}


def normalise(text: str) -> str:
    """Lowercase, strip punctuation and curly quotes, collapse whitespace."""
    text = text.lower()
    text = text.replace("“", " ").replace("”", " ")
    text = text.replace("’", "'").replace("—", " ")
    # keep hyphens: "thirty-nine" is one token and it is load-bearing
    text = re.sub(r"[^a-z0-9\-\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def content_tokens(text: str) -> list:
    return [t for t in normalise(text).split() if t not in _STOP and len(t) > 1]


def lexical_overlap(a: str, b: str) -> float:
    """Jaccard overlap on content words. Order-insensitive."""
    ta, tb = set(content_tokens(a)), set(content_tokens(b))
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def sequence_ratio(a: str, b: str) -> float:
    """Order-sensitive similarity — catches a reading that has the right words
    in the wrong procedural order.

    Compared over token lists, not characters: at character level the autojunk
    heuristic classes any character appearing in >1% of a long string as junk,
    which is every letter, and the ratio collapses toward zero.
    """
    return SequenceMatcher(
        None, content_tokens(a), content_tokens(b), autojunk=False
    ).ratio()


def claim_agreement(a: str, b: str):
    """The part that actually matters: do both texts assert the same numbers?

    Returns (fraction_agreed, per_term_detail).
    """
    na, nb = normalise(a), normalise(b)
    detail = []
    for term in LOAD_BEARING:
        in_a, in_b = term in na, term in nb
        detail.append({
            "term": term,
            "in_translation": in_a,
            "in_benchmark": in_b,
            "agree": in_a == in_b,
        })
    agreed = sum(1 for d in detail if d["agree"])
    return agreed / len(detail), detail


def score(translation: str, benchmark: str) -> dict:
    """Composite confidence. Claim agreement dominates deliberately — a fluent
    paraphrase that gets a number wrong must score worse than clumsy prose that
    gets every number right."""
    lex = lexical_overlap(translation, benchmark)
    seq = sequence_ratio(translation, benchmark)
    claims, detail = claim_agreement(translation, benchmark)

    composite = (0.60 * claims) + (0.25 * lex) + (0.15 * seq)

    if claims < 1.0:
        verdict = "DIVERGENT — a load-bearing number disagrees. Do not teach from this."
        band = "fail"
    elif composite >= 0.75:
        verdict = "VERIFIED — every load-bearing claim matches the benchmark."
        band = "high"
    else:
        verdict = "VERIFIED ON CLAIMS — numbers agree; wording diverges from Rosen."
        band = "medium"

    return {
        "composite": round(composite, 4),
        "percent": round(composite * 100, 1),
        "claim_agreement": round(claims, 4),
        "lexical_overlap": round(lex, 4),
        "sequence_ratio": round(seq, 4),
        "verdict": verdict,
        "band": band,
        "detail": detail,
    }


if __name__ == "__main__":
    import json
    from pathlib import Path

    data = json.loads(
        (Path(__file__).parent / "content" / "lessons" / "algebra.json").read_text()
    )
    result = score(data["unlock"]["our_translation"], data["critic"]["benchmark_text"])
    print(json.dumps({k: v for k, v in result.items() if k != "detail"}, indent=2))
    for d in result["detail"]:
        mark = "ok" if d["agree"] else "MISMATCH"
        print(f"  [{mark}] {d['term']}")
