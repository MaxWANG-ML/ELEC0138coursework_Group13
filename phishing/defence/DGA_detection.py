import numpy as np
import pandas as pd
import math
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from scipy.sparse import hstack
def compute_entropy(s):
    if not s:
        return 0
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    entropy = 0.0
    length = len(s)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy


def compute_vowel_ratio(s):
    vowels = set("aeiou")
    if not s:
        return 0
    count = sum(1 for ch in s.lower() if ch in vowels)
    return count / len(s)


def extract_stat_features(domain):
    domain = domain.strip().lower()
    length = len(domain)
    entropy = compute_entropy(domain)
    unique_chars = len(set(domain))
    vowel_ratio = compute_vowel_ratio(domain)
    return [length, entropy, unique_chars, vowel_ratio]


def load_domains(dga_file, legit_file):
    # If files don't have headers, use 'names' to assign column names
    # sep=None with engine='python' helps auto-detect delimiters (space, comma, tab, etc.)
    df_dga = pd.read_csv(dga_file, sep=None, engine='python', names=["domain", "label"])
    df_legit = pd.read_csv(legit_file, sep=None, engine='python', names=["domain", "label"])

    # Convert labels to int (ensure dga.txt labels are 1, legit.txt labels are 0)
    df_dga["label"] = df_dga["label"].astype(int)
    df_legit["label"] = df_legit["label"].astype(int)

    # Merge the two datasets and reset index
    df = pd.concat([df_dga, df_legit], ignore_index=True)
    df['label'] = df['label'].apply(lambda x: 1 if x != 0 else 0)
    return df, df_dga, df_legit


def build_features(df, features):
    # Statistical features
    features = np.array(features)
    features = features[:, :-1]

    # N-Gram features (using character 2-gram to 4-gram)
    tfidf_vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))
    tfidf_features = tfidf_vectorizer.fit_transform(df["domain"])

    # Save TfidfVectorizer to file
    joblib.dump(tfidf_vectorizer, "tfidf_vectorizer.pkl")
    print("TfidfVectorizer saved to tfidf_vectorizer.pkl")

    # Combine the two types of features (convert stat_features to sparse matrix before combining)
    from scipy.sparse import csr_matrix
    stat_features_sparse = csr_matrix(features)
    combined_features = hstack([tfidf_features, stat_features_sparse])
    return combined_features, tfidf_vectorizer


def train_dga_model(df, features):
    X = features
    y = df["label"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Use logistic regression as the classifier
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)

    # Save model to file
    joblib.dump(clf, "dga_model.pkl")
    print("Model saved to dga_model.pkl")

    y_pred = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    return clf


if __name__ == "__main__":
    # Replace these with the actual paths to your datasets
    dga_file = "./database/dga.txt"
    legit_file = "./database/legit.txt"
    feature_file = "./database/stat_features.csv"

    features_class1 = pd.read_csv(feature_file)
    # Load data
    df, df_dga, df_legit = load_domains(dga_file, legit_file)
    # print(f"Loaded {len(df)} domains in total, DGA: {sum(df_dga)}, Legit: {sum(df_legit)}")

    # Build features
    features, tfidf_vectorizer = build_features(df, features_class1)

    # Train model
    model = train_dga_model(df, features)
