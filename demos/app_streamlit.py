import streamlit as st
from accchk.chunk import chunk_text
from accchk.retrieve import Retriever
from accchk.check import NLIEntailer, keyword_signal
from accchk.claims import extract_claims

st.title("LLM Accuracy Checker — Demo (src/ + pyproject)")

st.sidebar.header("Corpus")
uploaded = st.sidebar.file_uploader("Upload Markdown/HTML files", accept_multiple_files=True, type=["md","markdown","html","htm"])
if st.sidebar.button("Build Index"):
    if not uploaded:
        st.warning("Upload at least one file.")
    else:
        passages, meta = [], []
        for uf in uploaded:
            raw = uf.read().decode("utf-8", errors="ignore")
            chunks = chunk_text(raw, max_tokens=150, overlap=30)
            for i, ch in enumerate(chunks):
                passages.append(ch)
                meta.append({"doc_id": uf.name, "passage_id": f"{uf.name}#p{i}", "text": ch})
        retriever = Retriever(index_path="dist/streamlit.faiss")
        retriever.build(passages, meta, save=True)
        st.success(f"Indexed {len(passages)} passages.")

st.header("Check an Answer")
q = st.text_input("Question (optional)")
a = st.text_area("LLM Answer", height=160, value="Go to Accounting > Reconcile. Select the account and statement period; you may override the balance if the difference isn't $0.00.")
if st.button("Run Checker"):
    retriever = Retriever(index_path="dist/streamlit.faiss")
    nli = NLIEntailer(device=-1)
    claims = extract_claims(a)
    rows = []
    for c in claims:
        results = retriever.search([c], k=5)[0]
        best = None; best_v="Not Found"; best_conf=0.0
        for r in results:
            v, conf = nli.verdict(c, r["text"])
            kw = keyword_signal(c, r["text"])
            conf = conf*0.7 + kw*0.3
            if conf > best_conf:
                best_conf = conf; best_v=v; best=r
        rows.append({"claim": c, "verdict": best_v, "confidence": round(best_conf,3), "evidence": best["text"] if best else ""})
    st.json({"question": q, "answer": a, "report": rows})
