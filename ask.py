"""
The Ask panel's matcher.

A child can type anything. Nothing here calls a model and nothing touches the
network — a question is matched against the lesson's own frozen answers, and if
it doesn't match, the panel says so.

That refusal is deliberate and is the point. algorism-code-spine.md §2.1: a
strong output template is an attractor, and a model asked a question with a
lineage-shaped hole in it will invent a scholar to fill it. The structural fix
is not to have a model in the loop at all. So there isn't one.
"""

import re

STOP = {
    "the", "a", "an", "is", "it", "to", "and", "in", "that", "this", "of",
    "do", "does", "did", "i", "you", "we", "my", "me", "for", "on", "at",
    "can", "could", "would", "should", "please", "tell", "explain", "about",
    "what", "how", "why", "when", "where", "which", "who", "so", "but", "if",
}


def normalise(text):
    text = (text or "").lower().replace("’", "'")
    text = re.sub(r"[^a-z0-9\s'\-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _tokens(text):
    return {t for t in normalise(text).split() if t not in STOP and len(t) > 1}


def score(question, phrases):
    """How well a question matches one answer's trigger phrases.

    A phrase appearing intact is decisive; otherwise fall back to shared
    content words, so a child who phrases it their own way still gets through.
    """
    q_norm = normalise(question)
    q_tokens = _tokens(question)
    best = 0.0
    for phrase in phrases:
        p_norm = normalise(phrase)
        if p_norm and p_norm in q_norm:
            best = max(best, 1.0)
            continue
        p_tokens = _tokens(phrase)
        if not p_tokens:
            continue
        overlap = len(q_tokens & p_tokens) / len(p_tokens)
        best = max(best, overlap * 0.9)
    return best


def answer(question, ask_block, threshold=0.5):
    """Return (answer_html, matched: bool).

    Below the threshold the lesson's own refusal is returned unchanged — it is
    frozen text, not something composed on the spot.
    """
    if not question or not question.strip():
        return None, False

    best_answer, best_score = None, 0.0
    for entry in ask_block.get("qa", []):
        s = score(question, entry.get("match", []))
        if s > best_score:
            best_answer, best_score = entry.get("answer"), s

    if best_answer and best_score >= threshold:
        return best_answer, True
    return ask_block.get("refusal", "I don't have a verified answer for that."), False


if __name__ == "__main__":
    import json
    from pathlib import Path

    block = json.loads(
        (Path(__file__).parent / "content" / "lessons" / "algebra.json").read_text()
    )["ask"]

    trials = [
        "why does completing the square actually work?",
        "where would I ever use this",
        "what if b is odd",
        "why is it called al jabr",
        "is it the same as the quadratic formula",
        "why did he draw a square",
        "who invented the periodic table",
        "what is the capital of France",
    ]
    for q in trials:
        text, matched = answer(q, block)
        print(f"[{'HIT ' if matched else 'MISS'}] {q}\n        {text[:88]}…\n")
