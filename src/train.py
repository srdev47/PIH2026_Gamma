import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

DATA_PATH = "data/fake_job_postings.csv"
MODEL_PATH = "models/model.joblib"

def build_text(df: pd.DataFrame) -> pd.Series:
    cols = ["title", "company_profile", "description", "requirements", "benefits"]
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return (
        df["title"].fillna("") + "\n" +
        df["company_profile"].fillna("") + "\n" +
        df["description"].fillna("") + "\n" +
        df["requirements"].fillna("") + "\n" +
        df["benefits"].fillna("")
    )

def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    if "fraudulent" not in df.columns:
        raise ValueError("CSV must contain a 'fraudulent' column (0=real, 1=fake).")

    X = build_text(df)
    y = df["fraudulent"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            max_features=60000,
            ngram_range=(1, 2),
            min_df=2
        )),
        ("clf", LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        ))
    ])

    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    print("\nConfusion matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification report:\n", classification_report(y_test, y_pred, digits=4))

    os.makedirs("models", exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)
    print(f"\nSaved model to {MODEL_PATH}")

if __name__ == "__main__":
    main()