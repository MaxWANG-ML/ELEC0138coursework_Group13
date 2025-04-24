import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

df_file = "./database/stat_features.csv"

df = pd.read_csv(df_file)

# 3. Split the data: malicious domains vs. legitimate domains
df_malicious = df[df['label'] == 1]
df_legit = df[df['label'] == 0]

# Plot comparison histograms for each statistical feature
features = ["length", "entropy", "unique_chars", "vowel_ratio"]

# 5. Plot comparison histogram for each feature
for feature in features:
    plt.figure(figsize=(8, 6))
    plt.hist(df_malicious[feature], bins=30, alpha=0.5, label="malicious", color="red")
    plt.hist(df_legit[feature], bins=30, alpha=0.5, label="legitimate", color="blue")
    plt.xlabel(feature)
    plt.ylabel("count")
    plt.title(f"comparison of malicious DNS and legitimate DNS on feature {feature} ")
    plt.legend()
    plt.savefig(f"comparison of malicious DNS and legitimate DNS on feature {feature} ")
plt.show()
