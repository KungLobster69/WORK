import numpy as np
import pandas as pd
import random
import os
import json
from collections import Counter
from Levenshtein import distance as lev_distance
from joblib import Parallel, delayed, parallel_backend
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score
from tqdm import tqdm

# --------------------------------
# Parameters
# --------------------------------
path = r"C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT_01\01.TRAIN_TEST_SET"
path_save = r"C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT_02\01.PROTOTYPE"
os.makedirs(path_save, exist_ok=True)

c_benign = [100]
c_malware = [100]
m_values = [2.0]

# --------------------------------
# Load Datasets
# --------------------------------
print("📥 Loading JSON datasets ...")
benign_df = pd.read_json(os.path.join(path, "benign_train.json"), lines=True)
malware_df = pd.read_json(os.path.join(path, "malware_train.json"), lines=True)
benign_strings = benign_df.iloc[:, 0].astype(str).tolist()
malware_strings = malware_df.iloc[:, 0].astype(str).tolist()

# --------------------------------
# Fast Distance Matrix (n x c only)
# --------------------------------
def compute_distance_matrix_to_prototypes(strings, prototypes):
    n, c = len(strings), len(prototypes)
    print(f"📏 Computing Distance Matrix: strings={n} × prototypes={c}")
    def pair(i, j):
        return (i, j, lev_distance(strings[i], prototypes[j]))
    pairs = [(i, j) for i in range(n) for j in range(c)]
    results = Parallel(n_jobs=-1, prefer="processes")(
        delayed(pair)(i, j) for i, j in tqdm(pairs, desc="🔧 Distance s↔p")
    )
    D = np.zeros((n, c), dtype=int)
    for i, j, d in results:
        D[i, j] = d
    return D

# --------------------------------
# Membership Matrix
# --------------------------------
def update_membership(D, m):
    n, c = D.shape
    def compute_row(i):
        u_i = []
        for j in range(c):
            d_ij = D[i, j] + 1e-6
            denom = sum((d_ij / (D[i, k] + 1e-6)) ** (2 / (m - 1)) for k in range(c))
            u_i.append(1 / denom)
        return u_i
    return np.array(Parallel(n_jobs=-1)(delayed(compute_row)(i) for i in range(n)))

# --------------------------------
# Fuzzy Median String
# --------------------------------
def generate_edit_candidates(s, alphabet):
    candidates = set()
    for i in range(len(s)):
        for a in alphabet:
            if s[i] != a:
                candidates.add(s[:i] + a + s[i+1:])
    for i in range(len(s) + 1):
        for a in alphabet:
            candidates.add(s[:i] + a + s[i:])
    for i in range(len(s)):
        candidates.add(s[:i] + s[i+1:])
    return candidates

def improved_fuzzy_median_string(current_string, strings, memberships, alphabet, max_local_iter=5):
    s = current_string
    for _ in range(max_local_iter):
        candidates = generate_edit_candidates(s, alphabet)
        candidates.add(s)
        best = s
        best_score = sum(m * lev_distance(s, x) for m, x in zip(memberships, strings))
        for c in candidates:
            score = sum(m * lev_distance(c, x) for m, x in zip(memberships, strings))
            if score < best_score:
                best, best_score = c, score
        if best == s:
            break
        s = best
    return s

# --------------------------------
# Evaluation
# --------------------------------
def assign_clusters(strings, prototypes):
    def nearest(s):
        dists = [lev_distance(s, p) for p in prototypes]
        return np.argmin(dists)
    return Parallel(n_jobs=-1)(delayed(nearest)(s) for s in strings)

def calculate_purity(true_labels, pred_labels):
    contingency = {}
    for t, p in zip(true_labels, pred_labels):
        contingency.setdefault(p, []).append(t)
    majority = sum(Counter(v).most_common(1)[0][1] for v in contingency.values())
    return majority / len(true_labels)

def evaluate_clustering_quality(strings, prototypes, true_labels, save_path):
    print("📊 Evaluating clustering quality ...")
    pred_labels = assign_clusters(strings, prototypes)
    purity = calculate_purity(true_labels, pred_labels)
    nmi = normalized_mutual_info_score(true_labels, pred_labels)
    ari = adjusted_rand_score(true_labels, pred_labels)
    metrics = {"purity": purity, "nmi": nmi, "ari": ari}
    with open(save_path.replace(".csv", "_quality.json"), "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"✅ Purity={purity:.4f}, NMI={nmi:.4f}, ARI={ari:.4f}")

# --------------------------------
# SG-FCMedians (Full Iterative, Fast)
# --------------------------------
def sgfcmed_iterative_fast(strings, c, m, save_path, label, max_iter=5):
    print(f"\n🚀 SG-FCMedians: label={label}, c={c}, m={m}")
    n = len(strings)
    indices = list(range(n))
    random.shuffle(indices)
    prototypes_idx = indices[:c]
    alphabet = set(''.join(strings))

    for it in range(max_iter):
        print(f"🔁 Iteration {it+1}/{max_iter}")
        prototype_strings = [strings[i] for i in prototypes_idx]
        D = compute_distance_matrix_to_prototypes(strings, prototype_strings)
        U = update_membership(D, m)

        with parallel_backend("loky"):
            new_prototypes = Parallel(n_jobs=-1)(
                delayed(improved_fuzzy_median_string)(
                    strings[prototypes_idx[j]], strings, U[:, j], alphabet
                ) for j in tqdm(range(c), desc=f"🧬 Updating Prototypes")
            )

        # Remap fuzzy strings back to closest actual string
        prototypes_idx = []
        for p in new_prototypes:
            dists = [lev_distance(p, s) for s in strings]
            prototypes_idx.append(np.argmin(dists))

    final_prototypes = [strings[i] for i in prototypes_idx]
    pd.DataFrame({'prototype': final_prototypes}).to_csv(save_path, index=False)
    true_labels = [0 if label == 'benign' else 1] * len(strings)
    evaluate_clustering_quality(strings, final_prototypes, true_labels, save_path)
    print(f"🏁 Done: saved to {save_path}")

# --------------------------------
# Run All Configs
# --------------------------------
for label, str_list, c_values in [("benign", benign_strings, c_benign), ("malware", malware_strings, c_malware)]:
    for c in c_values:
        for m in m_values:
            filename = f"{label}_c{c}_m{str(m).replace('.', '_')}.csv"
            save_path = os.path.join(path_save, filename)
            sgfcmed_iterative_fast(str_list.copy(), c, m, save_path, label)
