import os
import json
import psutil
import pandas as pd
import multiprocessing
from tqdm import tqdm
from math import ceil
from concurrent.futures import ProcessPoolExecutor, as_completed
from rapidfuzz.distance import Levenshtein

def auto_config(test_data_len):
    total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
    total_cores = multiprocessing.cpu_count()
    max_ram_mb = int((total_ram_gb * 1024 * 0.8) / total_cores)
    process_workers = max(1, total_cores - 1)

    if test_data_len <= 500:
        test_parts = 2
    elif test_data_len <= 1500:
        test_parts = 4
    elif test_data_len <= 3000:
        test_parts = 6
    else:
        test_parts = 8

    print(f"⚙️ CORES={total_cores}, RAM={total_ram_gb:.2f} GB → WORKERS={process_workers}, RAM/WORKER={max_ram_mb}MB, PARTS={test_parts}")
    return test_parts, max_ram_mb, process_workers

def read_multiline_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [json.loads(line) for line in file]
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return []

def chunk_list(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]

def auto_batch_size(json_strs, max_ram_per_worker_mb=400):
    avg_size = sum(len(s.encode('utf-8')) for s in json_strs[:10]) / 10
    avg_size_mb = avg_size / 1024 / 1024
    batch = max(1, int(max_ram_per_worker_mb / avg_size_mb))
    print(f"🧠 BATCH_SIZE={batch} (~{avg_size_mb:.2f}MB/string × {batch} ≈ {batch*avg_size_mb:.2f}MB)")
    return batch

def save_row_to_csv(csv_file_path, data_row):
    with open(csv_file_path, 'a', encoding='utf-8') as f:
        f.write(",".join(map(str, data_row)) + "\n")

def get_completed_row_count(csv_file_path):
    if os.path.exists(csv_file_path):
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    return 0

def split_test_data(test_strs, num_parts):
    size = len(test_strs) // num_parts
    return [test_strs[i * size: (i + 1) * size] for i in range(num_parts - 1)] + [test_strs[(num_parts - 1) * size:]]

def compute_distance_row(train_idx, train_str, test_chunks):
    try:
        full_row = []
        for chunk in test_chunks:
            dists = [Levenshtein.distance(train_str, t) for t in chunk]
            full_row.extend(dists)
        return (train_idx, full_row)
    except Exception as e:
        return (train_idx, [])

# ✅ MAIN
if __name__ == "__main__":
    multiprocessing.set_start_method('spawn', force=True)

    base_path = r'C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY'
    train_path = os.path.join(base_path, r'RESULT\05.DATA_VALIDATION\fold_3\MALWARE_100_BENIGN_100\validation_train.json')
    malware_test_path = os.path.join(base_path, r'RESULT\01.TRAIN_TEST_SET\malware_test.json')
    benign_test_path = os.path.join(base_path, r'RESULT\01.TRAIN_TEST_SET\benign_test.json')
    output_path = os.path.join(base_path, r'RESULT\08.EDIT_DISTANCE_TEST_DATA')
    os.makedirs(output_path, exist_ok=True)
    matrix_csv_path = os.path.join(output_path, 'EDIT_DISTANCE_MATRIX_FINAL.csv')

    print("📥 Loading data...")
    with open(train_path, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    malware_test = read_multiline_json(malware_test_path)
    benign_test = read_multiline_json(benign_test_path)

    if not train_data or not malware_test or not benign_test:
        print("🚫 Missing train or test data.")
    else:
        test_strs_full = [json.dumps(t) for t in (malware_test + benign_test)]

        NUM_TEST_PARTS, MAX_RAM_PER_WORKER_MB, PROCESS_WORKERS = auto_config(len(test_strs_full))
        test_part_list = split_test_data(test_strs_full, NUM_TEST_PARTS)

        total_train = len(train_data)
        completed_rows = get_completed_row_count(matrix_csv_path)

        print(f"📊 Train={total_train}, Test={len(test_strs_full)}, PARTS={NUM_TEST_PARTS}")
        print(f"🔁 Resuming from row: {completed_rows}/{total_train}")

        for part_index, test_subset in enumerate(test_part_list):
            print(f"\n🚀 PART {part_index + 1}/{NUM_TEST_PARTS} → {len(test_subset)} strings")

            BATCH_SIZE = min(auto_batch_size(test_subset, MAX_RAM_PER_WORKER_MB), 100)
            test_chunks = chunk_list(test_subset, BATCH_SIZE)

            tasks = [
                (i, json.dumps(train_data[i]))
                for i in range(total_train) if i >= completed_rows
            ]

            if not tasks:
                print(f"✅ Already completed PART {part_index + 1}")
                continue

            with ProcessPoolExecutor(max_workers=PROCESS_WORKERS) as executor:
                futures = {
                    executor.submit(compute_distance_row, train_idx, train_str, test_chunks): train_idx
                    for train_idx, train_str in tasks
                }

                for future in tqdm(as_completed(futures), total=len(futures), desc=f"PART {part_index + 1}"):
                    try:
                        train_idx, row = future.result(timeout=300)
                        save_row_to_csv(matrix_csv_path, row)
                    except Exception as e:
                        print(f"🔥 [PART {part_index + 1}] ERROR: {e}")

        print(f"\n🎉 Done! Saved to: {matrix_csv_path}")