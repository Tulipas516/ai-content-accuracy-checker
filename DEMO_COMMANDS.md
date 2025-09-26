# Hallucination & Grounding Demos

Below are copy/paste commands that intentionally test **supported**, **contradicted**, and **not found** scenarios.

> Make sure you've built an index that includes the new examples:
>
> ```bash
> accchk-build-index --glob "examples/*.md" --out dist/index.faiss
> ```

## ✅ Supported
```bash
accchk-check-answer   --question "How do I fix a failed invoice card payment?"   --answer 'Open Sales > Invoices, choose the invoice, and click Receive payment. If a card payment fails, confirm the billing address and ZIP and then retry.'
```

Expected: both claims **Supported** with citations from `invoice_payments.md`.

## ❌ Contradicted (unsafe advice)
```bash
accchk-check-answer   --question "Can I override balances during reconciliation?"   --answer "Yes, if the difference is not $0.00 you can override the balance to complete reconciliation."
```

Expected: **Contradicted** with evidence from `bank_reconcile_tips.md` ("Do not override balances").

## ❓ Not Found (hallucinated UI)
```bash
accchk-check-answer   --question "Where is the sales tax setting?"   --answer "Go to the Tools menu in the top-right and choose Sales Tax Wizard."
```

Expected: **Not Found** (no 'Tools' menu in examples) or **Contradicted** via `invoice_payments.md` note.

## ❌ Wrong thresholds (regulatory risk)
```bash
accchk-check-answer   --question "What's the 1099 threshold?"   --answer "Issue 1099s only when contractors are paid $800 or more in the tax year."
```

Expected: **Contradicted** with evidence from `contractor_1099_rules.md` ($600 threshold).

## ⚠️ Mixed answer (partial support)
```bash
accchk-check-answer   --question "How does AcmeBooks handle California sales tax?"   --answer "AcmeBooks calculates destination-based sales tax and automatically applies city add-ons for California."
```

Expected: first clause **Supported** (destination-based), second clause **Contradicted** (no auto city add-ons).
