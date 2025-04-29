
# SG-FCMedians String Clustering (Auto Optimizer + Dynamic Tolerance)

This project implements **String Grammar Fuzzy C-Medians (SG-FCMedians)** clustering with:

- ✅ Dynamic Tolerance adjustment every iteration
- ✅ Auto-optimization for finding the best `c` and `m`
- ✅ Support resume from checkpoint (fault-tolerant)
- ✅ Save Objective J(U,P) plot
- ✅ Save clustering quality metrics (Purity, NMI, ARI)

---

## 📂 Project Structure

.
├── sgfcmedians_project.py    # (Main Python Script)
├── benign_train.json         # (Input benign samples in JSONL)
├── malware_train.json        # (Input malware samples in JSONL)
├── output_folder/            # (Where results will be saved)

---

## ⚙️ How to Use

### 1. Prepare Data
- You need two JSONL files:
  - `benign_train.json`
  - `malware_train.json`
- Each line must be a **JSON object** with at least **one string field**.

Example:
{"string": "examplemalware1"}
{"string": "examplemalware2"}

(You can have extra fields but only the first column is used.)

---

### 2. Run the Script

Edit the script's **main section**:

mode = "optimizer"  # Use "optimizer" to automatically find best c/m

or

mode = "manual"     # If you want to run manually for each c/m pair

Then simply run:

python sgfcmedians_project.py

---

## 🛠 Parameters Overview

| Parameter | Description | Example |
|:---|:---|:---|
| `c_candidates` | List of candidate `c` values (number of prototypes) | `[100, 200, 300, 400, 500]` |
| `m_candidates` | List of candidate `m` values (fuzzifier) | `[2.0, 2.5, 3.0, ..., 5.0]` |
| `tolerance_percent` | Initial tolerance as percentage of c | `1.0` |
| `adjust_every` | Adjust tolerance every N iterations | `1` |
| `adjust_rate` | How much to shrink tolerance | `0.9` (shrinks 10% each time) |
| `max_iter` | Maximum number of iterations | `50` |

---

## 📊 Outputs

For each `c/m` combination:

- `label_cXXX_mX_X.csv` — Final prototype strings
- `label_cXXX_mX_X_J_log.csv` — J(U,P) objective values per iteration
- `label_cXXX_mX_X_J_plot.png` — Plot of J(U,P) vs iteration
- `label_cXXX_mX_X_quality.json` — Clustering performance (Purity, NMI, ARI)

If running `optimizer` mode:

- `label_optimization_summary.csv` — Summary of all tested c/m combinations with their scores.

---

## ✅ Features

- Auto-tuned Dynamic Tolerance: tolerance shrinks as training progresses
- Resume-safe: can recover if interrupted
- Supports large datasets via parallel distance computation
- Visualization: automatically saves J(U,P) plots
- Metric-driven Optimization: select best c/m based on Purity → NMI → ARI

---

## 📞 Contact
If you have questions, feel free to contact or create an issue.

Enjoy clustering! 🚀
