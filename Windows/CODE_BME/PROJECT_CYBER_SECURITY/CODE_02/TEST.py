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
import argparse

# --------------------------
# PARAMETERS
# --------------------------
path = r"C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT_01\01.TRAIN_TEST_SET"
path_save = r"C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT_02\01.PROTOTYPE"
os.makedirs(path_save, exist_ok=True)

# --------------------------
# PARSER FOR COMMAND LINE INPUT
# --------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(description="เลือกพารามิเตอร์และชุดข้อมูลที่ต้องการใช้")

    # เพิ่มพารามิเตอร์
    parser.add_argument('--dataset', type=str, required=True, help="ชื่อไฟล์ชุดข้อมูลที่ต้องการใช้ (เช่น benign_train.json หรือ malware_train.json)")
    parser.add_argument('--c', type=int, nargs='?', default=100, help="ค่าของ c ที่ต้องการใช้ในการคำนวณ (ค่าเดียวได้)")
    parser.add_argument('--m', type=float, nargs='?', default=2.0, help="ค่าของ m ที่ต้องการใช้ในการคำนวณ (ค่าเดียวได้)")
    parser.add_argument('--mode', choices=['percent', 'fixed'], default='percent', help="โหมดการเลือก c (percent หรือ fixed)")

    return parser.parse_args()

# --------------------------
# JSON LOADER
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
# UTILITY FUNCTIONS
# --------------------------

# การคำนวณค่าของ c
def compute_c_candidates(n_samples, mode='percent', percentages=None, fixed=None):
    if mode == 'percent':
        return [max(1, int(n_samples * pct / 100)) for pct in percentages]
    elif mode == 'fixed':
        return fixed
    else:
        raise ValueError("Invalid c_mode. Choose 'percent' or 'fixed'.")

def compute_distance_matrix_to_prototypes(strings, prototypes):
    n, c = len(strings), len(prototypes)
    D = np.zeros((n, c), dtype=np.int32)
    for i in range(n):
        for j in range(c):
            D[i, j] = lev_distance(strings[i], prototypes[j])
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
# SGFCMedIterativeFast
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

        D = compute_distance_matrix_to_prototypes(strings, prototype_strings)
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