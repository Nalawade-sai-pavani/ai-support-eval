# 🤖 AI Support Assistant: Prototype & Evaluation

> A small customer-support assistant that **answers only from verified policies** and **hands over to a human when it isn't sure**, plus a test harness that measures how well it works. 📊

👤 **Author:** _your name here_  📅 **Task:** Week 4, AI Solution Evaluation and Future Enhancement Proposal

---

## ✨ Features

| | Feature | What it does |
|---|---|---|
| 💬 | Chat assistant | Matches a question to the best of 12 verified policy answers |
| 🛡️ | Grounded answers | Never invents text, so it cannot hallucinate policy |
| 🙋 | Human escalation | Low confidence → "Let me connect you to a human agent" |
| 🎚️ | Adjustable threshold | Trade off wrong answers against how many chats the bot keeps |
| 🧪 | Test harness | Runs 44 labelled questions and reports accuracy, containment and more |
| 🌐 | Visual web demo | Chat, live confidence meter, threshold slider and a one-click test run |

---

## 📁 Project structure

```
ai-support-eval/
├── 📂 data/
│   ├── kb.json            12 verified policy answers
│   └── golden.csv         44 test questions (34 answerable, 10 out-of-scope)
├── 📂 src/
│   ├── bot.py             retrieval bot with escalation (also a CLI chat demo)
│   └── evaluate.py        metrics, threshold sweep and chart
├── 📂 web/
│   └── index.html         visual chat prototype (single file)
├── 📂 results/            generated metrics, sweep table and charts
├── 📄 requirements.txt
└── 📄 README.md
```

---

## 🚀 Quick start

### 1️⃣ Set up (VS Code terminal)
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac / Linux
pip install -r requirements.txt
```
🧭 Then choose the `.venv` interpreter: `Ctrl+Shift+P` → **Python: Select Interpreter**.

### 2️⃣ Run the evaluation 📊
```bash
python src/evaluate.py
```
Creates `results/metrics.csv`, `results/threshold_sweep.csv` and `results/threshold_tradeoff.png`.

### 3️⃣ Chat in the terminal 💬
```bash
python src/bot.py
```
Try: `I forgot my password`, `Can I pay with UPI`, `Tell me a joke`. Type `quit` to exit.

### 4️⃣ Open the visual prototype 🌐
```bash
python -m http.server 8000 --directory web
```
Then open **http://localhost:8000** (keep the terminal running).
Prefer a button? Install the **Live Server** extension, right-click `web/index.html` → **Open with Live Server**.

---

## 📈 Results (threshold 0.15)

| Metric | Result |
|---|---|
| ✅ Answer accuracy | **70.5%** |
| 🤝 Containment (no human needed) | **65.9%** |
| ❌ Confident but wrong | **15.9%** |
| 🚦 Off-topic questions escalated | **100%** (10 of 10) |
| ⏱️ p95 latency | about **1 ms** |

### 🎚️ The trade-off

| Threshold | Accuracy | Containment | Wrong answers |
|---|---|---|---|
| 0.05 | 75.0% | 72.7% | 18.2% |
| 0.15 | 70.5% | 65.9% | 15.9% |
| 0.25 | 59.1% | 50.0% | 11.4% |
| 0.40 | 43.2% | 25.0% | 2.3% |

💡 **Takeaway:** a higher threshold makes the bot safer (fewer wrong answers) but sends more chats to humans. Containment alone can be misleading, so it should always be read together with quality metrics.

---

## 🧠 How it works

1. 🔎 The question is turned into a TF-IDF vector.
2. 📐 Cosine similarity finds the closest policy answer.
3. 🚦 If the score is **below the threshold**, the chat goes to a human; otherwise the policy text is returned.
4. 🧪 `evaluate.py` repeats this for every test question and compares with the expected answer.

---

## ⚠️ Limitations

- 🔤 Keyword (TF-IDF) matching struggles with paraphrases. For example, `how long for refund` is wrongly matched to the damaged-item answer.
- 📏 44 hand-written test questions are too few for statistical confidence.
- 🚫 No LLM generation, so hallucination is approximated by the wrong-answer rate.
- 🌍 English only.

---

## 🗺️ Next steps

- [ ] 🧬 Replace TF-IDF with embedding-based hybrid search and a re-ranker
- [ ] 🧾 Add an LLM answer step with citations and a groundedness check
- [ ] 🔀 Add model routing, caching and a load test for p95 latency
- [ ] 🌏 Expand the test set to 500+ cases, including multilingual and adversarial questions
- [ ] 👥 Improve the human handoff with a conversation summary

---

## 📚 Context

This repository accompanies the report **"AI Solution Evaluation and Future Enhancement Proposal"**. 📝
All data is small and illustrative: it demonstrates the evaluation method, **not** production performance.

Made with 🐍 Python, 📊 scikit-learn and ☕ patience.
