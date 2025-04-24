import joblib
import numpy as np
import re
import math
from urllib.parse import urlparse
from scipy.sparse import csr_matrix, hstack

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


# Make sure the model and tfidf_vectorizer are saved during training
model = joblib.load("dga_model.pkl")
tfidf_vectorizer = joblib.load("tfidf_vectorizer.pkl")


def test_domain(domain):
    # Extract statistical features and convert to sparse matrix (single sample)
    stat_feats = extract_stat_features(domain)
    stat_feats = np.array(stat_feats).reshape(1, -1)
    stat_feats_sparse = csr_matrix(stat_feats)

    # Extract TF-IDF features (note that transform expects a list)
    tfidf_feats = tfidf_vectorizer.transform([domain])

    # Combine both types of features
    combined_features = hstack([tfidf_feats, stat_feats_sparse])

    # Use model to predict
    pred = model.predict(combined_features)
    return pred[0]

def DGA_detect(domain):
    result = test_domain(domain)
    return result

