import argparse
import pickle
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score,
    brier_score_loss,
)
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.text_processor import clean_text

DEFAULT_TEST_SIZE = 0.2
RANDOM_STATE = 42
MIN_ACCURACY = 0.85
MIN_MODEL_SIZE_BYTES = 1_000_000

LIAR_COLUMNS = [
    "id",
    "label",
    "statement",
    "subjects",
    "speaker",
    "speaker_job_title",
    "state_info",
    "party_affiliation",
    "barely_true_counts",
    "false_counts",
    "half_true_counts",
    "mostly_true_counts",
    "pants_on_fire_counts",
    "context",
]


def _read_primary_dataset(fake_csv: Path, real_csv: Path) -> pd.DataFrame:
    fake_df = pd.read_csv(fake_csv)
    fake_df["label"] = "FAKE"

    real_df = pd.read_csv(real_csv)
    real_df["label"] = "REAL"

    combined = pd.concat([fake_df, real_df], ignore_index=True)
    return combined


def _read_backup_dataset(dataset_csv: Path) -> pd.DataFrame:
    df = pd.read_csv(dataset_csv)
    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("Backup dataset must contain 'text' and 'label' columns.")
    normalized = df.copy()
    normalized["label"] = normalized["label"].astype(str).str.upper()
    return normalized


def _map_liar_label(label: str, half_true_to: str) -> str:
    normalized = str(label).strip().lower()
    real_labels = {"true", "mostly-true"}
    fake_labels = {"false", "barely-true", "pants-fire", "pants on fire"}

    if normalized == "half-true":
        return half_true_to
    if normalized in real_labels:
        return "REAL"
    if normalized in fake_labels:
        return "FAKE"

    return "UNKNOWN"


def _read_liar_dataset(liar_dir: Path, half_true_to: str) -> pd.DataFrame:
    splits = ["train.tsv", "valid.tsv", "test.tsv"]
    frames = []

    for split in splits:
        path = liar_dir / split
        if not path.exists():
            raise FileNotFoundError(f"Missing LIAR split file: {path}")

        split_df = pd.read_csv(path, sep="\t", header=None, names=LIAR_COLUMNS)
        frames.append(split_df)

    df = pd.concat(frames, ignore_index=True)
    mapped = df["label"].apply(lambda value: _map_liar_label(value, half_true_to))

    out = pd.DataFrame({"text": df["statement"], "label": mapped})
    out = out[out["label"].isin(["REAL", "FAKE"])].copy()
    return out


def _make_model(model_name: str):
    if model_name == "passive-aggressive":
        return PassiveAggressiveClassifier(
            max_iter=100,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=5,
            random_state=RANDOM_STATE,
        )
    if model_name == "logistic":
        return LogisticRegression(
            max_iter=200,
            random_state=RANDOM_STATE,
            n_jobs=None,
        )
    raise ValueError("Unsupported model. Choose: passive-aggressive or logistic")


def _verify_artifact_size(path: Path, strict_size_check: bool) -> None:
    size = path.stat().st_size
    if size < MIN_MODEL_SIZE_BYTES:
        message = (
            f"Artifact smaller than 1MB: {path.name} is {size} bytes "
            f"(< {MIN_MODEL_SIZE_BYTES}). This can still be valid for linear models."
        )
        if strict_size_check:
            raise RuntimeError(message)
        print(f"WARNING: {message}")


def train(
    out_dir: Path,
    model_name: str,
    strict_size_check: bool,
    min_accuracy: float,
    liar_dir: Path | None,
    liar_half_true_to: str,
    fake_csv: Path | None = None,
    real_csv: Path | None = None,
    dataset_csv: Path | None = None,
) -> None:
    print("Loading dataset...")
    if liar_dir:
        df = _read_liar_dataset(liar_dir, liar_half_true_to)
    elif fake_csv and real_csv:
        df = _read_primary_dataset(fake_csv, real_csv)
    elif dataset_csv:
        df = _read_backup_dataset(dataset_csv)
    else:
        raise ValueError(
            "Provide --liar-dir OR provide --fake and --real OR provide --dataset."
        )

    if "text" not in df.columns:
        raise ValueError("Missing 'text' column in dataset.")
    if "label" not in df.columns:
        raise ValueError("Missing 'label' column in dataset.")

    print(f"Loaded rows: {len(df)}")
    print(f"Nulls -> text: {df['text'].isna().sum()}, label: {df['label'].isna().sum()}")

    print("Cleaning text...")
    preview_before = df["text"].head(3).astype(str).tolist()
    df["clean_text"] = df["text"].astype(str).apply(clean_text)
    df = df.dropna(subset=["clean_text", "label"])
    df = df[df["clean_text"].str.len() > 0]
    df["label"] = df["label"].astype(str).str.upper()

    preview_after = df["clean_text"].head(3).tolist()
    print("Sample before cleaning (3 rows):")
    for idx, row in enumerate(preview_before, start=1):
        print(f"  {idx}. {row[:120]}")
    print("Sample after cleaning (3 rows):")
    for idx, row in enumerate(preview_after, start=1):
        print(f"  {idx}. {row[:120]}")

    x = df["clean_text"]
    y = df["label"]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=DEFAULT_TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )
    print(f"Train size: {len(x_train)} | Test size: {len(x_test)}")

    print("Fitting TF-IDF vectorizer...")
    tfidf = TfidfVectorizer(
        max_features=5000,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.8,
    )
    x_train_tfidf = tfidf.fit_transform(x_train)
    x_test_tfidf = tfidf.transform(x_test)
    print(f"TF-IDF train matrix: {x_train_tfidf.shape}")
    print(f"TF-IDF test matrix: {x_test_tfidf.shape}")

    print(f"Training model: {model_name}")
    model = _make_model(model_name)
    model.fit(x_train_tfidf, y_train)

    y_pred = model.predict(x_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    # Compute advanced metrics
    f1_macro = f1_score(y_test, y_pred, average="macro")
    f1_weighted = f1_score(y_test, y_pred, average="weighted")
    
    # For AUROC, we need probabilities
    y_pred_proba = None
    auroc = None
    brier = None
    if hasattr(model, "predict_proba"):
        y_pred_proba = model.predict_proba(x_test_tfidf)
        # Convert to binary (probability of FAKE class)
        classes = model.classes_
        fake_idx = list(classes).index("FAKE") if "FAKE" in classes else 0
        y_pred_proba_fake = y_pred_proba[:, fake_idx]
        y_test_binary = (y_test == "FAKE").astype(int)
        auroc = roc_auc_score(y_test_binary, y_pred_proba_fake)
        brier = brier_score_loss(y_test_binary, y_pred_proba_fake)

    print("=" * 50)
    print(f"TEST ACCURACY: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"F1-Macro: {f1_macro:.4f}")
    print(f"F1-Weighted: {f1_weighted:.4f}")
    if auroc is not None:
        print(f"AUROC: {auroc:.4f}")
        print(f"Brier Score: {brier:.4f}")
    print("=" * 50)
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(cm)

    if accuracy < min_accuracy:
        raise RuntimeError(
            f"Accuracy {accuracy:.4f} is below required {min_accuracy:.2f}. Retrain/tune required."
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    model_path = out_dir / "fake_news_model.pkl"
    vectorizer_path = out_dir / "tfidf_vectorizer.pkl"
    report_path = out_dir / "training_report.txt"
    sample_path = out_dir / "sample_predictions.csv"

    with model_path.open("wb") as model_file:
        pickle.dump(model, model_file)
    with vectorizer_path.open("wb") as vectorizer_file:
        pickle.dump(tfidf, vectorizer_file)

    _verify_artifact_size(model_path, strict_size_check)
    _verify_artifact_size(vectorizer_path, strict_size_check)

    with report_path.open("w", encoding="utf-8") as report_file:
        report_file.write(f"Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)\n")
        report_file.write(f"F1-Macro: {f1_macro:.4f}\n")
        report_file.write(f"F1-Weighted: {f1_weighted:.4f}\n")
        if auroc is not None:
            report_file.write(f"AUROC: {auroc:.4f}\n")
            report_file.write(f"Brier Score: {brier:.4f}\n")
        report_file.write("\nClassification Report:\n")
        report_file.write(str(report))
        report_file.write("\nConfusion Matrix:\n")
        report_file.write(str(cm))
        report_file.write("\n")

    sample_df = pd.DataFrame(
        {
            "text": x_test.iloc[:10].values,
            "actual": y_test.iloc[:10].values,
            "predicted": y_pred[:10],
        }
    )
    sample_df.to_csv(sample_path, index=False)

    test_article = "Breaking: Shocking truth about government conspiracy exposed!"
    test_clean = clean_text(test_article)
    test_vec = tfidf.transform([test_clean])
    test_pred = model.predict(test_vec)[0]
    model_any: Any = model
    if hasattr(model_any, "decision_function"):
        test_conf = float(abs(model_any.decision_function(test_vec)[0]))
    else:
        test_conf = float(max(model_any.predict_proba(test_vec)[0]))

    print("Verification test:")
    print(f"Prediction: {test_pred}")
    print(f"Confidence score: {test_conf:.4f}")

    print("Saved files:")
    print(f"- {model_path}")
    print(f"- {vectorizer_path}")
    print(f"- {report_path}")
    print(f"- {sample_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train fake news detection model.")
    parser.add_argument("--fake", type=Path, help="Path to Fake.csv")
    parser.add_argument("--real", type=Path, help="Path to True.csv")
    parser.add_argument(
        "--liar-dir",
        type=Path,
        help="Path to LIAR dataset directory containing train.tsv, valid.tsv, test.tsv.",
    )
    parser.add_argument(
        "--liar-half-true-to",
        default="REAL",
        choices=["REAL", "FAKE"],
        help="Binary mapping target for LIAR 'half-true' label.",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        help="Backup single CSV path with text,label columns.",
    )
    parser.add_argument(
        "--model",
        default="passive-aggressive",
        choices=["passive-aggressive", "logistic"],
        help="Model choice.",
    )
    parser.add_argument(
        "--out",
        default=Path("backend/models"),
        type=Path,
        help="Output directory for artifacts.",
    )
    parser.add_argument(
        "--strict-size-check",
        action="store_true",
        help="Fail training if artifact files are smaller than 1MB.",
    )
    parser.add_argument(
        "--min-accuracy",
        default=MIN_ACCURACY,
        type=float,
        help="Minimum required test accuracy before artifacts are accepted.",
    )
    args = parser.parse_args()

    train(
        out_dir=args.out,
        model_name=args.model,
        strict_size_check=args.strict_size_check,
        min_accuracy=args.min_accuracy,
        liar_dir=args.liar_dir,
        liar_half_true_to=args.liar_half_true_to,
        fake_csv=args.fake,
        real_csv=args.real,
        dataset_csv=args.dataset,
    )
