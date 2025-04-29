/* note
    SureSigns VS4 (admin password : 215)

    IntelliVue MP5SC (admin password : 4630)
    UDP/IP transport protocol (UDP port 24105)
*/

#define debug(txt) Serial.println(txt);



//#include "EEPROM.h"
//#define EEPROM_SIZE 10
//#define ADDR_reference_height_cm  0

#include <WiFi.h>
#include <esp_wifi.h>
#include <WiFiClientSecure.h>
#include "esp_wpa2.h"
#include <HTTPClient.h>


#include <ETH.h>

//#define ETH_CLK_MODE  ETH_CLOCK_GPIO0_IN //ETH_CLOCK_GPIO0_IN   - default: external clock from crystal oscillator
//#define ETH_CLK_MODE  ETH_CLK_GPIO0_OUT //ETH_CLOCK_GPIO16_OUT - 50MHz clock from internal APLL output on GPIO0 - possibly an inverter is needed for LAN8720
//#define ETH_CLK_MODE  ETH_CLK_GPIO16_OUT //ETH_CLOCK_GPIO16_OUT - 50MHz clock from internal APLL output on GPIO16 - possibly an inverter is needed for LAN8720
#define ETH_CLK_MODE ETH_CLOCK_GPIO17_OUT  //ETH_CLOCK_GPIO17_OUT - 50MHz clock from internal APLL inverted output on GPIO17 - tested with LAN8720

/*
     ETH_CLOCK_GPIO0_IN   - default: external clock from crystal oscillator
     ETH_CLOCK_GPIO0_OUT  - 50MHz clock from internal APLL output on GPIO0 - possibly an inverter is needed for LAN8720
     ETH_CLOCK_GPIO16_OUT - 50MHz clock from internal APLL output on GPIO16 - possibly an inverter is needed for LAN8720
     ETH_CLOCK_GPIO17_OUT - 50MHz clock from internal APLL inverted output on GPIO17 - tested with LAN8720
*/
#define ETH_CLK_MODE ETH_CLOCK_GPIO17_OUT

//Pin# of the enable signal for the external crystal oscillator (-1 to disable for internal APLL source)
#define ETH_POWER_PIN -1  //-1 // Do not use it, it can cause conflict during the software reset.

// Type of the Ethernet PHY (LAN8720 or TLK110)
#define ETH_TYPE ETH_PHY_LAN8720

// I²C-address of Ethernet PHY (0 or 1 for LAN8720, 31 for TLK110)
#define ETH_ADDR 1

// Pin# of the I²C clock signal for the Ethernet PHY
#define ETH_MDC_PIN 23

// Pin# of the I²C IO signal for the Ethernet PHY
#define ETH_MDIO_PIN 18




#include <SPI.h>
#include "src/TFT_eSPI/TFT_eSPI.h"       // Hardware-specific library
TFT_eSPI tft = TFT_eSPI();  // Invoke custom library
#define LED_ONOFF_PIN 33
uint8_t TFTupdate_event = 0x00;
void SPI_TFT_display_480x320(float person_weight_kg, float person_height_cm);
void SPI_TFT_ClearDisplay_480x320(float person_weight_kg, float person_height_cm);


#define uart0_RXD 3   //Hardware
#define uart0_TXD 1   //Hardware
#define uart1_RXD 9   //Hardware
#define uart1_TXD 10  //Hardware
//#define uart2_RXD 16 //Hardware
//#define uart2_TXD 17 //Hardware



///*TANITA {weight} and TFmini (hieght)*///
float feedback_weight_kg;
float feedback_height_cm, reference_height_cm = 224.2;
float sensor_height[2], average_height, sum_total, sum_count, sum_number = 100.0;
uint8_t TFmini_setReferenceHeight_event = 0;
float read_TANITA(String cmd);
float read_TFmini(uint8_t msg[]);
void TFmini_setReferenceHeight(void);


///*SureSingsVS4 {vital signs]*///
#define ACKCode_Accept "AA"  //changes the data from white to green
#define ACKCode_Reject "AR"  //changes the data from white to blue
#define ACKCode_Error  "AE"
uint8_t acknowledge_message_count;  // Acknowledge = 10 {\r}

void read_SureSignsVS4(String msg);
String vs4PID = "";
//String testMSG = "";



///*Patient Varaible*///
String PatientID;     //Example "O3622051614" (Patient identifier)
String SerialNumber;  // Example "US42722985"
//String PatientType; //Example "Adult"
String MeasurementDateTime;  //Example "03/04/2022 08:57:05"
float person_weight_kg;      //{unit:kg}
float person_height_cm;      //{unit:cm}
uint8_t SpO2;                //{unit:%}
uint8_t NBP_systolic;        //{unit:mmHg}
uint8_t NBP_diastolic;       //{unit:mmHg}
uint8_t NBP_mean;            //{unit:mmHg}
uint8_t HR_pulse;            //{unit:bpm}
String MessageDateTime;      //Example "20220424180911"
String MessageControl_ID;    //Example "US427229850000000014"








const char* EAP_ANONYMOUS_IDENTITY = "testwifi";  //anonymous identity
const char* EAP_IDENTITY = "testwifi";            //user identity
const char* EAP_PASSWORD = "M3d1ca1456";            //user password
const char* ssid = "BCM_Med";                     // SSID
IPAddress hostIP(10, 154, 10, 84);
const char* host = "http://10.154.10.84/api/datafromiot/index.php";
//const char* hostIP = "10.154.10.84";
const uint16_t port = 80;




IPAddress eth_ip(192, 168, 10, 10);
IPAddress eth_gateway(192, 168, 10, 1);
IPAddress eth_subnet(255, 255, 255, 0);


String post_message;
HTTPClient http;
WiFiServer VS4server(8080);
WiFiClient* VS4_client;





/*Data Collection*/
uint8_t data_collecting = 0x00;  //VS4 == 0x01, TFmni&TANITA == 0x02


void WiFiGotIP(WiFiEvent_t event, WiFiEventInfo_t info) {
  Serial.print("IP address: ");
  Serial.println(IPAddress(info.got_ip.ip_info.ip.addr));

  //Serial.print("             RSSI: "); Serial.println(WiFi.RSSI());
  //Serial.print("local MAC Address: "); Serial.println(WiFi.macAddress());
  //Serial.print("local  IP address: "); Serial.println(WiFi.localIP());
}
void WiFiDisconnected(WiFiEvent_t event, WiFiEventInfo_t info) {
  //Serial.print("WiFi lost connection. Reason: ");
  //Serial.println(info.wifi_sta_disconnected.reason);
  //Serial.println("Trying to Reconnect");
  WiFi.begin(ssid);
  //WiFi.reconnect();
}

void setup() {
  delay(1000);
  Serial.begin(115200, SERIAL_8N1);                        //"debug"
  Serial1.begin(115200, SERIAL_8N1);                       //"Benewake TFmini-S UART LiDAR Program"
  Serial2.begin(9600, SERIAL_8N1, /*RXD=*/16, /*TXD=*/5);  //"TANITA WB-3000 UART RS232 Program"


  //  EEPROM.begin(EEPROM_SIZE);
  //  reference_height_cm = EEPROM.readFloat(ADDR_reference_height_cm);
  //  if (isnan(reference_height_cm)) {
  //    EEPROM.writeFloat(ADDR_reference_height_cm, 0.0);
  //    EEPROM.commit();
  //    Serial.printf("TFmini_REF initialze == 0.0\n");
  //  }
  //  else {
  //    Serial.printf("TFmini_REF %.2f cm\n", reference_height_cm);
  //  }
  reference_height_cm = 224.2; //+/-1.8




  pinMode(LED_ONOFF_PIN, OUTPUT);
  digitalWrite(LED_ONOFF_PIN, HIGH);
  tft.init();
  tft.setRotation(3);
  tft.fillScreen(TFT_BLACK);

  PatientID = "Oxxxxxxxxxx";
  person_weight_kg = 999.9;
  person_height_cm = 999.9;
  SPI_TFT_ClearDisplay_480x320();
  //SPI_TFT_displayVS4_480x320();
  //SPI_TFT_displayTANITA_480x320();


  WiFi.onEvent(WiFiGotIP, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_GOT_IP);
  WiFi.onEvent(WiFiDisconnected, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_DISCONNECTED);

  //  /*delete old config*/
  //  WiFi.disconnect(true);
  delay(1000);
  WiFi.mode(WIFI_STA);
  esp_wifi_sta_wpa2_ent_set_identity((uint8_t*)EAP_ANONYMOUS_IDENTITY, strlen(EAP_ANONYMOUS_IDENTITY));  //provide identity
  esp_wifi_sta_wpa2_ent_set_username((uint8_t*)EAP_IDENTITY, strlen(EAP_IDENTITY));                      //provide username
  esp_wifi_sta_wpa2_ent_set_password((uint8_t*)EAP_PASSWORD, strlen(EAP_PASSWORD));                      //provide password
  esp_wifi_sta_wpa2_ent_enable();

  /*Begin WIFI Station*/
  WiFi.begin(ssid);  //connect to wifi

  delay(1000);

  Serial.printf("Hostname %s\n", WiFi.getHostname());


  ETH.begin(ETH_ADDR, ETH_POWER_PIN, ETH_MDC_PIN, ETH_MDIO_PIN, ETH_TYPE, ETH_CLK_MODE);  // Enable ETH
  ETH.config(eth_ip, eth_gateway, eth_subnet);
  Serial.print("ETH MAC: ");
  Serial.print(ETH.macAddress());
  Serial.print(", IPv4: ");
  Serial.print(ETH.localIP());
  if (ETH.fullDuplex()) {
    Serial.print(", FULL_DUPLEX");
  }
  Serial.print(", ");
  Serial.print(ETH.linkSpeed());
  Serial.println("Mbps");


  /*start the server*/
  VS4server.begin();
  VS4server.setNoDelay(true);


  delay(1000);
  Serial.print("Start IOT-BCM\n");


}  //<END> "void setup()"


void loop() {
  static uint32_t tock_updateDisplay, tock_updateHTTP;
  uint32_t uwTick = millis();

  //  if ((WiFi.status() != WL_CONNECTED) && (currentMillis - previousMillis >= 30000)) {
  //    previousMillis = currentMillis;
  //
  //    Serial.print(millis());
  //    Serial.println("Reconnecting to WiFi...");
  //    WiFi.begin(ssid); //connect to wifi
  //    previousMillis = currentMillis;
  //  }


  if (Serial1.available() >= 9) {
    uint8_t incomingByte;
    uint8_t TFminiS_data[10];
    //Serial.printf("S1[%d]:", Serial1.available());

    TFminiS_data[0] = Serial1.read();
    if (TFminiS_data[0] == 0x59) {
      TFminiS_data[1] = Serial1.read();
      if (TFminiS_data[1] == 0x59) {
        Serial1.readBytes(&(TFminiS_data[2]), 7);

        feedback_height_cm = read_TFmini(TFminiS_data);
        if (TFmini_setReferenceHeight_event == 0x01) {
          Serial.printf("%.2f %.2f\n", sensor_height[0], feedback_height_cm);
        }
        //?        Serial.printf("%02X%02X D%d S%d T%d C%02X\n",
        //?                      TFminiS_data[0], TFminiS_data[1],
        //?                      (TFminiS_data[2] | TFminiS_datat[3] << 8),
        //?                      (TFminiS_data[4] | TFminiS_data[5] << 8),
        //?                      (TFminiS_data[6] | TFminiS_data[7] << 8),
        //?                      TFminiS_data[8]);
      }
    } else if (TFminiS_data[0] == 0x5A) {
      TFminiS_data[1] = Serial1.read();
      if (TFminiS_data[1] == 0x05) {
        Serial1.readBytes(&(TFminiS_data[2]), 3);
        Serial1.printf("%02X %02X %02X %02X %02X\n",
                       TFminiS_data[0], TFminiS_data[1], TFminiS_data[2], TFminiS_data[3], TFminiS_data[4]);
      }
    }
  }  //<END> "if (Serial2.available() >= 9)"



  if (Serial2.available()) {
    String cmd = Serial2.readStringUntil('\n');
    //Serial.printf("S2[%d]:%s", Serial2.available(), cmd);

    if (cmd.indexOf("WB-3000") > -1)  //TANITA series WB-3000
    {
      feedback_weight_kg = read_TANITA(cmd);
      Serial.print("WB-300:");
      Serial.println(feedback_weight_kg);
    }
  }





  /*VS4 server mode*/
  if (VS4server.hasClient()) {
    WiFiClient newClient = VS4server.available();  // listen for incoming clients
    VS4_client = new WiFiClient(newClient);

    Serial.println("VS4 client <" + newClient.remoteIP().toString() + ">");  //"VS4 IPadddress(192.168.10.100)"
  }

  if (VS4_client) {
    if (VS4_client->available()) {
      String msg = VS4_client->readStringUntil('\r');
      Serial.printf("VS4:%s\n",msg.c_str());

      read_SureSignsVS4(msg);
      if(data_collecting == 0x01){SPI_TFT_displayVS4_480x320();}
    }

    if (VS4_client->connected() == false) {
      VS4_client->stop();
      //while (VS4_client->available()) VS4_client->read();
      VS4_client = NULL;
      Serial.println("VS4 is disconnect");
    }
  }  //<END> "if (VS4_client)"




  if ((uwTick - tock_updateDisplay >= 30000) && (TFTupdate_event == 0xFF)) {
    TFTupdate_event = 0x00;

    // data_collecting = 0x00;
    // PatientID = "Oxxxxxxxxxx";
    // person_weight_kg = 999.9;
    // person_height_cm = 999.9;
    // NBP_systolic = 0.0;
    // NBP_diastolic = 0.0;
    // NBP_mean = 0.0;
    // SpO2 = 0.0;
    // HR_pulse = 0.0;
    SPI_TFT_ClearDisplay_480x320();
  }

  if (TFTupdate_event == 0x01) {
    tock_updateDisplay = uwTick;
    TFTupdate_event = 0xFF;

    person_weight_kg = feedback_weight_kg;
    person_height_cm = feedback_height_cm;

    data_collecting |= 0x02;

    SPI_TFT_displayTANITA_480x320();

    Serial.printf("[%s]:%.2fkg %.2fcm\n", PatientID.c_str(), person_weight_kg, person_height_cm);
  } else if (TFTupdate_event == 0x02) {
  }



  //if (data_collecting == 0x03) {
  if (data_collecting != 0x00) {
    if(uwTick - tock_updateHTTP >= 10000) {
      tock_updateHTTP = uwTick;

      post_message = "";

      if (WiFi.status() == WL_CONNECTED) {

        http.begin(host);  //HTTP

        post_message = "{\"username\":\"phai\","
                      "\"key\":\"Mie8Er3ahweinuTaXe9chahdieyu2biev9ap4vieShooph4eif\","
                      "\"DeviceName\":\"BCM00884\","
                      "\"data\": {"
                      "\"visituid\":null,"
                      "\"Weight_kg\":"+ String(person_weight_kg, 2) + ","
                      "\"Height_cm\":"+ String(person_height_cm, 2) + ","
                      "\"Psystolic_mmHg\":"+ String(NBP_systolic) + ","
                      "\"Pdiactolic_mmHg\":"+ String(NBP_diastolic) + ","
                      "\"Pmean_mmHg\":"+ String(NBP_mean) + ","
                      "\"SPO2_percent\":"+ String(SpO2) + ","
                      "\"HR_bpm\":"+ String(HR_pulse) + ","
                      "\"respirations\":null,"
                      "\"temperature\":null,"
                      "\"episodeno\":\""+ PatientID + "\","
                      "\"hardware_brand\":\"Philips\","
                      "\"hardware_model\":\"VS4\","
                      "\"hardware_id\":\""+ SerialNumber + "\"}"
                      "}";
        http.addHeader("Content-Type", "application/json");
        int httpResponseCode = http.POST(post_message);

        Serial.print("http POST:");
        Serial.println(post_message);


        // httpCode will be negative on error
        if (httpResponseCode > 0) {
          // HTTP header has been send and Server response header has been handled
          Serial.printf("[HTTP] GET code: %d\n", httpResponseCode);

          // file found at server
          if (httpResponseCode == HTTP_CODE_OK) {
            String http_payload = http.getString();


            if(data_collecting == 0x01) {
              SPI_TFT_displayVS4_480x320_HTTPCODEOK();
            }
            else if(data_collecting == 0x02) {
              SPI_TFT_displayTANITA_480x320_HTTPCODEOK();
            }
            else if(data_collecting == 0x03) {
              SPI_TFT_displayVS4_480x320_HTTPCODEOK();
              SPI_TFT_displayTANITA_480x320_HTTPCODEOK();
            }


            
            PatientID = "Oxxxxxxxxxx";
            person_weight_kg = 0.0;
            person_height_cm = 0.0;
            NBP_systolic = 0.0;
            NBP_diastolic = 0.0;
            NBP_mean = 0.0;
            SpO2 = 0.0;
            HR_pulse = 0.0;
            data_collecting = 0x00;
            Serial.println(http_payload);
          }
        } 
        else {
          Serial.printf("[HTTP] GET failed, error: % s\n", http.errorToString(httpResponseCode).c_str());
        }


        http.end();
      }
    } 
  }



















   if (Serial.available())
   {
     String cmd = Serial.readStringUntil('\n');
  
     if (cmd.equals("post")) {
       Serial.println(cmd);
       data_collecting = 3;
     }
     else if (cmd.equals("ipconfig")) {
       Serial.println(cmd);
  
       Serial.print("             RSSI: "); Serial.println(WiFi.RSSI());
       Serial.print("local MAC Address: "); Serial.println(WiFi.macAddress());
       Serial.print("local  IP address: "); Serial.println(WiFi.localIP());
     }
     else if (cmd.equals("tare")) {
       Serial.println(cmd);
       if (TFmini_setReferenceHeight_event == 0x00) {
         TFmini_setReferenceHeight();
       }
       else if (TFmini_setReferenceHeight_event == 0x01) {
         TFmini_setReferenceHeight_event = 0x00;
       }
       Serial.println(TFmini_setReferenceHeight_event);
     }
  
  
     /*for TFmini-s*/
     //    if (cmd == "save")
     //    {
     //      uint8_t buff[] = {0x5A, 0x04, 0x11, 0x6F};
     //      TFminiSerial->write(buff, sizeof(buff));
     //
     //      Serial.println("TFmini<=> save ");
     //    }
     //    if (cmd == "dmm")
     //    {
     //      uint8_t buff[] = {0x5A, 0x05, 0x05, 0x06, 0x6A};
     //      TFminiSerial->write(buff, sizeof(buff));
     //
     //      Serial.println("TFmini<=> Standard 9 bytes(mm) ");
     //    }
  
   }





}  //<END> "void loop()"

void SPI_TFT_displayTANITA_480x320() {
  //tft.fillScreen(TFT_BLACK);

  //unit weight text//
  tft.setTextSize(3);
  tft.setTextDatum(BR_DATUM);  //Bottom right
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawString("kg", 480, 150, 4);

  //weight number//
  tft.setTextSize(2);
  tft.setTextDatum(BR_DATUM);  //Bottom right
  tft.setTextColor(TFT_RED, TFT_BLACK);
  tft.drawFloat(person_weight_kg, 1, 350, 170, 7);


  //unit height text//
  tft.setTextSize(3);
  tft.setTextDatum(BR_DATUM);  //Bottom right
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawString("cm", 480, 300, 4);

  //height number//
  tft.setTextSize(2);
  tft.setTextDatum(BR_DATUM);  //Bottom right
  tft.setTextColor(TFT_RED, TFT_BLACK);
  tft.drawFloat(person_height_cm, 1, 350, 300, 7);
}

void SPI_TFT_displayTANITA_480x320_HTTPCODEOK() {
  //tft.fillScreen(TFT_BLACK);

  //unit weight text//
  tft.setTextSize(3);
  tft.setTextDatum(BR_DATUM);  //Bottom right
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawString("kg", 480, 150, 4);

  //weight number//
  tft.setTextSize(2);
  tft.setTextDatum(BR_DATUM);  //Bottom right
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawFloat(person_weight_kg, 1, 350, 170, 7);


  //unit height text//
  tft.setTextSize(3);
  tft.setTextDatum(BR_DATUM);  //Bottom right
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawString("cm", 480, 300, 4);

  //height number//
  tft.setTextSize(2);
  tft.setTextDatum(BR_DATUM);  //Bottom right
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawFloat(person_height_cm, 1, 350, 300, 7);
}


void SPI_TFT_displayVS4_480x320() {
  //tft.fillScreen(TFT_BLACK);

  //PID text//
  tft.setTextSize(2);
  tft.setTextDatum(TL_DATUM);  //Top Left
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawString("PID", 0, 10, 4);

  tft.setTextSize(2);
  tft.setTextDatum(TL_DATUM);  //Top Left
  tft.setTextColor(TFT_RED, TFT_BLACK);
  tft.drawString(PatientID.c_str(), 100, 10, 4);
}

void SPI_TFT_displayVS4_480x320_HTTPCODEOK() {
  //tft.fillScreen(TFT_BLACK);

  //PID text//
  tft.setTextSize(2);
  tft.setTextDatum(TL_DATUM);  //Top Left
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawString("PID", 0, 10, 4);

  tft.setTextSize(2);
  tft.setTextDatum(TL_DATUM);  //Top Left
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawString(PatientID.c_str(), 100, 10, 4);
}



void SPI_TFT_ClearDisplay_480x320() {
  tft.fillScreen(TFT_BLACK);

  //PID text//
  tft.setTextSize(2);
  tft.setTextDatum(TL_DATUM);  //Top Left
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawString("PID", 0, 10, 4);

  tft.setTextSize(2);
  tft.setTextDatum(TL_DATUM);  //Top Left
  tft.setTextColor(TFT_BLACK, TFT_BLACK);
  tft.drawString(PatientID.c_str(), 100, 10, 4);

  //unit weight text//
  tft.setTextSize(3);
  tft.setTextDatum(BR_DATUM);  //Bottom right
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawString("kg", 480, 150, 4);

  //weight number//
  tft.setTextSize(2);
  tft.setTextDatum(BR_DATUM);  //Bottom right
  tft.setTextColor(TFT_BLACK, TFT_BLACK);
  tft.drawFloat(person_weight_kg, 1, 350, 150, 7);


  //unit height text//
  tft.setTextSize(3);
  tft.setTextDatum(BR_DATUM);  //Bottom right
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawString("cm", 480, 300, 4);

  //height number//
  tft.setTextSize(2);
  tft.setTextDatum(BR_DATUM);  //Bottom right
  tft.setTextColor(TFT_BLACK, TFT_BLACK);
  tft.drawFloat(person_height_cm, 1, 350, 300, 7);
}


float read_TANITA(String cmd) {
  float TANITA_weight_kg;
  //?Serial.printf("full command \"%s\"\n", cmd.c_str());
  if (cmd.indexOf("WB-3000") > -1)  //TANITA series WB-3000
  {
    cmd.remove(cmd.length() - 7, 6);
    cmd.remove(0, 24);
    //?Serial.printf("\"%s\"\n", cmd.c_str());

    if (cmd.charAt(0) == 'W') {
      if (cmd.charAt(1) == 'k') {
        cmd.remove(0, 3);
        TANITA_weight_kg = cmd.toFloat();
        TFTupdate_event = 0x01;

        //?Serial.println(person_weight_kg);
      } else if (cmd.charAt(1) == 'p') {
        cmd.remove(0, 3);
        TANITA_weight_kg = cmd.toFloat();
        TANITA_weight_kg = 0.45359237 * TANITA_weight_kg;  //{1.0lb==0.45359237kg}
        TFTupdate_event = 0x01;

        //?Serial.println(person_weight_kg);
      }
    }
  }  //<END> "if (indexOf("WB-3000") > -1)"


  return TANITA_weight_kg;
}//<END> "void read_TANITA(String cmd)"

float read_TFmini(uint8_t msg[]) {
  float TFmini_height_cm, object_height_cm;
  TFmini_height_cm = 0.1 * (msg[2] | msg[3] << 8);
  sensor_height[0] = TFmini_height_cm;  //"{auto update}"

  /*average error = 1.8 cm*/
  object_height_cm = reference_height_cm - TFmini_height_cm - 1.8;


  return object_height_cm;
}


void TFmini_setReferenceHeight(void) {
  TFmini_setReferenceHeight_event = 0x01;
  sum_count = 0;
  sum_total = 0;
}



void read_SureSignsVS4(String msg) {
  //if (msg.substring(0, 3) == "MSH") {
  if (msg.indexOf("MSH") > -1) {
    //debug(msg); //<debug> acknowledgment
    //>>MessageHeader (MSH)<<//
    acknowledge_message_count = 0;

    int16_t index[12];
    index[0] = -1;
    for (uint8_t i = 1; i <= 11; i++) {
      index[i] = msg.indexOf('|', index[i - 1] + 1);
      //Serial.printf("%02d %d=%c\n", i, index[i], msg.charAt(index[i]));
    }

    for (uint8_t i = 1; i <= 11; i++) {
      String sub = msg.substring(index[i - 1] + 1, index[i]);
      //Serial.printf("%02d=%s\n", i, sub.c_str());

      if (i == 7) MessageDateTime = sub;
      else if (i == 10) MessageControl_ID = sub;
    }
  } else if (msg.substring(0, 3) == "PID") {
    //>>Patient Identification (PID)<<//

    int16_t index[5];
    index[0] = -1;
    for (uint8_t i = 1; i <= 4; i++) {
      index[i] = msg.indexOf('|', index[i - 1] + 1);
      //Serial.printf("%02d %d=%c\n", i, index[i], msg.charAt(index[i]));
    }

    for (uint8_t i = 1; i <= 4; i++) {
      String sub = msg.substring(index[i - 1] + 1, index[i]);
      //Serial.printf("%02d=%s\n", i, sub.c_str());

      if (i == 4) vs4PID = sub; //PatientID = sub;
    }
  } else if (msg.substring(0, 3) == "PV1") {
    //>>Patient Visit<<//

    //      int16_t index[20];
    //      index[0] = -1;
    //      for (uint8_t i = 1 ; i <= 19 ; i++) {
    //        index[i] = msg.indexOf('|', index[i - 1] + 1);
    //        //Serial.printf("%02d %d=%c\n", i, index[i], msg.charAt(index[i]));
    //      }
    //
    //      for (uint8_t i = 1 ; i <= 19 ; i++) {
    //        String sub = msg.substring(index[i - 1] + 1, index[i]);
    //        //Serial.printf("%02d=%s\n", i, sub.c_str());
    //      }
  } else if (msg.substring(0, 3) == "ORC") {
    //>>Common Order<<//

    int16_t index[18];
    index[0] = -1;
    for (uint8_t i = 1; i <= 17; i++) {
      index[i] = msg.indexOf('|', index[i - 1] + 1);
      //Serial.printf("%02d %d=%c\n", i, index[i], msg.charAt(index[i]));
    }

    for (uint8_t i = 1; i <= 17; i++) {
      String sub = msg.substring(index[i - 1] + 1, index[i]);
      //Serial.printf("%02d=%s\n", i, sub.c_str());

      if (i == 17) SerialNumber = msg.substring(index[i - 1] + 3, msg.length());
    }
  } else if (msg.substring(0, 3) == "OBR") {
    //>>Observation Request<<//

    int16_t index[10];
    index[0] = -1;
    for (uint8_t i = 1; i <= 9; i++) {
      index[i] = msg.indexOf('|', index[i - 1] + 1);
      //Serial.printf("%02d %d=%c\n", i, index[i], msg.charAt(index[i]));
    }

    for (uint8_t i = 1; i <= 9; i++) {
      String sub = msg.substring(index[i - 1] + 1, index[i]);
      //Serial.printf("%02d=%s\n", i, sub.c_str());

      if (i == 8) MeasurementDateTime = sub;
    }
  } else if (msg.substring(0, 3) == "OBX") {
    //>>>Observation Result<<//
    acknowledge_message_count++;

    int16_t index[10];
    index[0] = -1;
    for (uint8_t i = 1; i <= 9; i++) {
      index[i] = msg.indexOf('|', index[i - 1] + 1);
      //Serial.printf("%02d %d=%c\n", i, index[i], msg.charAt(index[i]));
    }

    uint8_t* value;
    for (uint8_t i = 1; i <= 9; i++) {
      String sub = msg.substring(index[i - 1] + 1, index[i]);
      //Serial.printf("%02d=%s\n", i, sub.c_str());

      if (i == 4) {
        if (sub == "0002-4bb8^SpO2^MDIL") value = &SpO2;
        else if (sub == "0002-4a05^NBPs^MDIL") value = &NBP_systolic;
        else if (sub == "0002-4a06^NBPd^MDIL") value = &NBP_diastolic;
        else if (sub == "0002-4a07^NBPm^MDIL") value = &NBP_mean;
        else if (sub == "0002-4182^HR_Pulse^MDIL") value = &HR_pulse;
      } else if (i == 6) {
        *value = sub.toInt();
      }
    }

    //    if (acknowledge_message_count == 5) {
    //      VS4_client->printf("MSH|^~\\&|||||%s||ACK^^ACK_ALL|%s|P|2.4\r",
    //                         MessageDateTime.c_str(), PatientID.c_str());
    //      VS4_client->printf("MSA|%s|%s\r", ACKCode_Accept,  MessageControl_ID.c_str());
    //    }
  }


  if (acknowledge_message_count == 5) {
    //Serial.println(MessageDateTime.substring(0, 4)); //YYYY
    //Serial.println(MessageDateTime.substring(4, 6)); //MM
    //Serial.println(MessageDateTime.substring(6, 8)); //DD
    //Serial.println(MessageDateTime.substring(8, 10)); //hh
    //Serial.println(MessageDateTime.substring(10, 12)); //mm
    //Serial.println(MessageDateTime.substring(12, 14)); //ss

    /* ACKCode
      //    String time, AcknowledgmentDateTime;
      //    uint8_t hh, mm, ss;
      //
      //    time = MessageDateTime.substring(8, 10);
      //    hh = time.toInt();
      //    time = MessageDateTime.substring(10, 12);
      //    mm = time.toInt();
      //    time = MessageDateTime.substring(12, 14);
      //    ss = time.toInt();
      //
      //    mm = mm + 1;
      //    AcknowledgmentDateTime = MessageDateTime.substring(0, 8) +
      //                             String(hh) +
      //                             String(mm) +
      //                             String(ss);
      ACKCode */

    VS4_client->printf("MSH|^~\\&|||||%s||ACK^^ACK_ALL|%s|P|2.4\r", MessageDateTime.c_str(), "BDMS_IOT");
    VS4_client->printf("MSA|%s|%s\r", ACKCode_Accept, MessageControl_ID.c_str());

    //Serial.printf("MSH|^~\\&|||||%s||ACK^^ACK_ALL|%s|P|2.4\n",MessageDateTime.c_str(), "BDMS_IOT");
    //Serial.printf("MSA|%s|%s\n", ACKCode_Accept,  MessageControl_ID.c_str());
    
    PatientID = vs4PID;
    data_collecting |= 0x01;  //Complete receive "VS4" Data
    acknowledge_message_count = 0;

    Serial.printf("    MessageDateTime = %s\n", MessageDateTime.c_str());
    Serial.printf("      Serial number = %s\n", SerialNumber.c_str());
    Serial.printf("          PatientID = %s\n", PatientID.c_str());
    Serial.printf("MeasurementDateTime = %s\n", MeasurementDateTime.c_str());
    Serial.printf("            SpO2(%%) = %d\n", SpO2);
    Serial.printf("         NBPs(mmHg) = %d\n", NBP_systolic);
    Serial.printf("         NBPd(mmHg) = %d\n", NBP_diastolic);
    Serial.printf("         NBPm(mmHg) = %d\n", NBP_mean);
    Serial.printf("      HR_Pulse(bpm) = %d\n", HR_pulse);

    //Serial.println(F("ACKCode = AA(Accept)"));
  }
}





void get_network_info() {
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("[*] Network information for ");
    Serial.println(ssid);

    Serial.println("[+] BSSID : " + WiFi.BSSIDstr());
    Serial.print("[+] Gateway IP : ");
    Serial.println(WiFi.gatewayIP());
    Serial.print("[+] Subnet Mask : ");
    Serial.println(WiFi.subnetMask());
    Serial.println((String) "[+] RSSI : " + WiFi.RSSI() + " dB");
    Serial.print("[+] ESP32 IP : ");
    Serial.println(WiFi.localIP());
  }
}
