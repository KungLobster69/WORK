#include <HX711_ADC.h>
#if defined(ESP8266) || defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int HX711_dout[] = {A0, A2, A4, A6};
const int HX711_sck[] = {A1, A3, A5, A7};

HX711_ADC LoadCell1(HX711_dout[0], HX711_sck[0]);
HX711_ADC LoadCell2(HX711_dout[1], HX711_sck[1]);
HX711_ADC LoadCell3(HX711_dout[2], HX711_sck[2]);
HX711_ADC LoadCell4(HX711_dout[3], HX711_sck[3]);

const int calVal_eepromAdress[] = {0, sizeof(float), 2 * sizeof(float), 3 * sizeof(float)};
const int sampleSize = 10;

void setup() {
  Serial.begin(57600);
  delay(10);
  
  lcd.begin();
  lcd.backlight();
  
  Serial.println("Starting...");

  //checkEEPROM();

  setupLoadCell(LoadCell1, calVal_eepromAdress[0], "Load Cell 1");
  setupLoadCell(LoadCell2, calVal_eepromAdress[1], "Load Cell 2");
  setupLoadCell(LoadCell3, calVal_eepromAdress[2], "Load Cell 3");
  setupLoadCell(LoadCell4, calVal_eepromAdress[3], "Load Cell 4");

  Serial.println("Startup complete");
}

void loop() {
  float weight1 = getStableWeight(LoadCell1);
  float weight2 = getStableWeight(LoadCell2);
  float weight3 = getStableWeight(LoadCell3);
  float weight4 = getStableWeight(LoadCell4);

  float totalWeight = weight1 + weight2 + weight3 + weight4;

  Serial.print("Total Weight: ");
  Serial.println(totalWeight);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Total Weight: ");
  lcd.setCursor(0, 1);
  lcd.print(totalWeight);

  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == 'c') startCalibration();
    else if (inByte == 'v') checkEEPROM();
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
  } else {
    calibrate(LoadCell, eepromAddr, label);
  }
}

float getStableWeight(HX711_ADC &LoadCell) {
  float sum = 0.0;

  for (int i = 0; i < sampleSize; i++) {
    while (!LoadCell.update());
    sum += LoadCell.getData();
  }

  float averageWeight = sum / sampleSize;
  return (averageWeight < 0) ? 0.0 : averageWeight;
}

void startCalibration() {
  Serial.println("Starting Calibration for All Load Cells...");

  Serial.println("Do you want to clear EEPROM? (y/n)");
  bool clearConfirmed = false;
  while (!clearConfirmed) {
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'y') {
        clearEEPROM();
        clearConfirmed = true;
      } else if (inByte == 'n') {
        Serial.println("EEPROM not cleared.");
        clearConfirmed = true;
      }
    }
  }

  calibrate(LoadCell1, calVal_eepromAdress[0], "Load Cell 1");
  calibrate(LoadCell2, calVal_eepromAdress[1], "Load Cell 2");
  calibrate(LoadCell3, calVal_eepromAdress[2], "Load Cell 3");
  calibrate(LoadCell4, calVal_eepromAdress[3], "Load Cell 4");

  Serial.println("*** All Load Cells Calibrated Successfully ***");
}

void calibrate(HX711_ADC &LoadCell, int eepromAddr, const char *label) {
  Serial.print("*** Calibrating ");
  Serial.println(label);

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

  Serial.println("Place known mass on the Load Cell and send the weight (e.g., 100.0):");
  float known_mass = getUserInputFloat();
  LoadCell.refreshDataSet();
  float newCalVal = LoadCell.getNewCalibration(known_mass);

  Serial.print("New Calibration Value: ");
  Serial.println(newCalVal);

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
}

void clearEEPROM() {
  for (int i = 0; i < EEPROM.length(); i++) {
    EEPROM.write(i, 0);
  }
#if defined(ESP8266) || defined(ESP32)
  EEPROM.commit();
#endif
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
    startCalibration();
  }
}
