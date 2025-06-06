
# ========================================================
# 🧠 SG-FCMedians Full Clustering Script
# Description:
#     - Edit-distance-based fuzzy clustering for strings
#     - Supports checkpointing, resuming, visualization
#     - Outputs JSONL snapshots + clustering metrics
# ========================================================

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
# Path configuration
path = r"C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\TRAIN_TEST_SET"
path_save = r"C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\01.PROTOTYPE"
os.makedirs(path_save, exist_ok=True)

# Clustering parameter settings
c_mode = 'fixed' #percent,fixed
c_percentages = [10, 20]  # percentage of samples for number of prototypes
c_fixed = [100, 200, 300, 400, 500]  # for fixed mode
m_candidates = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
num_cores = max(1, os.cpu_count() - 2)

# --------------------------
# UTILITY FUNCTIONS
# --------------------------

# Load JSON lines into DataFrame
def load_json_lines(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return pd.DataFrame(data)

# Calculate c values based on either percentage or fixed list
def compute_c_candidates(n_samples, mode='percent', percentages=None, fixed=None):
    if mode == 'percent':
        return [max(1, int(n_samples * pct / 100)) for pct in percentages]
    elif mode == 'fixed':
        return fixed
    else:
        raise ValueError("Invalid c_mode. Choose 'percent' or 'fixed'.")

# Dynamically adjust batch size based on total distance comparisons
def auto_batch_size(n_samples, n_prototypes):
    total_pairs = n_samples * n_prototypes
    if total_pairs <= 10000:
        return 200
    elif total_pairs <= 50000:
        return 500
    elif total_pairs <= 200000:
        return 1000
    else:
        return 2000

# Distance between a string and prototype
def pair_distance(i, j, strings_ref, prototypes_ref):
    return (i, j, lev_distance(strings_ref[i], prototypes_ref[j]))

# Compute full D matrix with checkpoint
def compute_distance_matrix_to_prototypes_with_checkpoint(strings, prototypes, cache_path):
    n, c = len(strings), len(prototypes)
    batch_size = auto_batch_size(n, c)
    print(f"📏 Computing Distance Matrix: strings={n} × prototypes={c} (batch_size={batch_size})")

    D_path = cache_path.replace(".csv", "_partial_D.npy")
    batch_done_path = cache_path.replace(".csv", "_partial_batches.json")

    if os.path.exists(D_path):
        D = np.load(D_path)
        with open(batch_done_path, 'r') as f:
            done_batches = set(json.load(f))
        print(f"🔄 Resuming D: {len(done_batches)} batches already done")
    else:
        D = np.zeros((n, c), dtype=np.int32)
        done_batches = set()

    pairs = [(i, j) for i in range(n) for j in range(c)]
    batches = [pairs[k:k+batch_size] for k in range(0, len(pairs), batch_size)]

    for batch_idx, batch_pairs in enumerate(tqdm(batches, desc="🔧 Distance Matrix (Batched)")):
        if batch_idx in done_batches:
            continue

        results = Parallel(n_jobs=num_cores, backend="loky")(
            delayed(pair_distance)(i, j, strings, prototypes) for i, j in batch_pairs
        )
        for i, j, d in results:
            D[i, j] = d

        done_batches.add(batch_idx)

        if batch_idx % 10 == 0 or batch_idx == len(batches) - 1:
            np.save(D_path, D)
            with open(batch_done_path, 'w') as f:
                json.dump(sorted(done_batches), f)

    if os.path.exists(D_path): os.remove(D_path)
    if os.path.exists(batch_done_path): os.remove(batch_done_path)

    return D

# Update membership matrix U using D and fuzziness m
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

# Compute objective function value
def compute_objective(D, U, m):
    return np.sum((U ** m) * D)

# Nearest prototype index for each string
def assign_clusters(strings, prototypes):
    def nearest(s):
        dists = [lev_distance(s, p) for p in prototypes]
        return np.argmin(dists)
    return Parallel(n_jobs=num_cores, backend="loky")(
        delayed(nearest)(s) for s in strings
    )

# Purity score calculation
def calculate_purity(true_labels, pred_labels):
    contingency = {}
    for t, p in zip(true_labels, pred_labels):
        contingency.setdefault(p, []).append(t)
    majority = sum(Counter(v).most_common(1)[0][1] for v in contingency.values())
    return majority / len(true_labels)

# Evaluate clustering performance and save result
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


# ------------------------------------------------------
# STRING MEDIAN OPTIMIZATION (used for prototype update)
# ------------------------------------------------------
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

        batches = [candidates[i:i+5000] for i in range(0, len(candidates), 5000)]
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


# --------------------------
# ✅ INPUT VALIDATION + CHECKPOINT SAFETY
# --------------------------

# ตรวจสอบว่า input ถูกต้องและไม่ล่มตอน runtime
def validate_inputs(strings, c, label):
    if not isinstance(strings, list) or not all(isinstance(s, str) for s in strings):
        raise ValueError(f"[{label}] ❌ Input 'strings' ต้องเป็น list ของ string ทั้งหมด")
    if c > len(strings):
        raise ValueError(f"[{label}] ❌ จำนวน prototype (c={c}) มากกว่าข้อมูลทั้งหมด (n={len(strings)})")

# ตรวจ checkpoint สำหรับ resume ให้เชื่อถือได้
def validate_resume_checkpoint(checkpoint, expected_c, label):
    prototypes = checkpoint.get("prototypes", [])
    if len(prototypes) != expected_c:
        raise ValueError(f"[{label}] ❌ Resume failed: checkpoint มี prototype {len(prototypes)} ตัว แต่ต้องการ {expected_c}")
    if len(set(prototypes)) != len(prototypes):
        raise ValueError(f"[{label}] ❌ Resume failed: พบ prototype ซ้ำกันใน checkpoint")


# ------------------------------------------------------
# CLUSTERING DRIVER: sgfcmed_iterative_fast (already in previous section)
# ------------------------------------------------------
def sgfcmed_iterative_fast(strings, c, m, save_path, label,
                           tolerance_percent=1.0, max_iter=10,
                           adjust_every=1, adjust_rate=0.9):

    # ✅ ตรวจสอบ input ก่อนเริ่ม clustering
    validate_inputs(strings, c, label)

    # 📁 Paths for checkpointing and intermediate results
    checkpoint_path = save_path.replace(".csv", "_checkpoint.json")
    temp_U_path = save_path.replace(".csv", "_temp_U.npy")
    D_path = save_path.replace(".csv", "_partial_D.npy")
    batch_done_path = save_path.replace(".csv", "_partial_batches.json")
    J_log_path = save_path.replace(".csv", "_J_log.csv")
    change_log_path = save_path.replace(".csv", "_change_log.csv")

    J_values = []        # Log of objective function values
    change_counts = []   # Track prototype changes per iteration

    # 🔄 Resume logic if checkpoint exists
    if os.path.exists(checkpoint_path):
        print("🔄 Resuming from checkpoint...")
        with open(checkpoint_path, 'r') as f:
            checkpoint = json.load(f)

        # ✅ ตรวจสอบความถูกต้องของ checkpoint
        validate_resume_checkpoint(checkpoint, c, label)

        
        prototype_strings = checkpoint['prototypes']
        prototypes_idx = checkpoint['prototypes_idx']
        start_iter = checkpoint['current_iter']
        J_values = checkpoint.get('J_values', [])
        change_counts = checkpoint.get('change_counts', [])
    else:
        # 🆕 Initial random prototype selection
        indices = list(range(len(strings)))
        random.shuffle(indices)
        prototypes_idx = indices[:c]
        prototype_strings = [strings[i] for i in prototypes_idx]
        start_iter = 0
        checkpoint = {
            'prototypes': prototype_strings,
            'prototypes_idx': prototypes_idx,
            'current_iter': start_iter,
            'J_values': [],
            'change_counts': []
        }
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)

    alphabet = set(''.join(strings))  # Extract character set
    tolerance = max(1, int(c * tolerance_percent / 100))
    print(f"⚙️ Initial tolerance = {tolerance} ({tolerance_percent}% of c={c})")

    for it in range(start_iter, max_iter):
        print(f"🔁 Iteration {it+1}/{max_iter} (Current tolerance = {tolerance})")

        if os.path.exists(temp_U_path):
            print("🧠 Loading cached U matrix ...")
            U = np.load(temp_U_path)
            D = compute_distance_matrix_to_prototypes_with_checkpoint(strings, prototype_strings, save_path)
        else:
            D = compute_distance_matrix_to_prototypes_with_checkpoint(strings, prototype_strings, save_path)
            U = update_membership(D, m)
            np.save(temp_U_path, U)

        # 📉 Calculate objective function J
        J = compute_objective(D, U, m)
        J_values.append(J)
        pd.DataFrame({"iteration": list(range(1, len(J_values)+1)), "J": J_values})             .to_csv(J_log_path, index=False)
        print(f"📉 Objective J(U,P) = {J:.2f}")

        # 🧬 Update each prototype using fuzzy median
        new_prototypes = []
        for j in tqdm(range(c), desc=f"🧬 Updating Prototypes (Iter {it+1})"):
            proto = improved_fuzzy_median_string(prototype_strings[j], strings, U[:, j], alphabet)
            dists = [lev_distance(proto, s) for s in strings]
            nearest_idx = np.argmin(dists)
            new_prototypes.append(strings[nearest_idx])

        # 💾 Save prototype snapshot (JSONL) for this iteration
        proto_iter_save_path = save_path.replace(".csv", f"_prototype_iter{it}.jsonl")
        with open(proto_iter_save_path, 'w', encoding='utf-8') as f:
            for p in new_prototypes:
                json.dump({'prototype': p}, f)
                f.write('\n')

        # 🔎 Count how many prototypes changed
        changes = sum(1 for a, b in zip(prototype_strings, new_prototypes) if a != b)
        change_counts.append(changes)
        print(f"🔎 Prototype changes: {changes}")

        # 💾 Save prototype change log
        pd.DataFrame({"iteration": list(range(1, len(change_counts)+1)), "changes": change_counts})             .to_csv(change_log_path, index=False)

        # 🔁 Save checkpoint
        checkpoint['prototypes'] = new_prototypes
        checkpoint['prototypes_idx'] = [strings.index(p) for p in new_prototypes]
        checkpoint['current_iter'] = it + 1
        checkpoint['J_values'] = J_values
        checkpoint['change_counts'] = change_counts
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)

        prototype_strings = new_prototypes

        if (it + 1) % adjust_every == 0:
            tolerance = max(1, int(tolerance * adjust_rate))
            print(f"⚙️ Adjusted tolerance to {tolerance}")

        if changes <= tolerance:
            print(f"🛑 Stopping: prototypes converged (changes={changes} <= tolerance={tolerance}).")
            break

    # 📊 Plot objective J over iterations
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(J_values)+1), J_values, marker='o')
    plt.title(f"Objective J(U,P) vs Iteration (label={label}, c={c}, m={m})")
    plt.xlabel("Iteration")
    plt.ylabel("Objective J(U,P)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path.replace(".csv", "_J_plot.png"))
    plt.close()

    # 📈 Plot prototype change count
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, len(change_counts)+1), change_counts, marker='x', color='red')
    plt.title(f"Prototype Change Count vs Iteration (label={label}, c={c}, m={m})")
    plt.xlabel("Iteration")
    plt.ylabel("# Prototype Changes")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path.replace(".csv", "_change_plot.png"))
    plt.close()

    # 💾 Save final prototype list
    pd.DataFrame({'prototype': prototype_strings}).to_csv(save_path, index=False)

    # ✅ Evaluate final clustering
    true_labels = [0 if label == 'benign' else 1] * len(strings)
    evaluate_clustering_quality(strings, prototype_strings, true_labels, save_path)

    # 🧹 Cleanup temporary files
    for f in [checkpoint_path, temp_U_path, D_path, batch_done_path]:
        if os.path.exists(f):
            os.remove(f)

    print(f"\n🏁 Done: saved final results to {save_path}")


# ------------------------------------------------------
# HYPERPARAMETER OPTIMIZER
# ------------------------------------------------------
def optimizer_c_m(strings, label, c_candidates, m_candidates, save_dir,
                  tolerance_percent=1.0, max_iter=10):
    results = []
    os.makedirs(save_dir, exist_ok=True)

    for c in c_candidates:
        for m in m_candidates:
            print(f"\n🚀 Trying c={c}, m={m} ...")
            filename = f"{label}_c{c}_m{str(m).replace('.', '_')}.csv"
            save_path = os.path.join(save_dir, filename)

            sgfcmed_iterative_fast(strings.copy(), c, m, save_path, label,
                                   tolerance_percent=tolerance_percent, max_iter=max_iter)

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

    df_results = pd.DataFrame(results)
    df_results.to_csv(os.path.join(save_dir, f"{label}_optimization_summary.csv"), index=False)

    df_sorted = df_results.sort_values(
        by=['purity', 'nmi', 'ari'],
        ascending=[False, False, False]
    ).reset_index(drop=True)

    best_c = df_sorted.loc[0, 'c']
    best_m = df_sorted.loc[0, 'm']

    print(f"\n🏆 Best configuration: c={best_c}, m={best_m}")
    return best_c, best_m


# ------------------------------------------------------
# MAIN EXECUTION BLOCK
# ------------------------------------------------------
if __name__ == "__main__":
    mode = "manual"  # or "manual" , "optimizer

    print("📥 Loading benign dataset ...")
    benign_df = load_json_lines(os.path.join(path, "benign_train.json"))
    benign_strings = benign_df.iloc[:, 0].astype(str).tolist()

    benign_c_candidates = compute_c_candidates(
        n_samples=len(benign_strings),
        mode=c_mode,
        percentages=c_percentages,
        fixed=c_fixed
    )

    if mode == "optimizer":
        print("🔍 Running optimizer for benign dataset ...")
        optimizer_c_m(
            strings=benign_strings,
            label="benign",
            c_candidates=benign_c_candidates,
            m_candidates=m_candidates,
            save_dir=path_save,
            tolerance_percent=20,
            max_iter=3
        )
    else:
        for c in benign_c_candidates:
            for m in m_candidates:
                filename = f"benign_c{c}_m{str(m).replace('.', '_')}.csv"
                save_path = os.path.join(path_save, filename)
                sgfcmed_iterative_fast(benign_strings.copy(), c, m, save_path, label="benign",
                                       tolerance_percent=1.0, max_iter=3)

    del benign_df, benign_strings
    print("✅ All datasets processed successfully.")
