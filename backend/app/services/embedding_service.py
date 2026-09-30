import math
import os
import re
from collections import Counter

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

try:
    from sentence_transformers import SentenceTransformer, util
except ModuleNotFoundError:  # pragma: no cover - fallback for constrained envs
    SentenceTransformer = None
    util = None


model = None
USE_TRANSFORMER_MODEL = os.getenv("USE_TRANSFORMER_MODEL", "false").lower() == "true"


def _tokenize(text: str):
    return re.findall(r"[a-zA-Z0-9+-]+", text.lower())


def _fallback_embedding(text: str):
    tokens = _tokenize(text)
    return Counter(tokens)


def _cosine_similarity(counter1, counter2):
    common_terms = set(counter1) & set(counter2)
    dot = sum(counter1[t] * counter2[t] for t in common_terms)
    norm1 = math.sqrt(sum(v * v for v in counter1.values()))
    norm2 = math.sqrt(sum(v * v for v in counter2.values()))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)


def _get_model():
    global model
    if not USE_TRANSFORMER_MODEL:
        return None

    if model is None and SentenceTransformer is not None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def generate_embedding(text: str):
    model_instance = _get_model()
    if model_instance is not None:
        return model_instance.encode(text)
    return _fallback_embedding(text)


def calculate_semantic_similarity(text1: str, text2: str) -> float:
    try:
        embedding1 = generate_embedding(text1)
        embedding2 = generate_embedding(text2)

        if util is not None and hasattr(util, "cos_sim"):
            score = util.cos_sim(embedding1, embedding2).item()
            return round(float(score), 4)
    except Exception:
        pass

    fallback_score = _cosine_similarity(_fallback_embedding(text1), _fallback_embedding(text2))
    return round(float(fallback_score), 4)