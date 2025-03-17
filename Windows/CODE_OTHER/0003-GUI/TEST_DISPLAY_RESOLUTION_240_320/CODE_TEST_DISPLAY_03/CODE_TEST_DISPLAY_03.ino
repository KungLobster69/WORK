//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 03_Test_OpenWeatherMap_API
//----------------------------------------Including the libraries.
#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>
//----------------------------------------

//----------------------------------------SSID and PASSWORD of your WiFi network.
const char* ssid = "YOUR_WIFI_SSID";  //--> Your wifi name
const char* password = "YOUR_WIFI_PASSWORD"; //--> Your wifi password
//----------------------------------------

//----------------------------------------Your OpenWeatherMap API.
// Example:
// String openWeatherMapApiKey = "bd939aa3d23ff33d3c8f5dd1dd435";
String openWeatherMapApiKey = "REPLACE_WITH_YOUR_OPEN_WEATHER_MAP_API_KEY";

// Replace with your country code and city.
// Find city and country code here : https://openweathermap.org/
String city = "Chiang Mai";
String countryCode = "TH";
//----------------------------------------

String str_Weather_Main, str_Weather_Icon, str_Weather_Description;
String str_Temperature, str_Feels_Like, str_Temp_Max, str_Temp_Min;
String str_Humidity, str_Wind_Speed, str_Pressure, str_Visibility;

String jsonBuffer;



//________________________________________________________________________________ connecting_To_WiFi()
void connecting_To_WiFi() {
  //----------------------------------------Set Wifi to STA mode.
  Serial.println();
  Serial.println("-------------WIFI mode");
  Serial.println("WIFI mode : STA");
  WiFi.mode(WIFI_STA);
  Serial.println("-------------");
  delay(1000);
  //---------------------------------------- 

  //----------------------------------------Connect to Wi-Fi (STA).
  Serial.println();
  Serial.println("-------------Connection");
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  
  //:::::::::::::::::: The process of connecting ESP32 with WiFi Hotspot / WiFi Router.
  // The process timeout of connecting ESP32 with WiFi Hotspot / WiFi Router is 20 seconds.
  // If within 20 seconds the ESP32 has not been successfully connected to WiFi, the ESP32 will restart.
  // I made this condition because on my ESP32, there are times when it seems like it can't connect to WiFi, so it needs to be restarted to be able to connect to WiFi.
  
  int connecting_process_timed_out = 20; //--> 20 = 20 seconds.
  connecting_process_timed_out = connecting_process_timed_out * 2;
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
    if(connecting_process_timed_out > 0) connecting_process_timed_out--;
    if(connecting_process_timed_out == 0) {
      Serial.println();
      Serial.println("Failed to connect to WiFi. The ESP32 will be restarted.");
      Serial.println("-------------");
      delay(1000);
      ESP.restart();
    }
  }
  
  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("Successfully connected to : ");
  Serial.println(ssid);
  Serial.println("-------------");
  //:::::::::::::::::: 
  delay(1000);
  //---------------------------------------- 
}
//________________________________________________________________________________ 



//________________________________________________________________________________ get_Data_from_OpenWeatherMap()
void get_Data_from_OpenWeatherMap() {
  Serial.println();
  Serial.println("-------------");
  Serial.println("Getting Weather Data from OpenWeatherMap.");
  Serial.println("Please wait...");
  
  // Check WiFi connection status.
  if(WiFi.status()== WL_CONNECTED){
    String serverPath = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "," + countryCode + "&units=metric&APPID=" + openWeatherMapApiKey;
    
    jsonBuffer = httpGETRequest(serverPath.c_str());
    Serial.println();
    Serial.println("Weather Data in JSON form :");
    Serial.println(jsonBuffer);
    JSONVar myObject = JSON.parse(jsonBuffer);

    // JSON.typeof(jsonVar) can be used to get the type of the var.
    if (JSON.typeof(myObject) == "undefined") {
      Serial.println("Parsing input failed!");
      return;
    }

    Serial.println();
    Serial.println("Weather Data taken");

    str_Weather_Main = JSON.stringify(myObject["weather"][0]["main"]);
    str_Weather_Main.replace("\"", ""); //--> Removes the Double quotes (") character in the string.
    str_Weather_Icon = JSON.stringify(myObject["weather"][0]["icon"]);
    str_Weather_Icon.replace("\"", "");
    str_Weather_Description = JSON.stringify(myObject["weather"][0]["description"]);
    str_Weather_Description.replace("\"", "");
    
    str_Temperature = JSON.stringify(myObject["main"]["temp"]);
    str_Feels_Like = JSON.stringify(myObject["main"]["feels_like"]);
    str_Temp_Max = JSON.stringify(myObject["main"]["temp_max"]);
    str_Temp_Min = JSON.stringify(myObject["main"]["temp_min"]);
    
    str_Humidity = JSON.stringify(myObject["main"]["humidity"]);
    str_Wind_Speed = JSON.stringify(myObject["wind"]["speed"]);
    str_Pressure = JSON.stringify(myObject["main"]["pressure"]);
    str_Visibility = JSON.stringify(myObject["visibility"]);

    Serial.println();
    Serial.print("Weather Main : ");Serial.println(str_Weather_Main);
    Serial.print("Weather Icon : ");Serial.println(str_Weather_Icon);
    Serial.print("Weather Description : ");Serial.println(str_Weather_Description);
    
    Serial.print("Temperature : ");Serial.print(str_Temperature);Serial.println(" °C");
    Serial.print("Feels Like : ");Serial.print(str_Feels_Like);Serial.println(" °C");
    Serial.print("Temp Max : ");Serial.print(str_Temp_Max);Serial.println(" °C");
    Serial.print("Temp Min : ");Serial.print(str_Temp_Min);Serial.println(" °C");
    
    Serial.print("Humidity : ");Serial.print(str_Humidity);Serial.println(" %");
    Serial.print("Wind Speed : ");Serial.print(str_Wind_Speed);Serial.println(" m/s");
    Serial.print("Pressure : ");Serial.print(str_Pressure);Serial.println(" hPa");
    Serial.print("Visibility : ");Serial.print(str_Visibility);Serial.println(" m");

    Serial.println("-------------");
    Serial.println();
  }
  else {
    Serial.println("WiFi Disconnected");
    Serial.println("-------------");
    Serial.println();
  }
}
//________________________________________________________________________________



//________________________________________________________________________________ httpGETRequest()
String httpGETRequest(const char* serverName) {
  WiFiClient client;
  HTTPClient http;
    
  // Your Domain name with URL path or IP address with path.
  http.begin(client, serverName);
  
  // Send HTTP POST request.
  int httpResponseCode = http.GET();
  
  String payload = "{}"; 
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  
  // Free resources.
  http.end();

  return payload;
}
//________________________________________________________________________________ 



//________________________________________________________________________________ VOID SETUP()
void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
  Serial.println();
  delay(3000);

  connecting_To_WiFi();
  delay(500);

  get_Data_from_OpenWeatherMap();
  delay(500);
}
//________________________________________________________________________________ 



//________________________________________________________________________________ VOID LOOP()
void loop() {
  // put your main code here, to run repeatedly:

  delay(1000);
}
//________________________________________________________________________________ 
//<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<