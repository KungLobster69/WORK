
# 📘 SG-FCMedians: คู่มือใช้งานภาษาไทย (แบบละเอียดที่สุด)

ระบบนี้คือการจัดกลุ่มข้อความโดยใช้ **String Grammar Fuzzy C-Medians (SG-FCMedians)**  
รองรับการทำ Optimizer, Dynamic Tolerance, Resume, Parallel Computation

---

## ✅ ฟีเจอร์ (Features)

- ปรับค่าคลัสเตอร์ (c) และ fuzzifier (m) อัตโนมัติ
- ปรับ tolerance อัตโนมัติทุก iteration (Dynamic tolerance)
- วัดค่าคุณภาพ clustering: Purity, NMI, ARI
- Resume งานได้แม้โปรแกรมหยุดกลางทาง
- วาดกราฟ J(U,P) ตลอดการเรียนรู้
- บันทึกผลลัพธ์และข้อมูลกลางระหว่างทาง (temp files)

---

## 📂 โครงสร้างโฟลเดอร์ (Folders)

| รายการ | อธิบาย |
|:---|:---|
| `path` | โฟลเดอร์ข้อมูล (เช่น benign_train.json, malware_train.json) |
| `path_save` | โฟลเดอร์สำหรับบันทึกผลลัพธ์ (prototype, log, metrics) |

---

## 📌 โหมดการทำงาน (Modes)

- `"optimizer"`: รันหลายค่า c/m อัตโนมัติ หา config ที่ดีที่สุด
- `"manual"`: รันค่าที่กำหนดเอง

**แก้ตรงนี้ในไฟล์:**

```python
mode = "optimizer"  # หรือเปลี่ยนเป็น "manual"
```

---

## 🧠 ขั้นตอนการทำงาน (Workflow)

1. โหลดข้อมูลจากไฟล์ JSON (.json)
2. เลือกโหมด optimizer/manual
3. วนรันทุกคู่ (c, m)
4. สุ่ม prototype เริ่มต้นจากข้อมูลจริง
5. คำนวณ Distance Matrix ระหว่าง string และ prototype
6. คำนวณ Fuzzy Membership Matrix
7. อัปเดต prototype ผ่าน Fuzzy Median Search
8. วัด Objective J(U,P) และเช็ค convergence
9. ปรับ tolerance ลดลงทุกๆ adjust_every รอบ
10. หยุดเมื่อ prototype เปลี่ยนน้อยกว่าค่า tolerance หรือครบ max_iter

---

## ⚙️ จุดที่สามารถปรับได้ในโค้ด (Customizable Parameters)

### 📍 การเลือก c และ m:
```python
c_candidates = [100, 200, 300, 400, 500]
m_candidates = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
```

### 📍 การควบคุม batch size:
```python
batch_size = 500
candidate_batch_size = 5000
```

### 📍 การควบคุมการหยุด:
```python
tolerance_percent = 5.0
adjust_every = 1
adjust_rate = 0.9
max_iter = 50
```

---

## 📄 ไฟล์ผลลัพธ์ (Output Files)

| ไฟล์ | ความหมาย |
|:---|:---|
| `*.csv` | Prototype ที่ได้จาก clustering |
| `*_quality.json` | Purity, NMI, ARI |
| `*_J_log.csv` | ค่า J(U,P) ในแต่ละรอบ |
| `*_J_plot.png` | กราฟ Objective J(U,P) |
| `_temp.csv`, `_temp_idx.json`, `_temp_iter.json` | Temp files สำหรับ resume |

---

## ▶️ ตัวอย่างการใช้งาน (How to Use)

### ติดตั้งไลบรารีที่จำเป็น:

```bash
pip install python-Levenshtein joblib scikit-learn matplotlib tqdm
```

### รันโปรแกรม:

```bash
python 001_sgFCMed_Full.py
```

### หรือสร้างไฟล์ .bat:

```bat
@echo off
cd /d C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\CODE_02
python 001_sgFCMed_Full.py
pause
```

---

## 💡 เคล็ดลับการจูน (Tuning Tips)

- Dataset ใหญ่มาก (>10,000 strings):
  - ลด `candidate_batch_size` เหลือ 2000-3000
- อยากให้ convergence เร็วขึ้น:
  - เพิ่ม `tolerance_percent` เป็น 10% หรือ 20%
- อยากได้ clustering ละเอียดขึ้น:
  - ลด `adjust_rate` เป็น 0.85 หรือ 0.8
- อย่าลบไฟล์ temp หากต้องการ resume งาน
- RAM เยอะ (64GB ขึ้นไป): เพิ่ม `batch_size` และ `candidate_batch_size`

---

## 📌 หมายเหตุ (Important Notes)

- Resume ทำงานอัตโนมัติหากมีไฟล์ temp
- Checkpoint ระหว่าง Distance Matrix ทุก 1%
- รองรับ Parallel CPU Multi-core เต็มรูปแบบ

---
