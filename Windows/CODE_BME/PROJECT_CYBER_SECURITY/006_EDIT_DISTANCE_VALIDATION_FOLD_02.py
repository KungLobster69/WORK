import os
import json
import pandas as pd
from tqdm import tqdm
from rapidfuzz.distance import Levenshtein
from concurrent.futures import ProcessPoolExecutor, as_completed

# ✅ อ่าน JSON
def read_json_raw(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                print(f"⚠️ Warning: {file_path} is empty.")
                return []
            return json.loads(content)
    except Exception as e:
        print(f"❌ Error reading JSON file at {file_path}: {e}")
        return []

def check_and_load_raw(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return []
    return read_json_raw(file_path)

def load_existing_progress(csv_file_path, total_rows):
    if os.path.exists(csv_file_path):
        try:
            df = pd.read_csv(csv_file_path, header=None)
            current_rows = len(df)
            if current_rows >= total_rows:
                return None
            return current_rows
        except:
            return 0
    return 0

def save_progress(csv_file_path, data_row):
    with open(csv_file_path, 'a', encoding='utf-8') as f:
        f.write(",".join(map(str, data_row)) + "\n")

# ✅ ฟังก์ชันที่จะรันในแต่ละ process
def compute_distance_row(args):
    train_idx, train_str, test_strs, csv_file_name = args
    distance_row = [Levenshtein.distance(train_str, test_str) for test_str in test_strs]
    
    # ✅ log ทุกแถว (ใส่เฉพาะที่นี่เพื่อไม่ให้ output ซ้ำ)
    print(f"[{csv_file_name}] ✅ Done Train {train_idx} → Saved {len(distance_row)} distances")
    
    return (train_idx, distance_row)

# ✅ Main script
main_path = r'C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\05.DATA_VALIDATION'
output_base = r'C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\06.EDIT_DISTANCE_VALIDATION'

folds = [f"fold_{i}" for i in range(2, 3)]
MALWARE = ["MALWARE_100"]
BENIGN = ["BENIGN_100"]

for fold in folds:
    validation_fold_path = os.path.join(main_path, fold)
    output_path = os.path.join(output_base, fold)

    for cluster_01 in MALWARE:
        for cluster_02 in BENIGN:
            combined_folder_name = f"{cluster_01}_{cluster_02}"
            validation_combined_path = os.path.join(validation_fold_path, combined_folder_name)

            validation_train_path = os.path.join(validation_combined_path, "validation_train.json")
            validation_test_path = os.path.join(validation_combined_path, "validation_test.json")

            train_data = check_and_load_raw(validation_train_path)
            test_data = check_and_load_raw(validation_test_path)

            if not train_data or not test_data:
                continue

            csv_file_name = f"MATRIX_EDIT_DISTANCE_{cluster_01}_{cluster_02}.csv"
            csv_file_path = os.path.join(output_path, csv_file_name)
            os.makedirs(output_path, exist_ok=True)

            start_index = load_existing_progress(csv_file_path, len(train_data))
            if start_index is None:
                print(f"✅ Already completed: {csv_file_name}")
                continue

            print(f"🚀 Starting MULTIPROCESSING ({os.cpu_count()} cores) from index {start_index} → {csv_file_name}")

            test_strs = [str(t) for t in test_data]
            tasks = [
                (i, str(train_data[i]), test_strs, csv_file_name)
                for i in range(start_index, len(train_data))
            ]

            with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
                futures = {executor.submit(compute_distance_row, task): task[0] for task in tasks}

                # ✅ เก็บผลลัพธ์ตามลำดับ index
                results = {}
                for future in tqdm(as_completed(futures), total=len(futures), desc="Processing"):
                    train_idx, row = future.result()
                    results[train_idx] = row

                # ✅ เขียนผลลัพธ์ตามลำดับ index (resume-safe)
                for train_idx in sorted(results.keys()):
                    save_progress(csv_file_path, results[train_idx])

            print(f"✅ Finished and saved to {csv_file_path}")