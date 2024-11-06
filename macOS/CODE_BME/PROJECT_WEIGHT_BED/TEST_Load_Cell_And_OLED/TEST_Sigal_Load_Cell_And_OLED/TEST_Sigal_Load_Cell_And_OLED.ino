#include <HX711_ADC.h>
#if defined(ESP8266) || defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif
#include <Wire.h>
#include <LiquidCrystal_I2C.h> 

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int HX711_sck = 4;
const int HX711_dout = 5;

HX711_ADC LoadCell1(HX711_dout, HX711_sck);

const int calVal_eepromAdress = 0;  // EEPROM address for the load cell calibration value
const int sampleSize = 10;  // Number of weight readings to store

float weightBuffer[sampleSize];  // Array to store weight values

void setup() {
  Serial.begin(57600);
  delay(10);
  
  lcd.begin();
  lcd.backlight();
  
  Serial.println("Starting...");

  checkEEPROM();

  setupLoadCell(LoadCell1, calVal_eepromAdress, "Load Cell 1");

  Serial.println("Startup complete");
}

void loop() {
  // Check the status of the load cell
  if (!checkHX711(LoadCell1, "Load Cell 1")) {
    Serial.println("Error with Load Cell. Please check connections.");
    return;
  }

  // Collect average weight after measuring 100 values
  float weight1 = getStableWeight(LoadCell1, "Load Cell 1");

  Serial.print("Weight: ");
  Serial.println(weight1);

  lcd.setCursor(0, 0);
  lcd.print("Weight: ");
  lcd.setCursor(0, 1);
  lcd.print(weight1);

  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == 'c') startCalibration();  // Call calibration function
    else if (inByte == 'v') checkEEPROM();  // Check EEPROM
    else if (inByte == 't') tareLoadCell(LoadCell1, "Load Cell 1");  // Start tare for the load cell
    else if (inByte == 'd') clearEEPROMData();  // Clear EEPROM data
  }
}

void clearEEPROMData() {
  Serial.println("Clearing EEPROM data...");
  for (int i = 0; i < EEPROM.length(); i++) {
    EEPROM.write(i, 0);
  }
#if defined(ESP8266) || defined(ESP32)
  EEPROM.commit();
#endif
  Serial.println("EEPROM data cleared.");
}

void tareLoadCell(HX711_ADC &LoadCell, const char *label) {
  Serial.print("*** Taring ");
  Serial.println(label);

  LoadCell.tareNoDelay();  // Start tare without delay

  unsigned long startTime = millis();  // Start timer
  const unsigned long timeoutDuration = 10000; // Set timeout duration (10 seconds)

  // Check tare status
  while (!LoadCell.getTareStatus()) {
    LoadCell.update();

    if (millis() - startTime > timeoutDuration) {
      Serial.print(label);
      Serial.println(" Tare operation timed out. Please check connections and try again.");
      return;
    }
  }

  Serial.print(label);
  Serial.println(" Tare complete!");
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

bool checkHX711(HX711_ADC &LoadCell, const char *label) {
  if (LoadCell.getTareTimeoutFlag()) {
    Serial.print(label);
    Serial.println(" Tare timeout. Check connections.");
    return false;
  }
  if (LoadCell.getSignalTimeoutFlag()) {
    Serial.print(label);
    Serial.println(" Signal timeout. Check connections.");
    return false;
  }
  return true;
}

float getStableWeight(HX711_ADC &LoadCell, const char *label) {
  float sum = 0.0;

  for (int i = 0; i < sampleSize; i++) {
    while (!LoadCell.update());  // Wait until there is updated data
    float weight = LoadCell.getData();
    weightBuffer[i] = weight;  // Store weight in array
    sum += weight;  // Accumulate weight
  }

  float averageWeight = sum / sampleSize;  // Calculate average
  
  if (averageWeight < 0) {
    averageWeight = 0.0;  // Set to 0 instead
  }

  return averageWeight;  // Return average for display
}

void startCalibration() {
  Serial.println("Starting Calibration for Load Cell...");
  calibrate(LoadCell1, calVal_eepromAdress, "Load Cell 1");
  Serial.println("*** Calibration Complete ***");
}

void calibrate(HX711_ADC &LoadCell, int eepromAddr, const char *label) {
  Serial.print("*** Calibrating ");
  Serial.println(label);

  Serial.println("Remove all weight from the Load Cell and send 't' to tare.");
  bool tareComplete = false;
  unsigned long startTime = millis();
  const unsigned long timeoutDuration = 10000;

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

    if (millis() - startTime > timeoutDuration) {
      Serial.println("Tare operation timed out. Please check connections and try again.");
      return;
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
  Serial.print("Saved to EEPROM address: ");
  Serial.println(addr);
}

void checkEEPROM() {
  float value;
  EEPROM.get(calVal_eepromAdress, value);

  if (value != 0) {
    Serial.print("EEPROM Data at Address ");
    Serial.print(calVal_eepromAdress);
    Serial.print(": ");
    Serial.println(value);
  } else {
    Serial.println("No valid calibration data found. Starting calibration automatically...");
    startCalibration();  // Automatically start calibration
  }
}
