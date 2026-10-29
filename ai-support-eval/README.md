# AI Support Assistant: Prototype and Evaluation Harness

Companion project to the report **"AI Solution Evaluation and Future Enhancement Proposal"**.
It builds a small retrieval-based customer support assistant and measures it with the same
metrics defined in the report (accuracy, containment, wrong-answer rate, escalation quality, latency).

> The knowledge base and test set are small, hand-written and **illustrative**. Results demonstrate
> the evaluation method, not production performance.

## What it demonstrates
| Report idea | Where in the code |
|---|---|
| Grounded answers (RAG principle) | `src/bot.py` returns text only from `data/kb.json` |
| Escalation triggers | low-confidence retrieval -> "connect to human" |
| Golden test set + regression metrics | `data/golden.csv`, `src/evaluate.py` |
| Containment vs. quality trade-off | threshold sweep + chart in `results/` |
| p95 latency tracking | `latency_ms` per query |

## Project structure
```
ai-support-eval/
├── data/kb.json            12 verified policy answers
├── data/golden.csv         44 test questions (34 answerable, 10 out-of-scope)
├── src/bot.py              TF-IDF retrieval bot with escalation (also an interactive demo)
├── src/evaluate.py         metrics + threshold sweep + chart
├── web/index.html          visual chat prototype (open in a browser)
├── results/                generated metrics, sweep table, chart
├── requirements.txt
└── .gitignore
```

## Setup (VS Code terminal)
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
```
Then select the `.venv` interpreter: `Ctrl+Shift+P` -> **Python: Select Interpreter**.

## Run
```bash
python src/evaluate.py     # metrics, sweep table and chart in results/
python src/bot.py          # interactive chat demo
```

## Visual prototype (web)
`web/index.html` is a single-file browser version of the assistant with a chat window, a live
confidence meter, a threshold slider, session stats and a button that runs the 44-question test set.

Run it from the VS Code terminal:
```bash
python -m http.server 8000 --directory web
```
Then open http://localhost:8000 in your browser. (Or install the **Live Server** extension, right-click
`web/index.html` and choose **Open with Live Server**.)

## Results (threshold sweep on the golden set)
See `results/threshold_sweep.csv` and `results/threshold_tradeoff.png`.

Raising the confidence threshold lowers the wrong-answer rate but also lowers containment, because
more queries go to a human. This is the same trade-off discussed in the report: containment alone can
be misleading and must be paired with quality metrics. The default threshold (0.15) is a compromise
chosen from the sweep.

## Limitations
- Keyword (TF-IDF) retrieval cannot handle paraphrases as well as embeddings or an LLM.
- 44 test questions is too few for statistical confidence.
- No LLM generation, so no hallucination measurement beyond wrong-answer rate.

## Next steps (from the report roadmap)
1. Replace TF-IDF with embedding-based hybrid search and a re-ranker.
2. Add an LLM generation step with a groundedness check and citations.
3. Add model routing, caching and a load test for p95 latency.
4. Expand the golden set to 500+ cases, including multilingual and adversarial questions.
