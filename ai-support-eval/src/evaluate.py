"""Evaluate the bot on the golden set and sweep the escalation threshold."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from bot import SupportBot

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def evaluate(threshold: float, df: pd.DataFrame) -> dict:
    bot = SupportBot(threshold=threshold)
    rows = [bot.answer(q) for q in df.question]
    pred = pd.Series([r["id"] for r in rows])
    esc = pd.Series([r["escalated"] for r in rows])
    lat = pd.Series([r["latency_ms"] for r in rows])
    exp = df.expected_id.reset_index(drop=True)
    answerable = exp != "none"
    return {
        "threshold": threshold,
        "accuracy_%": (pred == exp).mean() * 100,
        "containment_%": (~esc).mean() * 100,
        "wrong_answer_rate_%": ((pred != exp) & ~esc).mean() * 100,
        "correct_escalation_%": esc[~answerable].mean() * 100,
        "missed_answerable_%": esc[answerable].mean() * 100,
        "p95_latency_ms": lat.quantile(0.95),
    }


def main():
    df = pd.read_csv(ROOT / "data" / "golden.csv")
    sweep = pd.DataFrame([evaluate(t, df) for t in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40]]).round(2)
    sweep.to_csv(RESULTS / "threshold_sweep.csv", index=False)
    print(f"Golden set size: {len(df)}\n")
    print(sweep.to_string(index=False))

    base = sweep[sweep.threshold == 0.15].iloc[0]
    base.to_csv(RESULTS / "metrics.csv", header=["value"])

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    for col in ["accuracy_%", "containment_%", "wrong_answer_rate_%", "correct_escalation_%"]:
        ax.plot(sweep.threshold, sweep[col], marker="o", label=col)
    ax.set_xlabel("Escalation confidence threshold")
    ax.set_ylabel("Percent")
    ax.set_title("Quality vs. containment trade-off")
    ax.legend(frameon=False, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(RESULTS / "threshold_tradeoff.png")


if __name__ == "__main__":
    main()
