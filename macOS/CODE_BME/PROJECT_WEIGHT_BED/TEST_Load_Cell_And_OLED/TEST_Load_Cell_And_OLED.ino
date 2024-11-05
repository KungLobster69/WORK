#include <HX711_ADC.h>
#if defined(ESP8266) || defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif
#include <Wire.h>
#include <LiquidCrystal_I2C.h> 

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int HX711_sck[] = {A0, A2, A4, A6};
const int HX711_dout[] = {A1, A3, A5, A7};

HX711_ADC LoadCell1(HX711_dout[0], HX711_sck[0]);
HX711_ADC LoadCell2(HX711_dout[1], HX711_sck[1]);
HX711_ADC LoadCell3(HX711_dout[2], HX711_sck[2]);
HX711_ADC LoadCell4(HX711_dout[3], HX711_sck[3]);

const int calVal_eepromAdress[] = {0, sizeof(float), sizeof(float) * 2, sizeof(float) * 3};  // Adjusted for four load cells
const int sampleSize = 10;  // Number of weight readings to store

float weightBuffer[sampleSize];  // Array to store weight values

void setup() {
  Serial.begin(57600);
  delay(10);
  
  lcd.begin();
  lcd.backlight();
  
  Serial.println("Starting...");

  checkEEPROM();

  setupLoadCell(LoadCell1, calVal_eepromAdress[0], "Load Cell 1");
  setupLoadCell(LoadCell2, calVal_eepromAdress[1], "Load Cell 2");
  setupLoadCell(LoadCell3, calVal_eepromAdress[2], "Load Cell 3");
  setupLoadCell(LoadCell4, calVal_eepromAdress[3], "Load Cell 4");

  Serial.println("Startup complete");
}

void loop() {
  // Check the status of each load cell
  if (!checkHX711(LoadCell1, "Load Cell 1") ||
      !checkHX711(LoadCell2, "Load Cell 2") ||
      !checkHX711(LoadCell3, "Load Cell 3") ||
      !checkHX711(LoadCell4, "Load Cell 4")) {
    Serial.println("Error with one or more Load Cells. Please check connections.");
    return;  // Exit loop if there is an error
  }

  // Collect average weight after measuring 100 values
  float weight1 = getStableWeight(LoadCell1, "Load Cell 1");
  float weight2 = getStableWeight(LoadCell2, "Load Cell 2");
  float weight3 = getStableWeight(LoadCell3, "Load Cell 3");
  float weight4 = getStableWeight(LoadCell4, "Load Cell 4");

  float totalWeight = weight1 + weight2 + weight3 + weight4;

  Serial.print("Total Weight: ");
  Serial.println(totalWeight);

  lcd.setCursor(0, 0);
  lcd.print("Total Weight: ");
  lcd.setCursor(0, 1);
  lcd.print(totalWeight);

  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == 'c') startCalibration();  // Call calibration function
    else if (inByte == 'v') checkEEPROM();  // Check EEPROM
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

// Function to check the HX711 status
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
  return true;  // Load cell is working correctly
}

float getStableWeight(HX711_ADC &LoadCell, const char *label) {
  float sum = 0.0;

  // Store weight for 100 times and find the average
  for (int i = 0; i < sampleSize; i++) {
    while (!LoadCell.update());  // Wait until there is updated data
    float weight = LoadCell.getData();
    weightBuffer[i] = weight;  // Store weight in array
    sum += weight;  // Accumulate weight
  }

  float averageWeight = sum / sampleSize;  // Calculate average
  
  // Check and fix negative weight values
  if (averageWeight < 0) {
    averageWeight = 0.0;  // Set to 0 instead
  }
  // Remove or comment out the print statements for average weight// Remove or comment out the print statements for average weight
  //Serial.print(label);
  //Serial.print(" Average Weight: ");
  //Serial.println(averageWeight);

  return averageWeight;  // Return average for display
}

void startCalibration() {
  Serial.println("Starting Calibration for All Load Cells...");

  // Start calibration for each load cell
  calibrate(LoadCell1, calVal_eepromAdress[0], "Load Cell 1");
  calibrate(LoadCell2, calVal_eepromAdress[1], "Load Cell 2");
  calibrate(LoadCell3, calVal_eepromAdress[2], "Load Cell 3");
  calibrate(LoadCell4, calVal_eepromAdress[3], "Load Cell 4");

  Serial.println("*** All Load Cells Calibrated Successfully ***");
}

void calibrate(HX711_ADC &LoadCell, int eepromAddr, const char *label) {
  Serial.print("*** Calibrating ");
  Serial.println(label);

  // Tare
  Serial.println("Remove all weight from the Load Cell and send 't' to tare.");
  bool tareComplete = false;
  unsigned long startTime = millis();  // Record the start time
  const unsigned long timeoutDuration = 10000; // Set a timeout duration (10 seconds)

  while (!tareComplete) {
    LoadCell.update();
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 't') {
        LoadCell.tareNoDelay();
        Serial.println("Taring in progress...");
      }
    }

    // Check if tare operation has completed
    if (LoadCell.getTareStatus()) {
      Serial.println("Tare complete!");
      tareComplete = true;
    }

    // Check for timeout
    if (millis() - startTime > timeoutDuration) {
      Serial.println("Tare operation timed out. Please check connections and try again.");
      return; // Exit the calibration process
    }
  }

  // Use a known weight
  Serial.println("Place known mass on the Load Cell and send the weight (e.g., 100.0):");
  float known_mass = getUserInputFloat();
  LoadCell.refreshDataSet();
  float newCalVal = LoadCell.getNewCalibration(known_mass);

  Serial.print("New Calibration Value: ");
  Serial.println(newCalVal);

  // Save to EEPROM
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
    Serial.println("No valid calibration data found. Starting calibration automatically...");
    startCalibration();  // Automatically start calibration
  }
}
