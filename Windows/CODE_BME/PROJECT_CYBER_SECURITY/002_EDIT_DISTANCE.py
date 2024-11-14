import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import os

# ระบุพาธของไฟล์ JSON สำหรับ benign และ malware
benign_train_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\01.TRAIN_TEST_SET\benign_train.json'
malware_train_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\01.TRAIN_TEST_SET\malware_train.json'

# โหลด JSON สำหรับ benign และ malware
benign_train_df = pd.read_json(benign_train_path, lines=True)
malware_train_df = pd.read_json(malware_train_path, lines=True)

@lru_cache(maxsize=None)
def optimized_edit_distance(str1, str2):
    m, n = len(str1), len(str2)
    previous_row = list(range(n + 1))
    current_row = [0] * (n + 1)

    for i in range(1, m + 1):
        current_row[0] = i
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                current_row[j] = previous_row[j - 1]
            else:
                current_row[j] = 1 + min(previous_row[j], current_row[j - 1], previous_row[j - 1])
        previous_row, current_row = current_row, previous_row

    return previous_row[n]

def save_progress(distance_matrix, current_i, current_j, save_path, checkpoint_path):
    # Save the current state of the matrix and parameters
    np.save(save_path, distance_matrix)
    np.savez(checkpoint_path, i=current_i, j=current_j)
    print(f"Progress saved: current pair ({current_i}, {current_j}) saved to {save_path} and {checkpoint_path}")

def load_progress(save_path, checkpoint_path):
    # Load saved matrix and parameters if they exist
    if os.path.exists(save_path) and os.path.exists(checkpoint_path):
        distance_matrix = np.load(save_path)
        checkpoint_data = np.load(checkpoint_path)
        return distance_matrix, checkpoint_data['i'], checkpoint_data['j']
    else:
        return None, 0, 0

def calculate_pairwise_distance(i, j, strings, distance_matrix, dataset_name, save_path, checkpoint_path):
    # Save progress immediately when starting a new calculation
    save_progress(distance_matrix, i, j, save_path, checkpoint_path)
    
    # คำนวณระยะห่างและจัดเก็บใน matrix
    distance = optimized_edit_distance(strings[i], strings[j])
    distance_matrix[i, j] = distance
    distance_matrix[j, i] = distance
    print(f"Distance between items {i} and {j} in {dataset_name} Done !!!")

def calculate_distance_matrix(strings, save_path, checkpoint_path, dataset_name):
    print(f"Starting calculation for {dataset_name} dataset...")

    # Load or initialize distance matrix and checkpoints
    distance_matrix, start_i, start_j = load_progress(save_path, checkpoint_path)
    if distance_matrix is None:
        distance_matrix = np.zeros((len(strings), len(strings)))

    # ใช้ ThreadPoolExecutor เพื่อคำนวณคู่สตริงพร้อมกัน
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(start_i, len(strings)):
            for j in range(start_j if i == start_i else 0, len(strings)):
                futures.append(executor.submit(calculate_pairwise_distance, i, j, strings, distance_matrix, dataset_name, save_path, checkpoint_path))
            start_j = 0  # Reset start_j after the first row

        # รอให้ทุกคู่คำนวณเสร็จ
        for future in futures:
            future.result()

    # บันทึก distance_matrix สุดท้ายลงในไฟล์
    np.save(save_path, distance_matrix)
    print(f"{dataset_name} matrix saved successfully at {save_path}")

# ดึงข้อมูลสตริงสำหรับ benign และ malware
benign_strings = benign_train_df.iloc[:, 0].values
malware_strings = malware_train_df.iloc[:, 0].values

# คำนวณและบันทึก distance_matrix สำหรับ benign
benign_save_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\02.EDIT_DISTANCE_MATRIX\benign_distance_matrix.npy'
benign_checkpoint_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\02.EDIT_DISTANCE_MATRIX\benign_checkpoint.npz'
calculate_distance_matrix(benign_strings, benign_save_path, benign_checkpoint_path, "Benign")

# คำนวณและบันทึก distance_matrix สำหรับ malware
malware_save_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\02.EDIT_DISTANCE_MATRIX\malware_distance_matrix.npy'
malware_checkpoint_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\02.EDIT_DISTANCE_MATRIX\malware_checkpoint.npz'
calculate_distance_matrix(malware_strings, malware_save_path, malware_checkpoint_path, "Malware")