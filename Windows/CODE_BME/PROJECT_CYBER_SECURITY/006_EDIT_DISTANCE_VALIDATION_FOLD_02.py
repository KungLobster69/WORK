import os
import json
import pandas as pd
from tqdm import tqdm
from rapidfuzz.distance import Levenshtein

# ✅ อ่าน JSON
def read_json_raw(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                print(f"⚠️ Warning: {file_path} is empty.")
                return []
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error reading JSON file at {file_path}: {e}")
        return []

# ✅ เช็กว่าไฟล์มีไหม
def check_and_load_raw(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return []
    return read_json_raw(file_path)

# ✅ โหลดจำนวนแถวที่คำนวณไปแล้ว
def load_existing_progress(csv_file_path, total_rows):
    if os.path.exists(csv_file_path):
        try:
            df = pd.read_csv(csv_file_path, header=None)
            current_rows = len(df)
            if current_rows >= total_rows:
                return None  # ทำครบแล้ว
            return current_rows  # คำนวณต่อจากตรงนี้
        except Exception as e:
            print(f"⚠️ Error reading existing CSV: {e}")
            return 0
    return 0

# ✅ บันทึกเพิ่มทีละแถว
def save_progress(csv_file_path, data_row):
    with open(csv_file_path, 'a', encoding='utf-8') as f:
        f.write(",".join(map(str, data_row)) + "\n")

# ✅ Path หลัก
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

            print(f"🚀 Resuming from index {start_index} → {csv_file_name}")
            for train_idx in tqdm(range(start_index, len(train_data)), desc=f"{csv_file_name}"):
                train_str = str(train_data[train_idx])
                test_strs = [str(item) for item in test_data]

                distance_row = []
                for test_idx, test_str in enumerate(test_strs):
                    dist = Levenshtein.distance(train_str, test_str)
                    distance_row.append(dist)

                    # ✅ print ทุก 10 test หรือ test สุดท้าย
                    if test_idx % 10 == 0 or test_idx == len(test_strs) - 1:
                        print(f"[{csv_file_name}] Train {train_idx}/{len(train_data)} - Test {test_idx}/{len(test_strs)} → Distance: {dist}")

                save_progress(csv_file_path, distance_row)

            print(f"✅ Finished and saved to {csv_file_path}")