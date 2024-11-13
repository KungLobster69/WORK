import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

# ระบุพาธของไฟล์ JSON สำหรับ benign และ malware
benign_train_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\01.TRAIN_TEST_SET\benign_train.json'
malware_train_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\01.TRAIN_TEST_SET\malware_train.json'

# โหลด JSON สำหรับ benign และ malware
benign_train_df = pd.read_json(benign_train_path, lines=True)
malware_train_df = pd.read_json(malware_train_path, lines=True)

@lru_cache(maxsize=None)  # ใช้ memoization เพื่อบันทึกค่า Edit Distance ที่คำนวณแล้ว
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

def calculate_pairwise_distance(i, j, strings, distance_matrix, dataset_name):
    # คำนวณระยะห่างและจัดเก็บใน matrix
    print(f"Calculating distance between items {i} and {j} in {dataset_name}")
    distance = optimized_edit_distance(strings[i], strings[j])
    distance_matrix[i, j] = distance
    distance_matrix[j, i] = distance
    print(f"Distance between items {i} and {j} in {dataset_name} Done !!!")

def calculate_distance_matrix(strings, save_path, dataset_name):
    print(f"Starting calculation for {dataset_name} dataset...")
    # สร้าง matrix เพื่อเก็บค่า edit distance
    distance_matrix = np.zeros((len(strings), len(strings)))

    # ใช้ ThreadPoolExecutor เพื่อคำนวณคู่สตริงพร้อมกัน
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(len(strings)):
            for j in range(i + 1, len(strings)):
                futures.append(executor.submit(calculate_pairwise_distance, i, j, strings, distance_matrix, dataset_name))

        # รอให้ทุกคู่คำนวณเสร็จ
        for future in futures:
            future.result()

    # บันทึก distance_matrix ลงในไฟล์
    np.save(save_path, distance_matrix)
    print(f"{dataset_name} matrix saved successfully at {save_path}")

# ดึงข้อมูลสตริงสำหรับ benign และ malware
benign_strings = benign_train_df.iloc[:, 0].values  # สมมติว่าคอลัมน์แรกเป็นข้อมูลที่ต้องการเปรียบเทียบ
malware_strings = malware_train_df.iloc[:, 0].values

# คำนวณและบันทึก distance_matrix สำหรับ benign
benign_save_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\02.EDIT_DISTANCE_MATRIX\benign_distance_matrix.npy'
calculate_distance_matrix(benign_strings, benign_save_path, "Benign")

# คำนวณและบันทึก distance_matrix สำหรับ malware
malware_save_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\02.EDIT_DISTANCE_MATRIX\malware_distance_matrix.npy'
calculate_distance_matrix(malware_strings, malware_save_path, "Malware")
