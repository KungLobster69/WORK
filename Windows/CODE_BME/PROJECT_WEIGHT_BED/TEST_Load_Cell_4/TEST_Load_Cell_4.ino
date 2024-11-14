#include <HX711_ADC.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#if defined(ESP8266) || defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

LiquidCrystal_I2C lcd(0x27, 16, 2);

// กำหนด pin สำหรับ load cell
const int HX711_dout[] = {A0, A2, A4, A6};
const int HX711_sck[] = {A1, A3, A5, A7};

// สร้าง object สำหรับ load cell แต่ละตัว
HX711_ADC LoadCell1(HX711_dout[0], HX711_sck[0]);
HX711_ADC LoadCell2(HX711_dout[1], HX711_sck[1]);
HX711_ADC LoadCell3(HX711_dout[2], HX711_sck[2]);
HX711_ADC LoadCell4(HX711_dout[3], HX711_sck[3]);

void setup() {
  Serial.begin(57600);
  delay(10);
  
  lcd.begin();
  lcd.backlight();
  
  Serial.println("Starting...");

  // เริ่มต้นการตั้งค่า load cell แต่ละตัว
  setupLoadCell(LoadCell1);
  setupLoadCell(LoadCell2);
  setupLoadCell(LoadCell3);
  setupLoadCell(LoadCell4);

  Serial.println("Startup complete");
}

void loop() {
  // อ่านค่าน้ำหนักจาก load cell แต่ละตัว
  float weight1 = getWeight(LoadCell1);
  float weight2 = getWeight(LoadCell2);
  float weight3 = getWeight(LoadCell3);
  float weight4 = getWeight(LoadCell4);

  // คำนวณน้ำหนักรวม
  float totalWeight = weight1 + weight2 + weight3 + weight4;

  // แสดงผลน้ำหนักของแต่ละ load cell และน้ำหนักรวมทาง Serial Monitor
  Serial.print("Weight 1: ");
  Serial.print(weight1);
  Serial.print(" | Weight 2: ");
  Serial.print(weight2);
  Serial.print(" | Weight 3: ");
  Serial.print(weight3);
  Serial.print(" | Weight 4: ");
  Serial.print(weight4);
  Serial.print(" | Total Weight: ");
  Serial.println(totalWeight);

  // แสดงน้ำหนักของแต่ละ load cell บน LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("W1:");
  lcd.print(weight1);
  lcd.print(" W2:");
  lcd.print(weight2);
  lcd.setCursor(0, 1);
  lcd.print("W3:");
  lcd.print(weight3);
  lcd.print(" W4:");
  lcd.print(weight4);

  // ตรวจสอบว่าผู้ใช้ต้องการ Tare หรือไม่
  if (Serial.available() > 0) {
    
     String msg = Serial.readStringUntil('\n');
    if (msg.startsWith("tare")) {
      tareAll();  // เรียกฟังก์ชัน tare สำหรับ load cell ทุกตัว
      Serial.println("Tare finish");
    }
  }

  delay(100);  // หน่วงเวลาสำหรับการแสดงผล
}

// ฟังก์ชันการตั้งค่า load cell แต่ละตัว
void setupLoadCell(HX711_ADC &LoadCell) {
  LoadCell.begin();
  LoadCell.start(2000, true);
  if (LoadCell.getTareTimeoutFlag() || LoadCell.getSignalTimeoutFlag()) {
    Serial.println("Timeout, check wiring and pin assignments");
    while (1);
  }
  LoadCell.setCalFactor(1000.0);  // ตั้งค่าปัจจัยการคำนวณ (Calibration factor)
  LoadCell.tareNoDelay();  // เริ่มการ tare ทันทีที่เริ่มต้น
  Serial.println("Load Cell initialized and tared.");
}

// ฟังก์ชันอ่านน้ำหนักจาก load cell โดยคืนค่าน้ำหนักปัจจุบัน
float getWeight(HX711_ADC &LoadCell) {
  while (!LoadCell.update());  // รอจนกว่าจะมีข้อมูลอัปเดต
  return LoadCell.getData();   // คืนค่าน้ำหนักปัจจุบัน
}

// ฟังก์ชัน tare สำหรับ load cell ทุกตัว
void tareAll() {
  Serial.println("Taring all load cells...");
  
  // Tare แต่ละ load cell ทีละตัวและรอให้เสร็จก่อนที่จะไปตัวถัดไป
  tareSingleLoadCell(LoadCell1, "Load Cell 1");
  tareSingleLoadCell(LoadCell2, "Load Cell 2");
  tareSingleLoadCell(LoadCell3, "Load Cell 3");
  tareSingleLoadCell(LoadCell4, "Load Cell 4");

  Serial.println("Tare complete for all load cells.");
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Tare Complete");
  delay(1000);  // แสดงข้อความ "Tare Complete" บน LCD ชั่วคราว
}

// ฟังก์ชัน Tare สำหรับ load cell แต่ละตัว
void tareSingleLoadCell(HX711_ADC &LoadCell, const char *label) {
  LoadCell.tareNoDelay();  // เริ่มการ tare
  Serial.print("Taring ");
  Serial.println(label);

  // รอให้การ tare ของ load cell นี้เสร็จสมบูรณ์
  while (!LoadCell.getTareStatus()) {
    LoadCell.update();
  }

  Serial.print(label);
  Serial.println(" tare complete!");
}
