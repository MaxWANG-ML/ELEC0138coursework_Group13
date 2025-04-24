import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

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
    # If the files have no header, use 'names' to manually specify column names
    # sep=None and engine='python' allow automatic delimiter detection (spaces, commas, tabs, etc.)
    df_dga = pd.read_csv(dga_file, sep=None, engine='python', names=["domain", "label"])
    df_legit = pd.read_csv(legit_file, sep=None, engine='python', names=["domain", "label"])

    # Convert labels to integers (ensure dga.txt = 1, legit.txt = 0)
    df_dga["label"] = df_dga["label"].astype(int)
    df_legit["label"] = df_legit["label"].astype(int)

    # Merge the two datasets and reset index
    df = pd.concat([df_dga, df_legit], ignore_index=True)
    return df


if __name__ == "__main__":
    # Replace the following two file paths with your actual dataset paths
    dga_file = "./database/dga.txt"
    legit_file = "./database/legit.txt"

    # Load data
    df = load_domains(dga_file, legit_file)
    print(f"Loaded {len(df)} domains")

    stat_features = df["domain"].apply(extract_stat_features).tolist()
    stat_features = np.array(stat_features)
    # Convert statistical features to DataFrame and add column names
    stat_df = pd.DataFrame(stat_features, columns=["length", "entropy", "unique_chars", "vowel_ratio"])
    # Add label column for plotting and comparison
    stat_df["label"] = df["label"].values
    stat_df['label'] = stat_df['label'].apply(lambda x: 1 if x != 0 else 0)
    # Save the DataFrame to CSV
    stat_df.to_csv("stat_features.csv", index=False, encoding="utf-8")
