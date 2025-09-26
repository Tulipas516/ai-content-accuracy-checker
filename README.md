# AI Content Accuracy Checker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

---

**LLM Accuracy Checker for Fintech & Compliance**
✅ Ingest knowledge base articles
✅ Retrieve passages with semantic embeddings
✅ Check each claim in an answer with NLI
✅ Flag hallucinations before they reach end users

This project is a **guardrail against hallucination**. It demonstrates how to ground AI-generated answers in verified content, making them safer for use in **fintech, bookkeeping, and compliance-sensitive domains** where wrong answers create **regulatory, financial, or trust risks**.

---

## 🧱 Layout

```
ai-content-accuracy-checker/
  pyproject.toml
  LICENSE
  README.md
  DEMO_COMMANDS.md     # Copy-paste demo scenarios
  src/accchk/          # Core Python package
  examples/            # Sample KB articles
  demos/               # Streamlit app
  dist/                # Generated artifacts (ignored in Git)
```

---

## 📦 Install

> Python 3.10+ recommended. Use a virtualenv.

```bash
git clone https://github.com/tmorales2000/ai-content-accuracy-checker.git
cd ai-content-accuracy-checker
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .
```

This installs dependencies and exposes the console scripts:

* `accchk-build-index`
* `accchk-check-answer`

---

## 🚀 Quick Start

### 1. Build the index

```bash
accchk-build-index --glob "examples/*.md" --out dist/index.faiss
```

### 2. Check an LLM answer

```bash
accchk-check-answer \
  --question "How do I reconcile a bank account?" \
  --answer "Go to Accounting > Reconcile; you may override the balance if the difference isn't $0.00."
```

### Sample Output

```json
{
  "question": "How do I reconcile a bank account?",
  "answer": "Go to Accounting > Reconcile; you may override the balance if the difference isn't $0.00.",
  "claims": [
    {
      "text": "Go to Accounting > Reconcile",
      "verdict": "Supported",
      "confidence": 0.84,
      "citation": { "doc_id": "reconcile_accounts.md", ... }
    },
    {
      "text": "you may override the balance if the difference isn't $0.00",
      "verdict": "Contradicted",
      "confidence": 0.83,
      "citation": { "doc_id": "reconcile_accounts.md", ... }
    }
  ],
  "scores": { "faithfulness": 0.5 }
}
```

👉 For a full set of ready-to-run demos, see [DEMO_COMMANDS.md](DEMO_COMMANDS.md).

---

## 🔒 Why This Matters — Guarding Against Hallucination

Large language models are powerful but prone to **hallucination**: confidently inventing facts that sound plausible but are false. For fintech and compliance, hallucinations can:

* Misstate **tax thresholds** → regulatory risk
* Advise unsafe **bookkeeping practices** → corrupted financials
* Invent **UI flows** that don’t exist → frustrated customers

This checker demonstrates how to **intercept hallucinations** before they reach end users by verifying every claim against a trusted content base:

* **Supported** = grounded in your docs
* **Contradicted** = explicitly false compared to your docs
* **Not Found** = unverified (likely hallucination)

---

## 📚 Example KB Articles

The `examples/` folder contains both **realistic guides** and **designed contradictions** to show the checker in action:

* `reconcile_accounts.md` — Proper steps for bank reconciliation
* `bank_reconcile_tips.md` — Warns *not* to override balances
* `invoice_payments.md` — Fixing failed card payments (no “Tools menu”)
* `sales_tax_setup.md` — Destination-based tax setup
* `contractor_1099_rules.md` — Correct $600 reporting threshold
* `*_conflict.md` — Intentional contradictions for demo

---

## 🧪 Hallucination & Grounding Demos

After building the index:

```bash
accchk-build-index --glob "examples/*.md" --out dist/index.faiss
```

You can try inline demos (below) or copy-paste from [DEMO_COMMANDS.md](DEMO_COMMANDS.md).

### ✅ Supported

```bash
accchk-check-answer --question "How do I fix a failed invoice card payment?" \
  --answer "Open Sales > Invoices, choose the invoice, and click Receive payment. If a card payment fails, confirm the billing address and ZIP and then retry."
```

### ❌ Contradicted

```bash
accchk-check-answer --question "Can I override balances during reconciliation?" \
  --answer "Yes, if the difference is not $0.00 you can override the balance."
```

### ❓ Not Found (hallucination)

```bash
accchk-check-answer --question "Where is the sales tax setting?" \
  --answer "Go to the Tools menu in the top-right and choose Sales Tax Wizard."
```

### ❌ Wrong thresholds (regulatory risk)

```bash
accchk-check-answer --question "What's the 1099 threshold?" \
  --answer "Issue 1099s only when contractors are paid $800 or more."
```

### ⚠️ Mixed (partial support)

```bash
accchk-check-answer --question "How does AcmeBooks handle California sales tax?" \
  --answer "AcmeBooks calculates destination-based sales tax and automatically applies city add-ons for California."
```

---

## 🖥️ Streamlit Demo

```bash
streamlit run demos/app_streamlit.py
```

* Upload Markdown/HTML help files
* Paste an LLM answer
* Get verdicts & citations

---

## 📈 Easy Extensions

* Add numeric/date validators (thresholds, deadlines)
* CI/CD gate: fail builds if faithfulness < 0.8
* Style/brand compliance checks
* Evidence reranking for better citations

---

## 🔍 Discoverability

* Repo topics: `llm`, `rag`, `hallucination`, `accuracy`, `fintech`, `nli`, `faiss`, `sentence-transformers`, `streamlit`
* Keywords in description & README: **LLM accuracy checker, hallucination guardrail, fintech compliance, FAISS, RAG, NLI, RoBERTa-MNLI**
* See [DEMO_COMMANDS.md](DEMO_COMMANDS.md) for copy-paste scenarios.

---

## ✅ License

MIT — see [LICENSE](LICENSE).
