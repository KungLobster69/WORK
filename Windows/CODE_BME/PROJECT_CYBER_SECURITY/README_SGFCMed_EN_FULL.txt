
# 📘 SG-FCMedians: Full User Manual (English Version)

This project implements **String Grammar Fuzzy C-Medians (SG-FCMedians)**  
for clustering sequences based on Levenshtein Distance, with optimizer, dynamic tolerance, and resume functionality.

---

## ✅ Features

- Automatic optimization of clusters (c) and fuzzifier (m)
- Dynamic tolerance adjustment at every iteration
- Evaluation metrics: Purity, NMI, ARI
- Resume support using temporary checkpoint files
- J(U,P) objective function graphing across iterations
- Fully parallelized computation

---

## 📂 Folder Structure

| Item | Description |
|:---|:---|
| `path` | Folder containing input files (e.g., benign_train.json, malware_train.json) |
| `path_save` | Output folder for prototypes, logs, metrics |

---

## 📌 Operation Modes

- `"optimizer"`: Test multiple (c, m) pairs automatically and select the best
- `"manual"`: Run all (c, m) combinations manually specified

**Modify this in the main file:**

```python
mode = "optimizer"  # or switch to "manual"
```

---

## 🧠 Workflow

1. Load the dataset from JSON files
2. Select mode (optimizer/manual)
3. Iterate over each (c, m) combination
4. Randomly select initial prototypes from the dataset
5. Compute the Distance Matrix
6. Compute the Membership Matrix
7. Update prototypes via fuzzy median search
8. Monitor convergence using the Objective J(U,P)
9. Dynamically shrink tolerance after `adjust_every` iterations
10. Stop when prototype changes ≤ tolerance or max_iter is reached

---

## ⚙️ Customizable Parameters

### 📍 Cluster and Fuzzifier Candidates:

```python
c_candidates = [100, 200, 300, 400, 500]
m_candidates = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
```

### 📍 Batch Sizes:

```python
batch_size = 500
candidate_batch_size = 5000
```

### 📍 Stopping Conditions:

```python
tolerance_percent = 5.0
adjust_every = 1
adjust_rate = 0.9
max_iter = 50
```

---

## 📄 Output Files

| File | Description |
|:---|:---|
| `*.csv` | Selected prototype strings |
| `*_quality.json` | Evaluation metrics: Purity, NMI, ARI |
| `*_J_log.csv` | Objective J(U,P) per iteration |
| `*_J_plot.png` | J(U,P) plot graph |
| `_temp.csv`, `_temp_idx.json`, `_temp_iter.json` | Temp files for resuming |

---

## ▶️ Example Usage

### Install Required Libraries:

```bash
pip install python-Levenshtein joblib scikit-learn matplotlib tqdm
```

### Run the script:

```bash
python 001_sgFCMed_Full.py
```

### Or create a .bat file:

```bat
@echo off
cd /d C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\CODE_02
python 001_sgFCMed_Full.py
pause
```

---

## 💡 Tuning Tips

- For very large datasets (>10,000 strings):
  - Reduce `candidate_batch_size` to 2000–3000
- For faster convergence:
  - Increase `tolerance_percent` (e.g., 10% or 20%)
- For more precise clustering:
  - Decrease `adjust_rate` to 0.85 or 0.8
- Never delete temp files if you want to resume training
- If your machine has high RAM (e.g., 64GB+):
  - Increase `batch_size` and `candidate_batch_size` for faster computation

---

## 📌 Important Notes

- Automatic resume is triggered if temp files are found
- Distance matrix computation saves a checkpoint every 1%
- Fully supports parallel CPU computation

---
