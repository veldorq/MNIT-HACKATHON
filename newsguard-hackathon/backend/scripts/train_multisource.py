import argparse
import pickle
import random
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

RANDOM_STATE = 42
DEFAULT_MIN_ACCURACY = 0.85

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


def map_binary_label(value: str, half_true_to: str = "REAL") -> str:
    label = str(value).strip().lower()
    if label in {"real", "true", "mostly-true", "mostly true"}:
        return "REAL"
    if label in {"fake", "false", "pants-fire", "pants on fire", "barely-true", "barely true"}:
        return "FAKE"
    if label in {"half-true", "half true"}:
        return half_true_to
    return "UNKNOWN"


def load_kaggle(fake_csv: Path, real_csv: Path) -> pd.DataFrame:
    fake_df = pd.read_csv(fake_csv)
    fake_df = pd.DataFrame({"text": fake_df["text"], "label": "FAKE", "source": "kaggle"})

    real_df = pd.read_csv(real_csv)
    real_df = pd.DataFrame({"text": real_df["text"], "label": "REAL", "source": "kaggle"})

    return pd.concat([fake_df, real_df], ignore_index=True)


def load_liar(liar_dir: Path, half_true_to: str) -> pd.DataFrame:
    parts: list[pd.DataFrame] = []
    for split in ["train.tsv", "valid.tsv", "test.tsv"]:
        split_path = liar_dir / split
        if not split_path.exists():
            raise FileNotFoundError(f"Missing LIAR split file: {split_path}")

        df = pd.read_csv(split_path, sep="\t", header=None, names=LIAR_COLUMNS)
        part = pd.DataFrame(
            {
                "text": df["statement"],
                "label": df["label"].apply(lambda x: map_binary_label(x, half_true_to)),
                "source": "liar",
            }
        )
        parts.append(part)

    out = pd.concat(parts, ignore_index=True)
    return out[out["label"].isin(["REAL", "FAKE"])]


def load_generic_dataset(dataset_path: Path, text_col: str, label_col: str, half_true_to: str) -> pd.DataFrame:
    if dataset_path.suffix.lower() == ".tsv":
        df = pd.read_csv(dataset_path, sep="\t")
    else:
        df = pd.read_csv(dataset_path)

    if text_col not in df.columns or label_col not in df.columns:
        raise ValueError(
            f"Dataset {dataset_path.name} must contain columns '{text_col}' and '{label_col}'."
        )

    return pd.DataFrame(
        {
            "text": df[text_col],
            "label": df[label_col].apply(lambda x: map_binary_label(x, half_true_to)),
            "source": dataset_path.stem,
        }
    )


def load_fakenewsnet(fakenewsnet_dir: Path, text_col: str) -> pd.DataFrame:
    required_files = [
        ("politifact_real.csv", "REAL", "fakenewsnet_politifact"),
        ("politifact_fake.csv", "FAKE", "fakenewsnet_politifact"),
        ("gossipcop_real.csv", "REAL", "fakenewsnet_gossipcop"),
        ("gossipcop_fake.csv", "FAKE", "fakenewsnet_gossipcop"),
    ]

    frames: list[pd.DataFrame] = []
    for filename, label, source_name in required_files:
        file_path = fakenewsnet_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Missing FakeNewsNet file: {file_path}")

        df = pd.read_csv(file_path)
        if text_col not in df.columns:
            raise ValueError(
                f"FakeNewsNet file {filename} is missing text column '{text_col}'."
            )

        out = pd.DataFrame(
            {
                "text": df[text_col],
                "label": label,
                "source": source_name,
            }
        )
        frames.append(out)

    return pd.concat(frames, ignore_index=True)


def make_model(model_name: str):
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
            max_iter=250,
            random_state=RANDOM_STATE,
        )
    raise ValueError("Unsupported model. Choose passive-aggressive or logistic")


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["text_hash"] = df["clean_text"].str.slice(0, 500)
    deduped = df.drop_duplicates(subset=["text_hash", "label"]).drop(columns=["text_hash"])
    return deduped


def balance_classes(df: pd.DataFrame) -> pd.DataFrame:
    class_counts = df["label"].value_counts()
    if len(class_counts) < 2:
        raise RuntimeError("Need both REAL and FAKE classes after preprocessing.")

    min_count = int(class_counts.min())
    parts = []
    for label in ["REAL", "FAKE"]:
        subset = df[df["label"] == label]
        subset = subset.sample(n=min_count, random_state=RANDOM_STATE)
        parts.append(subset)

    out = pd.concat(parts, ignore_index=True)
    return out.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)


def train(args: argparse.Namespace) -> None:
    random.seed(RANDOM_STATE)

    frames: list[pd.DataFrame] = []
    if args.kaggle_fake and args.kaggle_real:
        frames.append(load_kaggle(args.kaggle_fake, args.kaggle_real))

    if args.liar_dir:
        frames.append(load_liar(args.liar_dir, args.half_true_to))

    if args.fakenewsnet_dir:
        frames.append(load_fakenewsnet(args.fakenewsnet_dir, args.fakenewsnet_text_col))

    for extra in args.extra_dataset:
        frames.append(
            load_generic_dataset(
                dataset_path=extra,
                text_col=args.extra_text_col,
                label_col=args.extra_label_col,
                half_true_to=args.half_true_to,
            )
        )

    if not frames:
        raise ValueError("Provide at least one dataset source.")

    df = pd.concat(frames, ignore_index=True)
    print(f"Combined rows before clean: {len(df)}")
    print("Source counts:")
    print(df["source"].value_counts().to_string())

    df["text"] = df["text"].astype(str)
    df["clean_text"] = df["text"].apply(clean_text)
    df = df[df["clean_text"].str.len() > 0]
    df = df[df["label"].isin(["REAL", "FAKE"])]

    before_dedup = len(df)
    df = deduplicate(df)
    print(f"Rows after dedup: {len(df)} (removed {before_dedup - len(df)})")

    if args.balance:
        df = balance_classes(df)
        print("Class counts after balancing:")
        print(df["label"].value_counts().to_string())

    if args.max_samples > 0 and len(df) > args.max_samples:
        df = df.sample(n=args.max_samples, random_state=RANDOM_STATE)
        print(f"Rows after max_samples cap: {len(df)}")

    x_train, x_test, y_train, y_test = train_test_split(
        df["clean_text"],
        df["label"],
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=df["label"],
    )

    tfidf = TfidfVectorizer(
        max_features=7000,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.85,
        sublinear_tf=True,
    )
    x_train_vec = tfidf.fit_transform(x_train)
    x_test_vec = tfidf.transform(x_test)

    model = make_model(args.model)
    model.fit(x_train_vec, y_train)

    y_pred = model.predict(x_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    # Compute advanced metrics
    f1_macro = f1_score(y_test, y_pred, average="macro")
    f1_weighted = f1_score(y_test, y_pred, average="weighted")
    
    # For AUROC and Brier score
    y_pred_proba = None
    auroc = None
    brier = None
    if hasattr(model, "predict_proba"):
        y_pred_proba = model.predict_proba(x_test_vec)
        classes = model.classes_
        fake_idx = list(classes).index("FAKE") if "FAKE" in classes else 0
        y_pred_proba_fake = y_pred_proba[:, fake_idx]
        y_test_binary = (y_test == "FAKE").astype(int)
        auroc = roc_auc_score(y_test_binary, y_pred_proba_fake)
        brier = brier_score_loss(y_test_binary, y_pred_proba_fake)

    print("=" * 60)
    print(f"TEST ACCURACY: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"F1-Macro: {f1_macro:.4f}")
    print(f"F1-Weighted: {f1_weighted:.4f}")
    if auroc is not None:
        print(f"AUROC: {auroc:.4f}")
        print(f"Brier Score: {brier:.4f}")
    print("=" * 60)
    print(report)
    print(cm)

    if accuracy < args.min_accuracy:
        raise RuntimeError(
            f"Accuracy {accuracy:.4f} below threshold {args.min_accuracy:.2f}."
        )

    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    model_path = out / "fake_news_model.pkl"
    vec_path = out / "tfidf_vectorizer.pkl"
    report_path = out / "training_report.txt"
    sample_path = out / "sample_predictions.csv"

    with model_path.open("wb") as f:
        pickle.dump(model, f)
    with vec_path.open("wb") as f:
        pickle.dump(tfidf, f)

    with report_path.open("w", encoding="utf-8") as f:
        f.write(f"Accuracy: {accuracy:.4f}\n")
        f.write(f"F1-Macro: {f1_macro:.4f}\n")
        f.write(f"F1-Weighted: {f1_weighted:.4f}\n")
        if auroc is not None:
            f.write(f"AUROC: {auroc:.4f}\n")
            f.write(f"Brier Score: {brier:.4f}\n")
        f.write("\nClassification Report:\n")
        f.write(str(report))
        f.write("\nConfusion Matrix:\n")
        f.write(str(cm))
        f.write("\n\nSource counts after prep:\n")
        f.write(df["source"].value_counts().to_string())
        f.write("\n\nClass counts after prep:\n")
        f.write(df["label"].value_counts().to_string())

    preview = pd.DataFrame(
        {
            "text": x_test.iloc[:10].values,
            "actual": y_test.iloc[:10].values,
            "predicted": y_pred[:10],
        }
    )
    preview.to_csv(sample_path, index=False)

    model_any: Any = model
    test_article = "Breaking update reportedly reveals major conspiracy tied to officials"
    test_vec = tfidf.transform([clean_text(test_article)])
    test_pred = str(model.predict(test_vec)[0])
    if hasattr(model_any, "decision_function"):
        test_conf = float(abs(model_any.decision_function(test_vec)[0]))
    else:
        test_conf = float(max(model_any.predict_proba(test_vec)[0]))

    print("Verification test:")
    print(f"Prediction: {test_pred}")
    print(f"Confidence score: {test_conf:.4f}")
    print("Saved files:")
    print(f"- {model_path}")
    print(f"- {vec_path}")
    print(f"- {report_path}")
    print(f"- {sample_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train one model from multiple datasets.")
    parser.add_argument("--kaggle-fake", type=Path, help="Path to Fake.csv")
    parser.add_argument("--kaggle-real", type=Path, help="Path to True.csv")
    parser.add_argument("--liar-dir", type=Path, help="Path containing LIAR train/valid/test TSV files")
    parser.add_argument(
        "--fakenewsnet-dir",
        type=Path,
        help="Path containing FakeNewsNet CSV files (politifact/gossipcop fake/real).",
    )
    parser.add_argument(
        "--fakenewsnet-text-col",
        default="title",
        help="Text column to use from FakeNewsNet files (default: title).",
    )
    parser.add_argument(
        "--extra-dataset",
        type=Path,
        action="append",
        default=[],
        help="Additional dataset path(s). Repeat flag to include multiple files.",
    )
    parser.add_argument("--extra-text-col", default="text", help="Text column for extra datasets")
    parser.add_argument("--extra-label-col", default="label", help="Label column for extra datasets")
    parser.add_argument("--half-true-to", default="REAL", choices=["REAL", "FAKE"])
    parser.add_argument("--model", default="logistic", choices=["logistic", "passive-aggressive"])
    parser.add_argument("--balance", action="store_true", help="Balance REAL/FAKE class counts")
    parser.add_argument("--max-samples", type=int, default=0, help="Optional cap for training rows (0 means no cap)")
    parser.add_argument("--min-accuracy", type=float, default=DEFAULT_MIN_ACCURACY)
    parser.add_argument("--out", type=Path, default=Path("backend/models/multi"))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train(args)
