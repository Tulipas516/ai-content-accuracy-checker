from .chunk import split_into_sentences
import re

def extract_claims(answer: str):
    base = split_into_sentences(answer)
    claims = []
    for s in base:
        parts = re.split(r";|\band\b", s, flags=re.IGNORECASE)
        for p in parts:
            c = p.strip().strip("-•")
            if len(c) > 0:
                claims.append(c)
    return [c for c in claims if len(c.split()) >= 3]
