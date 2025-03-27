import numpy as np
import json
from Levenshtein import distance as levenshtein_distance
import pandas as pd
import os
from tqdm import tqdm

def read_json_raw(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                print(f"Warning: {file_path} is empty.")
                return []
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file at {file_path}: {e}")
        return []

def flatten_list(nested_list):
    return [item for sublist in nested_list if isinstance(sublist, list) for item in sublist]

def check_and_load_raw(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    return read_json_raw(file_path)

def save_progress(csv_file_path, data):
    with open(csv_file_path, 'a', encoding='utf-8') as f:
        f.write(",".join(map(str, data)) + "\n")

def load_existing_progress(csv_file_path, train_size):
    if os.path.exists(csv_file_path):
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return len(lines) if len(lines) < train_size else None
    return 0

main_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\05.DATA_VALIDATION'

folds = [f"fold_{i}" for i in range(2, 3)]
MALWARE = [f"MALWARE_100"]
BENIGN = [f"BENIGN_100"]

for fold in folds:
    validation_fold_path = os.path.join(main_path, fold)
    output_path = os.path.join(r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\06.EDIT_DISTANCE_VALIDATION', fold)

    for cluster_01 in MALWARE:
        for cluster_02 in BENIGN:
            combined_folder_name = f"{cluster_01}_{cluster_02}"
            validation_combined_path = os.path.join(validation_fold_path, combined_folder_name)
            
            validation_train_path = os.path.join(validation_combined_path, "validation_train.json")
            validation_test_path = os.path.join(validation_combined_path, "validation_test.json")

            train_data = check_and_load_raw(validation_train_path)
            test_data = check_and_load_raw(validation_test_path)

            if train_data and test_data:
                csv_file_name = f"MATRIX_EDIT_DISTANCE_{cluster_01}_{cluster_02}.csv"
                csv_file_path = os.path.join(output_path, csv_file_name)
                os.makedirs(output_path, exist_ok=True)

                start_index = load_existing_progress(csv_file_path, len(train_data))
                if start_index is None:
                    print(f"Edit Distance Matrix already completed for {csv_file_name}")
                    continue

                print(f"Starting edit distance calculation for {csv_file_name} from index {start_index}")
                with open(csv_file_path, 'a', encoding='utf-8') as f:
                    for train_idx in tqdm(range(start_index, len(train_data)), desc=f"Processing {csv_file_name}"):
                        print(f"Processing train index: {train_idx}")
                        row = []
                        for test_idx, test_item in enumerate(tqdm(test_data, desc=f"Train {train_idx}", leave=False)):
                            print(f"Calculating distance for train index {train_idx}, test index {test_idx}")
                            row.append(levenshtein_distance(str(train_data[train_idx]), str(test_item)))
                        save_progress(csv_file_path, row)
                print(f"Resumed and saved Edit Distance Matrix to {csv_file_name}")