import argparse, json
from .retrieve import Retriever
from .claims import extract_claims
from .check import NLIEntailer, keyword_signal
from .ingest import load_documents
from .chunk import chunk_text
from .utils import write_json

def build_index_main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="examples/*.md", help="Path glob to docs")
    ap.add_argument("--out", default="dist/index.faiss", help="Index path")
    args = ap.parse_args()

    docs = load_documents(args.glob)
    passages, meta = [], []
    for d in docs:
        chunks = chunk_text(d["text"], max_tokens=150, overlap=30)
        for i, ch in enumerate(chunks):
            passages.append(ch)
            meta.append({"doc_id": d["id"], "passage_id": f"{d['id']}#p{i}", "text": ch})
    retriever = Retriever(index_path=args.out)
    retriever.build(passages, meta, save=True)
    write_json("dist/corpus_meta.json", {"docs": [ {"id": d["id"], "path": d["path"], "hash": d["hash"]} for d in docs ]})
    print(f"Indexed {len(passages)} passages from {len(docs)} docs → {args.out}")

def check_answer_main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=False, default="", help="User question (optional)")
    ap.add_argument("--answer", required=True, help="LLM answer to verify")
    ap.add_argument("--k", type=int, default=5, help="Top-k passages per claim")
    ap.add_argument("--index", default="dist/index.faiss", help="Path to FAISS index")
    ap.add_argument("--device", type=int, default=-1, help="Transformers device (-1 cpu, 0 cuda)")
    args = ap.parse_args()

    claims = extract_claims(args.answer)
    retriever = Retriever(index_path=args.index)
    nli = NLIEntailer(device=args.device)

    report = {"question": args.question, "answer": args.answer, "claims": [], "scores": {}}
    supported = 0
    for cid, c in enumerate(claims, start=1):
        results = retriever.search([c], k=args.k)[0]
        best = None; best_verdict = "Not Found"; best_conf = 0.0
        for r in results:
            verdict, conf = nli.verdict(c, r["text"])
            kw = keyword_signal(c, r["text"])
            conf = (conf*0.7 + kw*0.3)
            if conf > best_conf:
                best_conf = conf; best_verdict = verdict; best = r
        entry = {"id": f"c{cid}", "text": c, "verdict": best_verdict, "confidence": round(float(best_conf), 3), "citation": best}
        if best_verdict == "Supported":
            supported += 1
        report["claims"].append(entry)

    report["scores"]["faithfulness"] = round(supported / max(1, len(claims)), 3)
    print(json.dumps(report, indent=2, ensure_ascii=False))
