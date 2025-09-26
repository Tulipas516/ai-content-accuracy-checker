from transformers import pipeline
from rapidfuzz import fuzz

class NLIEntailer:
    def __init__(self, model_name: str = "roberta-large-mnli", device: int = -1):
        # do NOT pass return_all_scores here; it’s deprecated
        self.pipe = pipeline(
            "text-classification",
            model=model_name,
            tokenizer=model_name,
            device=device,
        )

    def _normalize_scores(self, outputs):
        """
        Normalize various pipeline return shapes to a list of {'label', 'score'} dicts.
        Handles:
          - [{'label': 'ENTAILMENT', 'score': 0.9}, ...]
          - {'labels': [...], 'scores': [...]}
          - {'label': 'ENTAILMENT', 'score': 0.9}  (top-1)
        """
        # list of dicts (desired)
        if isinstance(outputs, list) and outputs and isinstance(outputs[0], dict) and "label" in outputs[0]:
            return [{"label": d["label"].lower(), "score": float(d["score"])} for d in outputs]

        # dict with parallel arrays
        if isinstance(outputs, dict) and "labels" in outputs and "scores" in outputs:
            return [{"label": l.lower(), "score": float(s)} for l, s in zip(outputs["labels"], outputs["scores"])]

        # single dict (top-1)
        if isinstance(outputs, dict) and "label" in outputs:
            return [{"label": outputs["label"].lower(), "score": float(outputs.get("score", 0.0))}]

        return []

    def verdict(self, claim: str, evidence: str):
        # Ask for all scores explicitly with top_k=None
        raw = self.pipe({"text": evidence, "text_pair": claim}, top_k=None)[0]
        scores = self._normalize_scores(raw)

        # Map labels → scores, tolerate naming variants
        score_map = {d["label"]: d["score"] for d in scores}
        # common label keys in MNLI heads
        entail = score_map.get("entailment", 0.0)
        contra = score_map.get("contradiction", score_map.get("contradictory", 0.0))
        neutral = score_map.get("neutral", 0.0)

        if entail >= max(contra, neutral):
            return "Supported", entail
        elif contra >= max(entail, neutral):
            return "Contradicted", contra
        else:
            return "Not Found", neutral

def keyword_signal(a: str, b: str):
    return fuzz.token_set_ratio(a, b) / 100.0
