import pandas as pd
import numpy as np
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from rapidfuzz.distance import Levenshtein
from threading import Lock

# ระบุพาธของไฟล์ JSON สำหรับ benign และ malware
benign_train_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\01.TRAIN_TEST_SET\benign_train.json'
malware_train_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\01.TRAIN_TEST_SET\malware_train.json'

# โหลด JSON สำหรับ benign และ malware
benign_train_df = pd.read_json(benign_train_path, lines=True)
malware_train_df = pd.read_json(malware_train_path, lines=True)

# ดึงข้อมูลสตริงสำหรับ benign และ malware
benign_strings = benign_train_df.iloc[:, 0].values
malware_strings = malware_train_df.iloc[:, 0].values

# Utility functions สำหรับ save/load progress
def save_progress(distance_matrix, current_progress, save_path, checkpoint_path):
    np.save(save_path, distance_matrix)
    np.savez(checkpoint_path, current_progress=current_progress)

def load_progress(save_path, checkpoint_path):
    if os.path.exists(save_path) and os.path.exists(checkpoint_path):
        distance_matrix = np.load(save_path)
        checkpoint_data = np.load(checkpoint_path)
        if 'current_progress' in checkpoint_data:
            return distance_matrix, int(checkpoint_data['current_progress'])
    return None, 0

def calculate_pairwise_edit_distance_single(strings, save_path, checkpoint_path, dataset_name):
    print(f"Starting {dataset_name} Edit Distance calculation...")

    n = len(strings)
    total_calculations = n * (n - 1) // 2
    distance_matrix, current_progress = load_progress(save_path, checkpoint_path)
    if distance_matrix is None:
        distance_matrix = np.zeros((n, n))

    save_interval = 100  # บันทึกผลทุกๆ n คู่ที่คำนวณเสร็จ

    overall_progress = tqdm(total=total_calculations, unit="pair", desc=f"{dataset_name} Progress", unit_scale=True, initial=current_progress)

    try:
        for i in range(n):
            for j in range(i + 1, n):  # คำนวณเฉพาะครึ่งบนของเมทริกซ์
                if distance_matrix[i, j] == 0:  # คำนวณเฉพาะที่ยังไม่ได้คำนวณ
                    # คำนวณ Edit Distance
                    distance_matrix[i, j] = distance_matrix[j, i] = Levenshtein.distance(strings[i], strings[j])
                    
                    # อัปเดตความคืบหน้ารวม
                    current_progress += 1
                    overall_progress.update(1)

                    # บันทึกผลหลังจากคำนวณครบทุก save_interval
                    if current_progress % save_interval == 0:
                        save_progress(distance_matrix, current_progress, save_path, checkpoint_path)

    finally:
        # ปิด bar ความคืบหน้ารวมเมื่อเสร็จสิ้น
        overall_progress.close()

    # บันทึกผลลัพธ์ครั้งสุดท้าย
    np.save(save_path, distance_matrix)
    print(f"{dataset_name} matrix saved successfully at {save_path}")

# คำนวณและบันทึก distance_matrix สำหรับ benign
benign_save_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\02.EDIT_DISTANCE_MATRIX\benign_distance_matrix.npy'
benign_checkpoint_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\02.EDIT_DISTANCE_MATRIX\benign_checkpoint.npz'
calculate_pairwise_edit_distance_single(benign_strings, benign_save_path, benign_checkpoint_path, "Benign")

# คำนวณและบันทึก distance_matrix สำหรับ malware
malware_save_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\02.EDIT_DISTANCE_MATRIX\malware_distance_matrix.npy'
malware_checkpoint_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\02.EDIT_DISTANCE_MATRIX\malware_checkpoint.npz'
calculate_pairwise_edit_distance_single(malware_strings, malware_save_path, malware_checkpoint_path, "Malware")