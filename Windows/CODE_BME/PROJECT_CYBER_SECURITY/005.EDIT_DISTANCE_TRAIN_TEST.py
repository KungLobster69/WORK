import os
import pandas as pd
from tqdm import tqdm
import json

# Load all JSON files in the folder into a dictionary
def load_json_files_as_dict(folder_path):
    data_dict = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):  # ตรวจสอบเฉพาะไฟล์ที่มีนามสกุล .json
            file_path = os.path.join(folder_path, file_name)
            data_dict[file_name] = pd.read_json(file_path)
    return data_dict

# Function to calculate edit distance
def edit_distance_optimized(s1, s2):
    m, n = len(s1), len(s2)
    previous_row = list(range(n + 1))
    current_row = [0] * (n + 1)
    for i in range(1, m + 1):
        current_row[0] = i
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            current_row[j] = min(
                current_row[j - 1] + 1,
                previous_row[j] + 1,
                previous_row[j - 1] + cost
            )
        previous_row, current_row = current_row, previous_row
    return previous_row[-1]

# Function to calculate edit distances and save as JSON
def calculate_edit_distances_and_save(data_dict, test_df, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for file_name, train_df in data_dict.items():
        print(f"Calculating Edit Distance for {file_name}...")
        # Select first 3 rows of train_df and test_df for demonstration
        train_df_sample = train_df.iloc[:3]
        test_df_sample = test_df.iloc[:3]

        results = []
        total = len(train_df_sample) * len(test_df_sample)
        progress = tqdm(total=total, desc=f"Processing {file_name}", unit="calculation")
        for i, s1 in enumerate(train_df_sample.iloc[:, 0]):  # ใช้คอลัมน์แรก
            row_results = []
            for j, s2 in enumerate(test_df_sample.iloc[:, 0]):  # ใช้คอลัมน์แรก
                distance = edit_distance_optimized(s1, s2)
                row_results.append({"train_index": i, "test_index": j, "edit_distance": distance})
                progress.update(1)
            results.append(row_results)
        progress.close()
        output_file = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_distances.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"Saved results to {output_file}")

# Load train data
combined_train_data_folder = r"C:\Users\KUNG_LOBSTER69\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\04.COMBINED_TRAIN_DATA"
combined_train_data_dict = load_json_files_as_dict(combined_train_data_folder)

# Load test data
benign_test_df = pd.read_json(r"C:\Users\KUNG_LOBSTER69\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\01.TRAIN_TEST_SET\benign_test.json", lines=True)
malware_test_df = pd.read_json(r"C:\Users\KUNG_LOBSTER69\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\01.TRAIN_TEST_SET\malware_test.json", lines=True)

# Path for output
output_folder = r"C:\Users\KUNG_LOBSTER69\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\05.EDIT_DISTANCE_TRAIN_TEST"

# Calculate distances and save
calculate_edit_distances_and_save(combined_train_data_dict, benign_test_df, output_folder)
calculate_edit_distances_and_save(combined_train_data_dict, malware_test_df, output_folder)