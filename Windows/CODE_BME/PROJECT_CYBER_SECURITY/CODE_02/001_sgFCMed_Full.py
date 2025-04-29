import numpy as np
import pandas as pd
import random
import os
import json
from collections import Counter
from Levenshtein import distance as lev_distance
from joblib import Parallel, delayed
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score
from tqdm import tqdm

# --------------------------------
# Parameters
# --------------------------------
path = r"C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT_01\01.TRAIN_TEST_SET"
path_save = r"C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT_02\01.PROTOTYPE"
os.makedirs(path_save, exist_ok=True)

c_benign = [100, 200, 300, 400, 500]
c_malware = [1000, 2000, 3000, 4000, 5000]
m_values = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

batch_size = 500
candidate_batch_size = 5000
num_cores = max(1, os.cpu_count() - 2)

# --------------------------------
# Load JSON
# --------------------------------
def load_json_lines(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return pd.DataFrame(data)

# --------------------------------
# Helper Functions
# --------------------------------
def pair_distance(i, j, strings_ref, prototypes_ref):
    return (i, j, lev_distance(strings_ref[i], prototypes_ref[j]))

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

def compute_weighted_distance(candidate, strings, memberships):
    return sum(m * lev_distance(candidate, x) for m, x in zip(memberships, strings))

def improved_fuzzy_median_string(current_string, strings, memberships, alphabet, max_local_iter=5):
    s = current_string
    for it in range(max_local_iter):
        candidates = generate_edit_candidates(s, alphabet)
        candidates.add(s)
        candidates = list(candidates)

        best = s
        best_score = sum(m * lev_distance(s, x) for m, x in zip(memberships, strings))

        batches = [candidates[i:i+candidate_batch_size] for i in range(0, len(candidates), candidate_batch_size)]
        for batch in batches:
            scores = Parallel(n_jobs=num_cores, prefer="processes", backend="loky")(
                delayed(compute_weighted_distance)(cand, strings, memberships)
                for cand in batch
            )
            min_idx = np.argmin(scores)
            if scores[min_idx] < best_score:
                best = batch[min_idx]
                best_score = scores[min_idx]

        if best == s:
            break
        s = best
    return s

# --------------------------------
# Distance Matrix
# --------------------------------
def compute_distance_matrix_to_prototypes(strings, prototypes, batch_size=None, temp_save_path=None):
    n, c = len(strings), len(prototypes)
    if batch_size is None:
        batch_size = 500
    print(f"📏 Computing Distance Matrix: strings={n} × prototypes={c} (batch size={batch_size})")
    D = np.zeros((n, c), dtype=np.int32)

    pairs = [(i, j) for i in range(n) for j in range(c)]
    batches = [pairs[k:k+batch_size] for k in range(0, len(pairs), batch_size)]
    save_every_batches = max(1, len(batches) // 100)

    strings_ref = strings
    prototypes_ref = prototypes

    for batch_num, batch_pairs in enumerate(tqdm(batches, desc="🔧 Distance Matrix (Batched)")):
        results = Parallel(n_jobs=num_cores, prefer="processes", backend="loky")(
            delayed(pair_distance)(i, j, strings_ref, prototypes_ref) for i, j in batch_pairs
        )
        for i, j, d in results:
            D[i, j] = d

        if temp_save_path and ((batch_num + 1) % save_every_batches == 0 or (batch_num + 1) == len(batches)):
            np.save(temp_save_path.replace(".csv", "_distmatrix.npy"), D)
            print(f"💾 Distance Matrix checkpoint saved at {batch_num+1}/{len(batches)} batches")
    
    return D

# --------------------------------
# Update Membership
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
    return np.array(Parallel(n_jobs=num_cores, backend="loky")(
        delayed(compute_row)(i) for i in range(n)
    ))

# --------------------------------
# Assign Clusters
# --------------------------------
def assign_clusters(strings, prototypes):
    def nearest(s):
        dists = [lev_distance(s, p) for p in prototypes]
        return np.argmin(dists)
    return Parallel(n_jobs=num_cores, backend="loky")(
        delayed(nearest)(s) for s in strings
    )

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
# Main SG-FCMedians with full Checkpoint
# --------------------------------
def sgfcmed_iterative_fast(strings, c, m, save_path, label, max_iter=5):
    temp_save_path = save_path.replace(".csv", "_temp.csv")
    idx_save_path = save_path.replace(".csv", "_temp_idx.json")
    iter_save_path = save_path.replace(".csv", "_temp_iter.json")
    distmatrix_save_path = save_path.replace(".csv", "_distmatrix.npy")

    if os.path.exists(idx_save_path) and os.path.exists(iter_save_path):
        print("🔄 Resuming previous run ...")
        with open(idx_save_path, 'r') as f:
            prototypes_idx = json.load(f)
        with open(iter_save_path, 'r') as f:
            iter_info = json.load(f)
        start_iter = iter_info['current_iter']
    else:
        indices = list(range(len(strings)))
        random.shuffle(indices)
        prototypes_idx = indices[:c]
        start_iter = 0
        with open(idx_save_path, 'w') as f:
            json.dump(prototypes_idx, f)
        with open(iter_save_path, 'w') as f:
            json.dump({'current_iter': start_iter}, f)

    alphabet = set(''.join(strings))

    for it in range(start_iter, max_iter):
        print(f"🔁 Iteration {it+1}/{max_iter}")

        prototype_strings = [strings[i] for i in prototypes_idx]

        if os.path.exists(distmatrix_save_path):
            print("📥 Loading existing distance matrix ...")
            D = np.load(distmatrix_save_path)
        else:
            D = compute_distance_matrix_to_prototypes(
                strings, prototype_strings, batch_size=batch_size, temp_save_path=temp_save_path
            )
        
        U = update_membership(D, m)

        new_prototypes = [None] * c
        completed = set()

        if os.path.exists(temp_save_path):
            df_temp = pd.read_csv(temp_save_path)
            for idx, row in df_temp.iterrows():
                if pd.notnull(row['prototype']):
                    new_prototypes[idx] = row['prototype']
                    completed.add(idx)
            print(f"🔄 Resuming prototypes {len(completed)}/{c}")

        for j in tqdm(range(c), desc=f"🧬 Updating Prototypes (Iter {it+1})"):
            if j in completed:
                continue

            proto = improved_fuzzy_median_string(strings[prototypes_idx[j]], strings, U[:, j], alphabet)
            new_prototypes[j] = proto

            if (j+1) % max(1, c // 100) == 0 or (j+1) == c:
                temp_df = pd.DataFrame({'prototype': new_prototypes})
                temp_df.to_csv(temp_save_path, index=False)
                print(f"💾 Prototype checkpoint saved at {j+1}/{c}")

        prototypes_idx = []
        for p in new_prototypes:
            dists = [lev_distance(p, s) for s in strings]
            prototypes_idx.append(np.argmin(dists))

        with open(idx_save_path, 'w') as f:
            json.dump(prototypes_idx, f)
        with open(iter_save_path, 'w') as f:
            json.dump({'current_iter': it+1}, f)

        if os.path.exists(distmatrix_save_path):
            os.remove(distmatrix_save_path)

    final_prototypes = [strings[i] for i in prototypes_idx]
    pd.DataFrame({'prototype': final_prototypes}).to_csv(save_path, index=False)

    true_labels = [0 if label == 'benign' else 1] * len(strings)
    evaluate_clustering_quality(strings, final_prototypes, true_labels, save_path)

    for fpath in [temp_save_path, idx_save_path, iter_save_path, distmatrix_save_path]:
        if os.path.exists(fpath):
            os.remove(fpath)
    print(f"🏁 Done: saved to {save_path}")

# --------------------------------
# Run
# --------------------------------
if __name__ == "__main__":
    print("📥 Loading benign dataset ...")
    benign_df = load_json_lines(os.path.join(path, "benign_train.json"))
    benign_strings = benign_df.iloc[:, 0].astype(str).tolist()

    for c in c_benign:
        for m in m_values:
            filename = f"benign_c{c}_m{str(m).replace('.', '_')}.csv"
            save_path = os.path.join(path_save, filename)
            sgfcmed_iterative_fast(benign_strings.copy(), c, m, save_path, label="benign")

    del benign_df
    del benign_strings

    print("📥 Loading malware dataset ...")
    malware_df = load_json_lines(os.path.join(path, "malware_train.json"))
    malware_strings = malware_df.iloc[:, 0].astype(str).tolist()

    for c in c_malware:
        for m in m_values:
            filename = f"malware_c{c}_m{str(m).replace('.', '_')}.csv"
            save_path = os.path.join(path_save, filename)
            sgfcmed_iterative_fast(malware_strings.copy(), c, m, save_path, label="malware")

    del malware_df
    del malware_strings

    print("✅ All datasets processed successfully.")