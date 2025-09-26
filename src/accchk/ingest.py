from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from .utils import sha256_of_text
import os, re, glob

def load_documents(path_glob):
    docs = []
    for p in glob.glob(path_glob):
        ext = os.path.splitext(p)[1].lower()
        raw = open(p, "r", encoding="utf-8", errors="ignore").read()
        if ext in [".md", ".markdown"]:
            text = md_to_text(raw)
        elif ext in [".html", ".htm"]:
            text = html_to_text(raw)
        else:
            continue
        docs.append({"id": os.path.basename(p), "path": p, "hash": sha256_of_text(raw), "text": text})
    return docs

def md_to_text(md):
    mdp = MarkdownIt()
    tokens = mdp.parse(md)
    lines = []
    for t in tokens:
        if t.type in ("inline", "code_block", "fence"):
            content = t.content.strip()
            if content:
                lines.append(content)
    return "\n".join(lines)

def html_to_text(html):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script","style","nav","header","footer","aside"]):
        tag.decompose()
    text = soup.get_text("\n")
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()
