import re
from pathlib import Path

import pickle

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "fake_news_model.pkl"
VECTORIZER_PATH = Path(__file__).resolve().parents[1] / "models" / "tfidf_vectorizer.pkl"

with MODEL_PATH.open("rb") as model_file:
    model = pickle.load(model_file)
with VECTORIZER_PATH.open("rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)


def clean_for_inference(text: str) -> str:
    clean = re.sub(r"http\S+|www\S+|https\S+", "", str(text).lower())
    clean = re.sub(r"[^a-zA-Z\s]", "", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def predict_fake_news(text: str) -> dict[str, object]:
    clean_text = clean_for_inference(text)
    vec = vectorizer.transform([clean_text])
    pred = str(model.predict(vec)[0]).upper()

    if hasattr(model, "decision_function"):
        raw_conf = float(abs(model.decision_function(vec)[0]))
        confidence = min(raw_conf, 1.0)
    else:
        confidence = float(max(model.predict_proba(vec)[0]))

    return {
        "prediction": pred,
        "confidence": confidence,
        "is_fake": pred == "FAKE",
    }


if __name__ == "__main__":
    article = "Breaking: shocking truth exposed by unknown sources"
    print(predict_fake_news(article))
