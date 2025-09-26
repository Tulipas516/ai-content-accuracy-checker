import re
from typing import List

def split_into_sentences(text: str) -> List[str]:
    sents = re.split(r'(?<=[.?!])\s+(?=[A-Z0-9])', text.strip())
    return [s.strip() for s in sents if s.strip()]

def chunk_text(text: str, max_tokens: int = 150, overlap: int = 30) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i:i+max_tokens]
        chunks.append(" ".join(chunk_words))
        i += max_tokens - overlap
    return chunks
