
#include <SPI.h>
#include <nRF24L01p.h>

#include <HX711_ADC.h>
#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

//pins:
//Right
const int HX711_dout_1 = 3; //mcu > HX711 no 1 dout pin
const int HX711_sck_1 = 2; //mcu > HX711 no 1 sck pin

//Left
const int HX711_dout_2 = 5; //mcu > HX711 no 2 dout pin
const int HX711_sck_2 = 4; //mcu > HX711 no 2 sck pin

//HX711 constructor (dout pin, sck pin)
HX711_ADC LoadCell_1(HX711_dout_1, HX711_sck_1); //HX711 1
HX711_ADC LoadCell_2(HX711_dout_2, HX711_sck_2); //HX711 2

const int calVal_eepromAdress_1 = 0; // eeprom adress for calibration value load cell 1 (4 bytes)
const int calVal_eepromAdress_2 = 4; // eeprom adress for calibration value load cell 2 (4 bytes)
unsigned long t = 0;

nRF24L01p transmitter(8,7);//CSN,CE

String DataSent = "";
String message;
String PRXsays;

float W_L, W_R;

//Device ID and NRF Channel3

int ID = 4;
char NRFCH = "BMEI";


void setup() {
  Serial.begin(57600); delay(10);
  Serial.println();
  Serial.println("Starting...");

  float calibrationValue_1; // calibration value load cell 1
  float calibrationValue_2; // calibration value load cell 2

  calibrationValue_1 = -17.35;//-19.64;R uncomment this if you want to set this value in the sketch
  calibrationValue_2 = -172.85;//-20.11;L uncomment this if you want to set this value in the sketch
  
#if defined(ESP8266) || defined(ESP32)
  //EEPROM.begin(512); // uncomment this if you use ESP8266 and want to fetch the value from eeprom
#endif
  //EEPROM.get(calVal_eepromAdress_1, calibrationValue_1); // uncomment this if you want to fetch the value from eeprom
  //EEPROM.get(calVal_eepromAdress_2, calibrationValue_2); // uncomment this if you want to fetch the value from eeprom

  LoadCell_1.begin();
  LoadCell_2.begin();
  unsigned long stabilizingtime = 2000; // tare preciscion can be improved by adding a few seconds of stabilizing time
  boolean _tare = true; //set this to false if you don't want tare to be performed in the next step
  byte loadcell_1_rdy = 0;
  byte loadcell_2_rdy = 0;
  while ((loadcell_1_rdy + loadcell_2_rdy) < 2) { //run startup, stabilization and tare, both modules simultaniously
    if (!loadcell_1_rdy) loadcell_1_rdy = LoadCell_1.startMultiple(stabilizingtime, _tare);
    if (!loadcell_2_rdy) loadcell_2_rdy = LoadCell_2.startMultiple(stabilizingtime, _tare);
  }
  if (LoadCell_1.getTareTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 no.1 wiring and pin designations");
  }
  if (LoadCell_2.getTareTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 no.2 wiring and pin designations");
  }
  LoadCell_1.setCalFactor(calibrationValue_1); // user set calibration value (float)
  LoadCell_2.setCalFactor(calibrationValue_2); // user set calibration value (float)
  Serial.println("Startup is complete");


    //nRF24
  SPI.begin();
  SPI.setBitOrder(MSBFIRST);
  transmitter.channel(90);// ตั้งช่องความถี่ให้ตรงกัน
  //transmitter.RXaddress("Prado");
  transmitter.TXaddress("BMEI"); // ตั้งชื่อตำแหน่งให้ตรงกัน ชื่อตั้งได้สูงสุด 5 ตัวอักษร
  transmitter.init();
  
}

void loop() {
  static boolean newDataReady = 0;
  const int serialPrintInterval = 0; //increase value to slow down serial print activity

  // check for new data/start next conversion:
  if (LoadCell_1.update()) newDataReady = true;
    LoadCell_2.update();

  //get smoothed value from data set
  if ((newDataReady)) {
    if (millis() > t + serialPrintInterval) {
       float a  = LoadCell_1.getData();
       float b = LoadCell_2.getData();
        W_R = a;
        W_L = b;
      newDataReady = 0;
      t = millis();
      ///////////// This code is only for DevID=4 //////////
      if(W_L<1000){
        W_L = 0; 
      }else{
        W_L = W_L*7.5;
      }
      ///////////////////////////////////////////////////////
      
      DataSent = String(ID)+";" + String(W_L)+";" + String(W_R*0.8);
       Serial.println(DataSent);
      
       transmitter.txPL(DataSent); // ค่าที่ต้องการส่ง
       transmitter.send(FAST); // สั่งให้ส่งออกไป
       delay(100);
       DataSent="";
    }
  }

   

//  // receive command from serial terminal, send 't' to initiate tare operation:
//  if (Serial.available() > 0) {
//    char inByte = Serial.read();
//    if (inByte == 't') {
//      LoadCell_1.tareNoDelay();
//      LoadCell_2.tareNoDelay();
//    }
//  }
//
//  //check if last tare operation is complete
//  if (LoadCell_1.getTareStatus() == true) {
//    Serial.println("Tare load cell 1 complete");
//  }
//  if (LoadCell_2.getTareStatus() == true) {
//    Serial.println("Tare load cell 2 complete");
//  }

}
