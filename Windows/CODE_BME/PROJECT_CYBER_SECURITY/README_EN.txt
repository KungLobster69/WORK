
================================================================================
📘 Filename: 001_sgFCMed_Full.py
================================================================================

This program performs:

- String Grammar Fuzzy C-Medians (SG-FCMedians) clustering on string datasets
- Supports both manual running and automatic optimization for c and m
- Dynamic tolerance adjustment at each iteration
- Resume functionality if interrupted
- Saves prototypes, J(U,P) values, Purity, NMI, ARI, and J(U,P) plots

================================================================================
🛠️ Main Functions in the Code
================================================================================

- load_json_lines(filepath): Load JSON lines into a DataFrame
- compute_distance_matrix_to_prototypes(strings, prototypes): Compute distance matrix between strings and prototypes
- update_membership(D, m): Calculate fuzzy membership matrix
- compute_objective(D, U, m): Compute the objective function J(U,P)
- improved_fuzzy_median_string(current_string, strings, memberships, alphabet): Find the best fuzzy median
- sgfcmed_iterative_fast(...): Main learning process with dynamic tolerance adjustment and resume
- optimizer_c_m(...): Auto-select the best c and m

================================================================================
📂 Input / Output
================================================================================

- Input:
  - benign_train.json
  - malware_train.json

- Output:
  - Prototype CSV files
  - Quality JSON files (Purity, NMI, ARI)
  - J-log CSV files
  - J-plot PNG graphs
  - Temporary files (_temp.csv, _temp_idx.json, _temp_iter.json) for resuming

================================================================================
📋 Important Parameters
================================================================================

| Parameter | Description | Default |
|:---|:---|:---|
| path | Input data folder | RESULT_01/01.TRAIN_TEST_SET |
| path_save | Output result folder | RESULT_02/01.PROTOTYPE |
| c_candidates | Candidate values for c | [100, 200, 300, 400, 500] |
| m_candidates | Candidate values for m | [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0] |
| batch_size | Batch size for distance matrix computation | 500 |
| candidate_batch_size | Batch size for candidate fuzzy medians | 5000 |
| num_cores | Number of CPU cores used | (total cores - 2) |

================================================================================
🔵 Workflow
================================================================================

1. Load datasets (benign_train.json, malware_train.json)
2. Select mode (optimizer or manual)
3. Run sgfcmed_iterative_fast() for each (c, m) pair
4. Compute Distance Matrix, Membership, Update Prototypes
5. Track J(U,P), adjust tolerance dynamically
6. Stop when prototype changes ≤ tolerance or max_iter reached
7. Save all results

================================================================================
🛠️ Configurable Parts
================================================================================

- Change `mode = "optimizer"` or `"manual"`
- Modify `c_candidates`, `m_candidates`
- Adjust `tolerance_percent`, `adjust_rate`, `adjust_every`
- Set paths for datasets and outputs
- Set maximum iterations (`max_iter`)

================================================================================
📄 Output Files per Run
================================================================================

| File | Description |
|:---|:---|
| *.csv | Final prototypes |
| *_quality.json | Purity, NMI, ARI scores |
| *_J_log.csv | J(U,P) values per iteration |
| *_J_plot.png | J(U,P) graph |
| _temp.csv, _temp_idx.json, _temp_iter.json | Temporary files for resume |

================================================================================
▶️ Example to Run
================================================================================

1. Set the mode:
    mode = "optimizer"  # or "manual"

2. Run the script:
    python 001_sgFCMed_Full.py

3. Wait until the process completes (results will be saved in path_save)

================================================================================
💬 Important Notes
================================================================================

- Resume functionality is automatic if temp files exist
- Dynamic tolerance reduces tolerance over iterations
- Levenshtein Distance is used for all computations
- Full parallel computing (multi-core CPU)

================================================================================
✅ End of README
================================================================================
