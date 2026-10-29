"""Retrieval-based support assistant (prototype).

Mirrors key ideas from the report:
- grounded answers: replies come only from the verified knowledge base
- escalation trigger: low retrieval confidence -> hand off to a human
- latency is measured per query
"""
import json
import time
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parent.parent


class SupportBot:
    def __init__(self, kb_path=ROOT / "data" / "kb.json", threshold=0.15):
        self.kb = json.load(open(kb_path, encoding="utf-8"))
        self.vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vec.fit_transform([k["text"] for k in self.kb])
        self.threshold = threshold

    def answer(self, question: str) -> dict:
        start = time.perf_counter()
        sims = cosine_similarity(self.vec.transform([question]), self.matrix)[0]
        i = int(sims.argmax())
        escalate = bool(sims[i] < self.threshold)
        return {
            "id": "none" if escalate else self.kb[i]["id"],
            "text": "Let me connect you to a human agent." if escalate else self.kb[i]["text"],
            "confidence": float(sims[i]),
            "escalated": escalate,
            "latency_ms": (time.perf_counter() - start) * 1000,
        }


if __name__ == "__main__":
    bot = SupportBot()
    print("Support assistant demo. Type 'quit' to exit.")
    while True:
        q = input("You: ").strip()
        if q.lower() in {"quit", "exit"}:
            break
        r = bot.answer(q)
        print(f"Bot ({r['confidence']:.2f}, escalated={r['escalated']}): {r['text']}\n")
