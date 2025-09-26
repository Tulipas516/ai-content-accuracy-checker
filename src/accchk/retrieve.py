from .embed import Embedder
from .index import VectorIndex

class Retriever:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2", index_path="dist/index.faiss"):
        self.embedder = Embedder(model_name)
        self.index_path = index_path
        self.index = None

    def build(self, passages, meta, save=True):
        vecs = self.embedder.encode(passages)
        self.index = VectorIndex(vecs.shape[1], self.index_path)
        self.index.add(vecs, meta)
        if save:
            self.index.save()

    def load(self):
        if self.index is None:
            self.index = VectorIndex(384, self.index_path)
            self.index.load()

    def search(self, queries, k=5):
        self.load()
        qvecs = self.embedder.encode(queries)
        return self.index.search(qvecs, k=k)
