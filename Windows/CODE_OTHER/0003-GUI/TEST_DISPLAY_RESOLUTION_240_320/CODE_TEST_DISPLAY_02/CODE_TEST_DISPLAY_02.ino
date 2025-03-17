//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 02_Test_and_Setup_DS3231_RTC_Module
//----------------------------------------Including Libraries.
#include "RTClib.h"
//----------------------------------------

char daysOfTheWeek[8][10] = {"SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "ERROR"};

String inputString = "";  // a String to hold incoming data.
bool stringComplete = false;  // whether the string is complete.

int d_year;
byte d_month, d_day, daysOfTheWeek_Val;
byte t_hour, t_minute, t_second;

unsigned long prevMill_Update_DateTime = 0;
const long interval_Update_DateTime = 1000;

RTC_DS3231 rtc;




//________________________________________________________________________________ VOID SETUP()
void setup() {
  // put your setup code here, to run once:

  delay(2000);
  Serial.begin(115200);

  // reserve 200 bytes for the inputString.
  inputString.reserve(200);

  //----------------------------------------Starting and setting up the DS3231 RTC module.
  Serial.println();
  Serial.println("------------");
  Serial.println("Starting the DS3231 RTC module.");
  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }
  Serial.println("Successfully started the DS3231 RTC module.");
  Serial.println("------------");
  Serial.println();
  //----------------------------------------

  //----------------------------------------
  Serial.println();
  Serial.println("------------");
  Serial.println("Serial monitor settings :");
  Serial.println("- End Char  : Newline");
  Serial.println("- Baud Rate : 115200");
  Serial.println("------------");
  Serial.println();
  //----------------------------------------

  Serial.println();
  Serial.println("------------");
  Serial.println("Example command to set the time and date on the RTC module : ");
  Serial.println("SET,2024,7,9,12,3,0");
  Serial.println();
  Serial.println("SET = command to set.");
  Serial.println("2024 = Year.");
  Serial.println("7 = Month.");
  Serial.println("9=Day.");
  Serial.println("12 = Hour.");
  Serial.println("3 = Minute.");
  Serial.println("0 = Second.");
  Serial.println("------------");
  Serial.println();

  delay(3000);
}
//________________________________________________________________________________ 




//________________________________________________________________________________ VOID LOOP()
void loop() {
  // put your main code here, to run repeatedly:

  serialEvent();

  unsigned long currentMillis_Update_DateTime = millis();
  if (currentMillis_Update_DateTime - prevMill_Update_DateTime >= interval_Update_DateTime) {
    prevMill_Update_DateTime = currentMillis_Update_DateTime;

    get_DateTime();
  }

  // print the string when a newline arrives.
  if (stringComplete) {
    Serial.print("Input String : ");
    Serial.println(inputString);

    String command = "";
    command = getValue(inputString, ',', 0);

    if (command == "SET") {
      Serial.println();
      Serial.println("------------");
      Serial.println("Set the Time and Date of the DS3231 RTC Module.");
      Serial.println("Incoming settings data : ");
      
      d_year = getValue(inputString, ',', 1).toInt();
      d_month = getValue(inputString, ',', 2).toInt();
      d_day = getValue(inputString, ',', 3).toInt();
      t_hour = getValue(inputString, ',', 4).toInt();
      t_minute = getValue(inputString, ',',5).toInt();
      t_second = getValue(inputString, ',', 6).toInt();

      Serial.print("- Year : ");Serial.println(d_year);
      Serial.print("- Month : ");Serial.println(d_month);
      Serial.print("- Day : ");Serial.println(d_day);
      Serial.print("- Hour : ");Serial.println(t_hour);
      Serial.print("- Minute : ");Serial.println(t_minute);
      Serial.print("- Second : ");Serial.println(t_second);
      
      Serial.println("Set Time and Date...");
      rtc.adjust(DateTime(d_year, d_month, d_day, t_hour, t_minute, t_second));

      Serial.println("Setting the Time and Date has been completed.");
      Serial.println("------------");
      Serial.println();
    }
    
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}
//________________________________________________________________________________ 




//________________________________________________________________________________ serialEvent()
void serialEvent() {
  while (Serial.available()) {
    // get the new byte.
    char inChar = (char)Serial.read();

    // if the incoming character is a newline, set a flag so the main loop can do something about it.
    if (inChar == '\n') {
      stringComplete = true;
      return;
    }
    
    // add it to the inputString.
    inputString += inChar;
  }
}
//________________________________________________________________________________ 




//________________________________________________________________________________ getValue()
// String function to process the data received
// I got this from : https://www.electroniclinic.com/reyax-lora-based-multiple-sensors-monitoring-using-arduino/
String getValue(String data, char separator, int index) {
  int found = 0;
  int strIndex[] = { 0, -1 };
  int maxIndex = data.length() - 1;
  
  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
//________________________________________________________________________________ 




//________________________________________________________________________________ get_DateTime()
void get_DateTime() {
  DateTime now = rtc.now();

  d_year = now.year();
  d_month = now.month();
  d_day = now.day();
  daysOfTheWeek_Val = now.dayOfTheWeek();
  if (daysOfTheWeek_Val > 7 || daysOfTheWeek_Val < 0) daysOfTheWeek_Val = 7;
  t_hour = now.hour();
  t_minute = now.minute();
  t_second = now.second();

  char full_DateTime[60];
  sprintf(full_DateTime, "%s | %02d-%02d-%d | Time : %02d:%02d:%02d", daysOfTheWeek[daysOfTheWeek_Val], d_day, d_month, d_year, t_hour, t_minute, t_second);

  Serial.print("Date : ");
  Serial.println(full_DateTime);
}
//________________________________________________________________________________ 
//<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<