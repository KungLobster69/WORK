#include <HX711_ADC.h>
#if defined(ESP8266) || defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif
#include <Wire.h>
#include <LiquidCrystal_I2C.h> 

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int HX711_dout[] = {A1, A3};
const int HX711_sck[] = {A2, A4};

HX711_ADC LoadCell1(HX711_dout[0], HX711_sck[0]);
HX711_ADC LoadCell2(HX711_dout[1], HX711_sck[1]);

const int calVal_eepromAdress[] = {0, sizeof(float)};
const int sampleSize = 100;  // จำนวนค่าวัดน้ำหนักที่จะเก็บ

float weightBuffer[sampleSize];  // อาร์เรย์เก็บค่าน้ำหนัก

void setup() {
  Serial.begin(57600);
  delay(10);
  
  lcd.begin();
  lcd.backlight();
  
  Serial.println("Starting...");

  checkEEPROM();

  setupLoadCell(LoadCell1, calVal_eepromAdress[0], "Load Cell 1");
  setupLoadCell(LoadCell2, calVal_eepromAdress[1], "Load Cell 2");

  Serial.println("Startup complete");
}

void loop() {
  // เก็บค่าเฉลี่ยน้ำหนักหลังจากวัด 500 ครั้ง
  float weight1 = getStableWeight(LoadCell1, "Load Cell 1");
  float weight2 = getStableWeight(LoadCell2, "Load Cell 2");

  float totalWeight = weight1 + weight2;

  Serial.print("Total Weight: ");
  Serial.println(totalWeight);

  lcd.setCursor(0, 0);
  lcd.print("Total Weight: ");
  lcd.setCursor(0, 1);
  lcd.print(totalWeight);

  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == 'c') startCalibration();  // เรียกฟังก์ชัน Calibration
    else if (inByte == 'v') checkEEPROM();  // ตรวจสอบ EEPROM
  }
}

void setupLoadCell(HX711_ADC &LoadCell, int eepromAddr, const char *label) {
  LoadCell.begin();
  LoadCell.start(2000, true);

  if (LoadCell.getTareTimeoutFlag() || LoadCell.getSignalTimeoutFlag()) {
    Serial.println("Timeout, check wiring and pin assignments");
    while (1);
  }

  float calVal;
  EEPROM.get(eepromAddr, calVal);

  if (calVal != 0) {
    LoadCell.setCalFactor(calVal);
    Serial.print(label);
    Serial.print(" Calibration value from EEPROM: ");
    Serial.println(calVal);
  } else {
    Serial.print(label);
    Serial.println(" No valid calibration value found. Starting calibration...");
    calibrate(LoadCell, eepromAddr, label);
  }
}

float getStableWeight(HX711_ADC &LoadCell, const char *label) {
  float sum = 0.0;

  // เก็บค่าน้ำหนัก 100 ครั้งและหาค่าเฉลี่ย
  for (int i = 0; i < sampleSize; i++) {
    while (!LoadCell.update());  // รอจนกว่าจะมีข้อมูลอัปเดต
    float weight = LoadCell.getData();
    weightBuffer[i] = weight;  // เก็บน้ำหนักในอาร์เรย์
    sum += weight;  // สะสมค่าน้ำหนัก
  }

  float averageWeight = sum / sampleSize;  // หาค่าเฉลี่ย
  
  // ตรวจสอบและแก้ไขกรณีที่ค่าน้ำหนักเป็นลบ
  if (averageWeight < 0) {
    averageWeight = 0.0;  // กำหนดให้เป็น 0 แทน
  }

  Serial.print(label);
  Serial.print(" Average Weight: ");
  Serial.println(averageWeight);

  return averageWeight;  // คืนค่าเฉลี่ยเพื่อแสดงผล
}

void startCalibration() {
  Serial.println("Starting Calibration for All Load Cells...");

  // ถามผู้ใช้ว่าต้องการล้างข้อมูลใน EEPROM หรือไม่
  Serial.println("Do you want to clear EEPROM? (y/n)");
  bool clearConfirmed = false;
  while (!clearConfirmed) {
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'y') {
        clearEEPROM();  // ล้างข้อมูลใน EEPROM
        clearConfirmed = true;
      } else if (inByte == 'n') {
        Serial.println("EEPROM not cleared.");
        clearConfirmed = true;
      }
    }
  }

  // เริ่มปรับเทียบ Load Cell ทั้งสองตัว
  calibrate(LoadCell1, calVal_eepromAdress[0], "Load Cell 1");
  calibrate(LoadCell2, calVal_eepromAdress[1], "Load Cell 2");

  Serial.println("*** All Load Cells Calibrated Successfully ***");
}

void calibrate(HX711_ADC &LoadCell, int eepromAddr, const char *label) {
  Serial.print("*** Calibrating ");
  Serial.println(label);

  // ทำการ Tare เพื่อล้างน้ำหนักปัจจุบัน
  Serial.println("Remove all weight from the Load Cell and send 't' to tare.");
  bool tareComplete = false;
  while (!tareComplete) {
    LoadCell.update();
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 't') {
        LoadCell.tareNoDelay();
        Serial.println("Taring in progress...");
      }
    }

    if (LoadCell.getTareStatus()) {
      Serial.println("Tare complete!");
      tareComplete = true;
    }
  }

  // รอผู้ใช้ใส่น้ำหนักที่รู้ค่าแน่นอน
  Serial.println("Place known mass on the Load Cell and send the weight (e.g., 100.0):");
  float known_mass = getUserInputFloat();
  LoadCell.refreshDataSet();
  float newCalVal = LoadCell.getNewCalibration(known_mass);

  Serial.print("New Calibration Value: ");
  Serial.println(newCalVal);

  // ถามผู้ใช้ว่าจะบันทึกค่าปรับเทียบลงใน EEPROM หรือไม่
  Serial.println("Save this calibration value to EEPROM? (y/n)");
  bool saveConfirmed = false;
  while (!saveConfirmed) {
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'y') {
        saveToEEPROM(eepromAddr, newCalVal);
        saveConfirmed = true;
      } else if (inByte == 'n') {
        Serial.println("Calibration value not saved.");
        saveConfirmed = true;
      }
    }
  }

  Serial.println("*** Calibration Complete ***");
}

float getUserInputFloat() {
  while (true) {
    if (Serial.available() > 0) {
      float input = Serial.parseFloat();
      if (input != 0) return input;
    }
  }
}

void saveToEEPROM(int addr, float value) {
  EEPROM.put(addr, value);
#if defined(ESP8266) || defined(ESP32)
  EEPROM.commit();
#endif
  Serial.print("Saved to EEPROM address: ");
  Serial.println(addr);
}

void clearEEPROM() {
  Serial.println("Clearing all EEPROM data...");
  for (int i = 0; i < EEPROM.length(); i++) {
    EEPROM.write(i, 0);
  }
#if defined(ESP8266) || defined(ESP32)
  EEPROM.commit();
#endif
  Serial.println("EEPROM cleared.");
}

void checkEEPROM() {
  bool hasData = false;

  for (int i = 0; i < sizeof(calVal_eepromAdress) / sizeof(calVal_eepromAdress[0]); i++) {
    float value;
    EEPROM.get(calVal_eepromAdress[i], value);

    if (value != 0) {
      hasData = true;
      Serial.print("EEPROM Data at Address ");
      Serial.print(calVal_eepromAdress[i]);
      Serial.print(": ");
      Serial.println(value);
    }
  }

  if (!hasData) {
    Serial.println("No valid calibration data found. Starting calibration...");
    startCalibration();
  }
}
