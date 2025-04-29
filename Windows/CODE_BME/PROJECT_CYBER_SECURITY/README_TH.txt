
================================================================================
📘 ชื่อไฟล์: 001_sgFCMed_Full.py
================================================================================

โปรแกรมนี้ทำการ:

- เรียกใช้งาน SG-FCMedians (String Grammar Fuzzy C-Medians) บนชุดข้อมูล string
- รองรับทั้งการรันแบบ manual และ auto optimizer (หา c และ m ที่ดีที่สุด)
- มีระบบ Dynamic tolerance ลด tolerance อัตโนมัติทุก iteration
- มีระบบ Resume ถ้าโดนหยุดกลางคัน จะสามารถ continue ได้
- บันทึก prototype, ค่า J(U,P), ค่า purity, NMI, ARI และกราฟ J(U,P)

================================================================================
🛠️ ฟังก์ชันหลักที่มีในไฟล์
================================================================================

- load_json_lines(filepath): โหลดข้อมูลจากไฟล์ JSON แบบบรรทัดต่อบรรทัด
- compute_distance_matrix_to_prototypes(strings, prototypes): คำนวณระยะทางระหว่าง string ทั้งหมดกับ prototype
- update_membership(D, m): คำนวณ matrix ของ fuzzy membership
- compute_objective(D, U, m): คำนวณค่า Objective function J(U,P)
- improved_fuzzy_median_string(current_string, strings, memberships, alphabet): หา fuzzy median ที่ดีที่สุด
- sgfcmed_iterative_fast(...): ทำการเรียนรู้แบบ SG-FCMedians พร้อม dynamic adjust tolerance และ resume ได้
- optimizer_c_m(...): หา best c และ m อัตโนมัติ

================================================================================
📂 ข้อมูล Input/Output
================================================================================

- Input:
  - benign_train.json
  - malware_train.json

- Output:
  - Prototype CSV
  - Quality JSON
  - J-log CSV
  - J-plot PNG
  - Temp files (_temp.csv, _temp_idx.json, _temp_iter.json) สำหรับ resume

================================================================================
📋 Parameters สำคัญในไฟล์
================================================================================

| ตัวแปร | อธิบาย | ค่าเริ่มต้น |
|:---|:---|:---|
| path | ที่อยู่ของชุดข้อมูล | RESULT_01/01.TRAIN_TEST_SET |
| path_save | ที่เก็บผลลัพธ์ | RESULT_02/01.PROTOTYPE |
| c_candidates | ค่าของ c ที่จะลอง | [100, 200, 300, 400, 500] |
| m_candidates | ค่าของ m ที่จะลอง | [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0] |
| batch_size | ขนาด batch ตอนคำนวณระยะทาง | 500 |
| candidate_batch_size | ขนาด batch ตอนหา fuzzy median | 5000 |
| num_cores | จำนวน core CPU ที่ใช้ | (จำนวน core ทั้งหมด - 2) |

================================================================================
🔵 วิธีการทำงาน (Flow)
================================================================================

1. โหลด dataset (benign_train.json, malware_train.json)
2. เลือก mode (optimizer หรือ manual)
3. รัน sgfcmed_iterative_fast() สำหรับแต่ละคู่ (c, m)
4. คำนวณ Distance Matrix, Membership, Update Prototype
5. วัดค่า J(U,P), ลด tolerance ทุก adjust_every รอบ
6. หยุดเมื่อ prototype เปลี่ยนน้อยกว่าค่า tolerance หรือครบ max_iter
7. บันทึกไฟล์ผลลัพธ์ทั้งหมด

================================================================================
🛠️ จุดที่แก้ไขได้ในไฟล์
================================================================================

- เปลี่ยน mode = "optimizer" หรือ "manual"
- เปลี่ยน c_candidates, m_candidates
- เปลี่ยน tolerance_percent, adjust_rate, adjust_every
- เปลี่ยน path dataset และ path save
- เปลี่ยน max_iter ตามต้องการ

================================================================================
📄 ผลลัพธ์ที่จะได้จากแต่ละ run
================================================================================

| ไฟล์ | อธิบาย |
|:---|:---|
| *.csv | Prototype string ที่ได้ |
| *_quality.json | ค่า Purity, NMI, ARI |
| *_J_log.csv | ค่า J(U,P) ต่อรอบ |
| *_J_plot.png | กราฟ J(U,P) |
| _temp.csv, _temp_idx.json, _temp_iter.json | Temp file สำหรับ resume |

================================================================================
▶️ ตัวอย่างการรัน
================================================================================

1. ตั้งค่า mode:
    mode = "optimizer"  # หรือ "manual"

2. รันไฟล์:
    python 001_sgFCMed_Full.py

3. รอให้ระบบทำงานจนเสร็จ (ไฟล์จะถูกบันทึกใน path_save)

================================================================================
💬 หมายเหตุ
================================================================================

- รองรับ Resume อัตโนมัติ (หาก temp file ยังอยู่)
- Dynamic tolerance จะช่วยให้ converge ไวขึ้น
- ใช้ Levenshtein Distance คำนวณทั้งหมด
- ใช้งาน CPU Multi-core เต็มประสิทธิภาพ

================================================================================
✅ จบ README
================================================================================
