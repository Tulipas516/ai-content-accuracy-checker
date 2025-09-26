# AI Content Starter — LLM Accuracy Checker

**Purpose:** A minimal, working demo that ingests help-style content, builds a retrieval index, and checks whether an LLM’s answer is **Supported / Contradicted / Not Found** by your sources — with citations.

This project is a **guardrail against hallucination**. It demonstrates how to ground AI-generated answers in verified content, making them safer for production use in **fintech and other compliance-sensitive domains** (e.g., tax, payments, bookkeeping).

---

## 🧱 Layout

```
ai-content-starter/
  pyproject.toml
  LICENSE
  README.md
  DEMO_COMMANDS.md     # Ready-to-run demo scenarios
  src/
    accchk/
      __init__.py
      utils.py
      ingest.py
      chunk.py
      embed.py
      index.py
      claims.py
      check.py
      retrieve.py
      cli.py
  examples/            # Sample KB articles
  demos/
    app_streamlit.py   # Optional UI
  dist/                # Generated artifacts
```

---

## 📦 Install (editable)

> Python 3.10+ recommended. Use a virtualenv.

```bash
git clone https://github.com/tmorales2000/ai-content-starter.git
cd ai-content-starter
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .
```

This installs dependencies and exposes the console scripts on your PATH:

* `accchk-build-index`
* `accchk-check-answer`

---

## 🚀 Quick Start (CLI)

### 1. Build the index

```bash
accchk-build-index --glob "examples/*.md" --out dist/index.faiss
```

### 2. Check an LLM answer

```bash
accchk-check-answer \
  --question 'How do I reconcile a bank account?' \
  --answer 'Go to Accounting > Reconcile; you may override the balance if the difference isn'\''t $0.00.'
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

👉 For ready-made demo scenarios, check out [DEMO_COMMANDS.md](DEMO_COMMANDS.md).

---

## 🔒 Why This Matters — Guarding Against Hallucination

LLMs are powerful but prone to **hallucination**: confidently inventing facts that sound plausible but are false. For financial and compliance-sensitive domains, hallucinations can:

* Misstate tax thresholds (→ regulatory risk)
* Advise unsafe bookkeeping practices (→ corrupted financials)
* Invent UI flows that don’t exist (→ frustrated customers)

This checker demonstrates how to **intercept hallucinations before they reach end users** by verifying every claim against a trusted content base.

* **Supported** = grounded in your docs
* **Contradicted** = explicitly false compared to your docs
* **Not Found** = unverified (likely hallucination)

---

## 📚 Example KB Articles

The `examples/` folder contains both **realistic guides** and **designed contradictions** to demonstrate checks in action:

* `reconcile_accounts.md` — Proper steps for bank reconciliation
* `bank_reconcile_tips.md` — Explicitly warns not to override balances
* `invoice_payments.md` — Fixing failed card payments, no “Tools menu”
* `sales_tax_setup.md` — Destination-based sales tax, manual CA add-ons
* `contractor_1099_rules.md` — Correct $600 reporting threshold
* `*_conflict.md` — Introduces intentional contradictions

---

## 🧪 Hallucination & Grounding Demos

After rebuilding the index:

```bash
accchk-build-index --glob "examples/*.md" --out dist/index.faiss
```

You can run demos inline, or copy-paste from [DEMO_COMMANDS.md](DEMO_COMMANDS.md).

### ✅ Supported

```bash
accchk-check-answer \
  --question "How do I fix a failed invoice card payment?" \
  --answer 'Open Sales > Invoices, choose the invoice, and click Receive payment. If a card payment fails, confirm the billing address and ZIP and then retry.'
```

### ❌ Contradicted

```bash
accchk-check-answer \
  --question "Can I override balances during reconciliation?" \
  --answer "Yes, if the difference is not $0.00 you can override the balance to complete reconciliation."
```

### ❓ Not Found (hallucination)

```bash
accchk-check-answer \
  --question "Where is the sales tax setting?" \
  --answer "Go to the Tools menu in the top-right and choose Sales Tax Wizard."
```

### ❌ Wrong thresholds (regulatory risk)

```bash
accchk-check-answer \
  --question "What's the 1099 threshold?" \
  --answer "Issue 1099s only when contractors are paid $800 or more in the tax year."
```

### ⚠️ Mixed (partial support)

```bash
accchk-check-answer \
  --question "How does AcmeBooks handle California sales tax?" \
  --answer "AcmeBooks calculates destination-based sales tax and automatically applies city add-ons for California."
```

---

## 🖥️ Streamlit Demo

```bash
streamlit run demos/app_streamlit.py
```

* Upload Markdown/HTML help files
* Paste an LLM answer
* Get verdicts and citations in JSON

---

## 📈 Easy Extensions

* Add numeric/date validators (e.g., thresholds, deadlines)
* CI/CD gate: fail builds if faithfulness < 0.8
* Style/brand compliance checks
* Rerankers for better evidence quality

---

## ✅ License

MIT — see `LICENSE`.
