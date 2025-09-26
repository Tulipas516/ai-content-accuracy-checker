import faiss, numpy as np, os, json
from typing import List

class VectorIndex:
    def __init__(self, dim: int, index_path: str):
        self.dim = dim
        self.index_path = index_path
        self.index = faiss.IndexFlatIP(dim)
        self.meta = []

    def add(self, vectors: np.ndarray, meta: List[dict]):
        assert vectors.shape[1] == self.dim
        self.index.add(vectors)
        self.meta.extend(meta)

    def search(self, query_vecs: np.ndarray, k: int = 5):
        D, I = self.index.search(query_vecs, k)
        results = []
        for q in range(I.shape[0]):
            items = []
            for score, idx in zip(D[q], I[q]):
                if idx == -1:
                    continue
                m = self.meta[idx].copy()
                m["score"] = float(score)
                items.append(m)
            results.append(items)
        return results

    def save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + ".meta.json", "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.index_path + ".meta.json", "r", encoding="utf-8") as f:
            self.meta = json.load(f)
