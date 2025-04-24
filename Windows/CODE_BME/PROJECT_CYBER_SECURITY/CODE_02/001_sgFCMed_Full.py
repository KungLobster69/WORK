# ===============================================
# SG-FCMedians with Resume + Parallel + Purity/NMI/ARI Evaluation
# ===============================================

import numpy as np
import pandas as pd
import random
import os
import json
from collections import Counter
from rapidfuzz.distance import Levenshtein
from joblib import Parallel, delayed, parallel_backend
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score

# --------------------------------
# Parameters
# --------------------------------
path = r"C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT_01\01.TRAIN_TEST_SET"
path_save = r"C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT_02\01.PROTOTYPE"
os.makedirs(path_save, exist_ok=True)

c_benign = [100, 200, 300, 400, 500]
c_malware = [1000, 2000, 3000, 4000, 5000]
m_values = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

# --------------------------------
# Load Datasets
# --------------------------------
benign_df = pd.read_json(os.path.join(path, "benign_train.json"), lines=True)
malware_df = pd.read_json(os.path.join(path, "malware_train.json"), lines=True)
benign_strings = benign_df.iloc[:, 0].astype(str).tolist()
malware_strings = malware_df.iloc[:, 0].astype(str).tolist()

# --------------------------------
# SG-FCMedians Core Functions
# --------------------------------
def compute_distance_matrix(strings):
    n = len(strings)
    def row(i):
        return [Levenshtein.distance(strings[i], strings[j]) for j in range(n)]
    return np.array(Parallel(n_jobs=-1)(delayed(row)(i) for i in range(n)))

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

def improved_fuzzy_median_string(current_string, strings, memberships, alphabet, max_iter=5):
    s = current_string
    for _ in range(max_iter):
        candidates = generate_edit_candidates(s, alphabet)
        candidates.add(s)
        best_candidate = s
        best_score = sum(m * Levenshtein.distance(s, s_i) for m, s_i in zip(memberships, strings))
        for candidate in candidates:
            score = sum(m * Levenshtein.distance(candidate, s_i) for m, s_i in zip(memberships, strings))
            if score < best_score:
                best_candidate = candidate
                best_score = score
        if best_candidate == s:
            break
        s = best_candidate
    return s

def update_membership(D, prototypes, m):
    n, c = D.shape[0], len(prototypes)
    U = np.zeros((n, c))
    for i in range(n):
        for j in range(c):
            d_ij = D[i, prototypes[j]] + 1e-6
            denom = sum((d_ij / (D[i, prototypes[k]] + 1e-6)) ** (2 / (m - 1)) for k in range(c))
            U[i, j] = 1 / denom
    return U

# --------------------------------
# Evaluation: Purity / NMI / ARI
# --------------------------------
def assign_clusters(strings, prototypes):
    labels = []
    for s in strings:
        distances = [Levenshtein.distance(s, p) for p in prototypes]
        cluster = np.argmin(distances)
        labels.append(cluster)
    return labels

def calculate_purity(true_labels, pred_labels):
    contingency_matrix = {}
    for t, p in zip(true_labels, pred_labels):
        if p not in contingency_matrix:
            contingency_matrix[p] = []
        contingency_matrix[p].append(t)
    
    majority_sum = sum(Counter(v).most_common(1)[0][1] for v in contingency_matrix.values())
    return majority_sum / len(true_labels)

def evaluate_clustering_quality(strings, prototypes, true_labels, save_path):
    pred_labels = assign_clusters(strings, prototypes)
    purity = calculate_purity(true_labels, pred_labels)
    nmi = normalized_mutual_info_score(true_labels, pred_labels)
    ari = adjusted_rand_score(true_labels, pred_labels)
    
    quality = {
        'purity': purity,
        'nmi': nmi,
        'ari': ari
    }

    quality_path = save_path.replace('.csv', '_quality.json')
    with open(quality_path, 'w') as f:
        json.dump(quality, f, indent=4)

    print(f"📊 Saved: Purity={purity:.4f}, NMI={nmi:.4f}, ARI={ari:.4f} → {quality_path}")

# --------------------------------
# Resume-safe Prototype Save
# --------------------------------
def safe_append_prototype(prototype, filepath):
    mode = 'a' if os.path.exists(filepath) else 'w'
    header = not os.path.exists(filepath)
    pd.DataFrame({'prototype': [prototype]}).to_csv(filepath, mode=mode, header=header, index=False)

def get_existing_prototypes(filepath):
    if not os.path.exists(filepath):
        return 0
    try:
        return pd.read_csv(filepath).shape[0]
    except Exception:
        return 0

# --------------------------------
# Main SG-FCMedians (Parallel per prototype)
# --------------------------------
def compute_single_prototype(j, D, strings, prototypes_idx, m, alphabet):
    memberships = update_membership(D, prototypes_idx, m)[:, j]
    proto_init = strings[prototypes_idx[j]]
    new_proto = improved_fuzzy_median_string(proto_init, strings, memberships, alphabet)
    return j, new_proto

def sgfcmed_resume_by_prototype_parallel(strings, c, m, save_path, label, max_iter=10):
    D = compute_distance_matrix(strings)
    indices = list(range(len(strings)))
    random.shuffle(indices)
    prototypes_idx = indices[:c]
    alphabet = set(''.join(strings))

    existing_count = get_existing_prototypes(save_path)
    indices_to_process = list(range(existing_count, c))

    if not indices_to_process:
        print(f"✅ Already completed: {save_path}")
    else:
        print(f"🚀 Computing {len(indices_to_process)} prototypes in parallel...")

        with parallel_backend('loky'):
            results = Parallel(n_jobs=-1)(
                delayed(compute_single_prototype)(j, D, strings, prototypes_idx, m, alphabet)
                for j in indices_to_process
            )

        for j, proto in sorted(results):
            safe_append_prototype(proto, save_path)
            print(f"✅ Saved prototype {j+1} to {save_path}")

    # Evaluate quality
    df = pd.read_csv(save_path)
    prototypes = df['prototype'].tolist()
    true_labels = [0 if label == "benign" else 1] * len(strings)
    evaluate_clustering_quality(strings, prototypes, true_labels, save_path)

# --------------------------------
# Run All Configs
# --------------------------------
for label, strings, c_values in [('benign', benign_strings, c_benign), ('malware', malware_strings, c_malware)]:
    for c in c_values:
        for m in m_values:
            filename = f"{label}_c{c}_m{str(m).replace('.', '_')}.csv"
            save_path = os.path.join(path_save, filename)
            sgfcmed_resume_by_prototype_parallel(strings.copy(), c=c, m=m, save_path=save_path, label=label, max_iter=10)