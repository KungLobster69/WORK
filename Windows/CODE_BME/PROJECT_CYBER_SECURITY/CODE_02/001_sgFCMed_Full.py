# --------------------------
# IMPORTS
# --------------------------
import numpy as np
import pandas as pd
import random
import os
import json
import matplotlib.pyplot as plt
from collections import Counter
from Levenshtein import distance as lev_distance
from joblib import Parallel, delayed
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score
from tqdm import tqdm

# --------------------------
# PARAMETERS
# --------------------------
path = r"C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT_01\01.TRAIN_TEST_SET"
path_save = r"C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT_02\01.PROTOTYPE"
os.makedirs(path_save, exist_ok=True)

c_candidates = [100, 200, 300, 400, 500]          # candidate c values
m_candidates = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0] # candidate m values

batch_size = 500
candidate_batch_size = 5000
num_cores = max(1, os.cpu_count() - 2)

# --------------------------
# JSON Loader
# --------------------------
def load_json_lines(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return pd.DataFrame(data)

# --------------------------
# HELPER FUNCTIONS
# --------------------------

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
    for _ in range(max_local_iter):
        candidates = generate_edit_candidates(s, alphabet)
        candidates.add(s)
        candidates = list(candidates)

        best = s
        best_score = sum(m * lev_distance(s, x) for m, x in zip(memberships, strings))

        batches = [candidates[i:i+candidate_batch_size] for i in range(0, len(candidates), candidate_batch_size)]
        for batch in batches:
            scores = Parallel(n_jobs=num_cores, backend="loky")(
                delayed(compute_weighted_distance)(cand, strings, memberships) for cand in batch
            )
            min_idx = np.argmin(scores)
            if scores[min_idx] < best_score:
                best = batch[min_idx]
                best_score = scores[min_idx]

        if best == s:
            break
        s = best
    return s

def compute_distance_matrix_to_prototypes(strings, prototypes, batch_size=None):
    n, c = len(strings), len(prototypes)
    if batch_size is None:
        batch_size = 500
    print(f"📏 Computing Distance Matrix: strings={n} × prototypes={c}")
    D = np.zeros((n, c), dtype=np.int32)

    pairs = [(i, j) for i in range(n) for j in range(c)]
    batches = [pairs[k:k+batch_size] for k in range(0, len(pairs), batch_size)]

    for batch_num, batch_pairs in enumerate(tqdm(batches, desc="🔧 Distance Matrix (Batched)")):
        results = Parallel(n_jobs=num_cores, backend="loky")(
            delayed(pair_distance)(i, j, strings, prototypes) for i, j in batch_pairs
        )
        for i, j, d in results:
            D[i, j] = d

    return D

def update_membership(D, m):
    n, c = D.shape
    def compute_row(i):
        u_i = []
        for j in range(c):
            d_ij = D[i, j] + 1e-6
            denom = sum((d_ij / (D[i, k] + 1e-6)) ** (1 / (m - 1)) for k in range(c))
            u_i.append(1 / denom)
        return u_i
    return np.array(Parallel(n_jobs=num_cores, backend="loky")(
        delayed(compute_row)(i) for i in range(n)
    ))

def compute_objective(D, U, m):
    return np.sum((U ** m) * D)

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

# --------------------------
# SGFCMedIterativeFast (Dynamic Adjust Tolerance)
# --------------------------
def sgfcmed_iterative_fast(strings, c, m, save_path, label, 
                           tolerance_percent=1.0, max_iter=50,
                           adjust_every=1, adjust_rate=0.9):
    temp_save_path = save_path.replace(".csv", "_temp.csv")
    idx_save_path = save_path.replace(".csv", "_temp_idx.json")
    iter_save_path = save_path.replace(".csv", "_temp_iter.json")

    J_values = []

    if os.path.exists(temp_save_path) and os.path.exists(idx_save_path) and os.path.exists(iter_save_path):
        print("🔄 Resuming from checkpoint...")
        df_temp = pd.read_csv(temp_save_path)
        with open(idx_save_path, 'r') as f:
            prototypes_idx = json.load(f)
        with open(iter_save_path, 'r') as f:
            start_iter = json.load(f)['current_iter']
        prototype_strings = df_temp['prototype'].tolist()
        if os.path.exists(save_path.replace(".csv", "_J_log.csv")):
            J_values = pd.read_csv(save_path.replace(".csv", "_J_log.csv"))["J"].tolist()
    else:
        indices = list(range(len(strings)))
        random.shuffle(indices)
        prototypes_idx = indices[:c]
        prototype_strings = [strings[i] for i in prototypes_idx]
        start_iter = 0
        pd.DataFrame({'prototype': prototype_strings}).to_csv(temp_save_path, index=False)
        with open(idx_save_path, 'w') as f:
            json.dump(prototypes_idx, f)
        with open(iter_save_path, 'w') as f:
            json.dump({'current_iter': start_iter}, f)

    alphabet = set(''.join(strings))
    tolerance = max(1, int(c * tolerance_percent / 100))
    print(f"⚙️ Initial tolerance = {tolerance} ({tolerance_percent}% of c={c})")

    for it in range(start_iter, max_iter):
        print(f"🔁 Iteration {it+1}/{max_iter} (Current tolerance = {tolerance})")

        D = compute_distance_matrix_to_prototypes(strings, prototype_strings, batch_size=batch_size)
        U = update_membership(D, m)
        J = compute_objective(D, U, m)
        J_values.append(J)

        pd.DataFrame({"iteration": list(range(1, len(J_values)+1)), "J": J_values}) \
            .to_csv(save_path.replace(".csv", "_J_log.csv"), index=False)
        print(f"📉 Objective J(U,P) = {J:.2f}")

        new_prototypes = []
        for j in tqdm(range(c), desc=f"🧬 Updating Prototypes (Iter {it+1})"):
            proto = improved_fuzzy_median_string(prototype_strings[j], strings, U[:, j], alphabet)
            dists = [lev_distance(proto, s) for s in strings]
            nearest_idx = np.argmin(dists)
            new_prototypes.append(strings[nearest_idx])

        changes = sum(1 for a, b in zip(prototype_strings, new_prototypes) if a != b)
        print(f"🔎 Prototype changes: {changes}")

        pd.DataFrame({'prototype': new_prototypes}).to_csv(temp_save_path, index=False)
        prototypes_idx = [strings.index(p) for p in new_prototypes]
        with open(idx_save_path, 'w') as f:
            json.dump(prototypes_idx, f)
        with open(iter_save_path, 'w') as f:
            json.dump({'current_iter': it+1}, f)

        prototype_strings = new_prototypes

        # 🔥 Dynamic Adjust Tolerance: ลดลงทุก adjust_every รอบ
        if (it + 1) % adjust_every == 0:
            tolerance = max(1, int(tolerance * adjust_rate))
            print(f"⚙️ Adjusted tolerance to {tolerance}")

        if changes <= tolerance:
            print(f"🛑 Stopping: prototypes converged (changes={changes} <= tolerance={tolerance}).")
            break

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(J_values)+1), J_values, marker='o')
    plt.title(f"Objective J(U,P) vs Iteration (label={label}, c={c}, m={m})")
    plt.xlabel("Iteration")
    plt.ylabel("Objective J(U,P)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path.replace(".csv", "_J_plot.png"))
    plt.close()

    final_prototypes = prototype_strings
    pd.DataFrame({'prototype': final_prototypes}).to_csv(save_path, index=False)

    true_labels = [0 if label == 'benign' else 1] * len(strings)
    evaluate_clustering_quality(strings, final_prototypes, true_labels, save_path)

    for f in [temp_save_path, idx_save_path, iter_save_path]:
        if os.path.exists(f):
            os.remove(f)
    print(f"🏁 Done: saved to {save_path}")

# --------------------------
# OPTIMIZER หา c และ m อัตโนมัติ
# --------------------------
def optimizer_c_m(strings, label, c_candidates, m_candidates, save_dir,
                  tolerance_percent=1.0, max_iter=50):
    results = []
    os.makedirs(save_dir, exist_ok=True)

    for c in c_candidates:
        for m in m_candidates:
            print(f"\n🚀 Trying c={c}, m={m} ...")
            filename = f"{label}_c{c}_m{str(m).replace('.', '_')}.csv"
            save_path = os.path.join(save_dir, filename)
            sgfcmed_iterative_fast(strings.copy(), c, m, save_path, label,
                                   tolerance_percent=tolerance_percent, max_iter=max_iter)

            # Load quality metrics
            with open(save_path.replace(".csv", "_quality.json"), 'r') as f:
                metrics = json.load(f)

            results.append({
                'c': c,
                'm': m,
                'purity': metrics['purity'],
                'nmi': metrics['nmi'],
                'ari': metrics['ari'],
                'path': save_path
            })

    # Save optimization results
    df_results = pd.DataFrame(results)
    df_results.to_csv(os.path.join(save_dir, f"{label}_optimization_summary.csv"), index=False)

    # Select best c, m
    df_sorted = df_results.sort_values(
        by=['purity', 'nmi', 'ari'],
        ascending=[False, False, False]
    ).reset_index(drop=True)

    best_c = df_sorted.loc[0, 'c']
    best_m = df_sorted.loc[0, 'm']

    print(f"\n🏆 Best configuration: c={best_c}, m={best_m}")
    return best_c, best_m

# --------------------------
# MAIN PROGRAM (เลือกใช้ Optimizer หรือ Manual)
# --------------------------
if __name__ == "__main__":
    mode = "optimizer"  # เปลี่ยนเป็น "manual" ถ้าอยากกำหนดเอง

    print("📥 Loading benign dataset ...")
    benign_df = load_json_lines(os.path.join(path, "benign_train.json"))
    benign_strings = benign_df.iloc[:, 0].astype(str).tolist()

    if mode == "optimizer":
        print("🔍 Running optimizer for benign dataset ...")
        optimizer_c_m(
            strings=benign_strings,
            label="benign",
            c_candidates=c_candidates,
            m_candidates=m_candidates,
            save_dir=path_save,
            tolerance_percent=20,
            max_iter=50
        )
    else:
        for c in c_candidates:
            for m in m_candidates:
                filename = f"benign_c{c}_m{str(m).replace('.', '_')}.csv"
                save_path = os.path.join(path_save, filename)
                sgfcmed_iterative_fast(benign_strings.copy(), c, m, save_path, label="benign",
                                       tolerance_percent=1.0, max_iter=50)

    del benign_df, benign_strings

    print("📥 Loading malware dataset ...")
    malware_df = load_json_lines(os.path.join(path, "malware_train.json"))
    malware_strings = malware_df.iloc[:, 0].astype(str).tolist()

    if mode == "optimizer":
        print("🔍 Running optimizer for malware dataset ...")
        optimizer_c_m(
            strings=malware_strings,
            label="malware",
            c_candidates=c_candidates,
            m_candidates=m_candidates,
            save_dir=path_save,
            tolerance_percent=20,
            max_iter=50
        )
    else:
        for c in c_candidates:
            for m in m_candidates:
                filename = f"malware_c{c}_m{str(m).replace('.', '_')}.csv"
                save_path = os.path.join(path_save, filename)
                sgfcmed_iterative_fast(malware_strings.copy(), c, m, save_path, label="malware",
                                       tolerance_percent=0.5, max_iter=50)

    del malware_df, malware_strings
    print("✅ All datasets processed successfully.")