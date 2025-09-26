# AI Content Accuracy Checker

**LLM Guardrails for Fintech & Compliance**

This project demonstrates how to **verify LLM answers against trusted knowledge bases** using:
- FAISS + sentence-transformers for retrieval
- RoBERTa-MNLI for natural language inference
- JSON verdicts for *Supported / Contradicted / Not Found*

## Why it matters
LLMs hallucinate. In fintech, hallucinations aren’t just inconvenient — they can create **regulatory, financial, and trust risks**. This repo provides a minimal but functional framework for catching ungrounded claims before they reach end users.

## Quick Start
```bash
pip install -e .
accchk-build-index --glob "examples/*.md" --out dist/index.faiss
accchk-check-answer --question "How do I reconcile a bank account?" \\
  --answer "Go to Accounting > Reconcile; you may override the balance if the difference isn't $0.00."
```

## Demos
See [DEMO_COMMANDS.md](../DEMO_COMMANDS.md) for copy-paste examples of:
- ✅ Supported  
- ❌ Contradicted  
- ❓ Not Found (hallucination)  
- ⚠️ Mixed / Partial Support  

## Project Links
- [GitHub Repository](https://github.com/YOURUSER/ai-content-accuracy-checker)
- [License (MIT)](../LICENSE)
