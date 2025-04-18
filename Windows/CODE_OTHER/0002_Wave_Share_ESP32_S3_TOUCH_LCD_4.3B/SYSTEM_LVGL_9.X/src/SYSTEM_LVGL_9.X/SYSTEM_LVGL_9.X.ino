#include <lvgl.h>
#include "ui.h"
#include "images.h"
#include <conf_lcd.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <time.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ===================== Global Configuration =====================

// WiFi credentials
const char* ssid = "Kampanat_2.4GHz";
const char* password = "0992719317";

// OpenWeatherMap API
const char* api_key = "aaa13c64bf47cc336c2437303e00684a";
String current_city = "Detecting...";

// ใช้ sensor จริงหรือไม่ (true = ใช้ sensor จริง, false = ใช้ข้อมูลจาก API)
bool useSensorData = false;

// WiFi reconnect timer
static unsigned long last_wifi_check = 0;

// ===================== Sensor Functions =====================

// mock sensor temperature (สามารถเปลี่ยนเป็น sensor จริงได้)
float read_sensor_temperature() {
  return 26.7;
}

// mock sensor humidity (สามารถเปลี่ยนเป็น sensor จริงได้)
float read_sensor_humidity() {
  return 58.5;
}

// ===================== UI Setup =====================

// แสดงค่าเริ่มต้นของ label ทั้งหมดบนหน้าจอ
void set_initial_display_of_labels() {
  lv_label_set_text(objects.label_city, "Detecting...");
  lv_label_set_text(objects.label_date, "--, ----");
  lv_label_set_text(objects.label_time, "--:--:--");
  lv_label_set_text(objects.label_temperature, "--.-- °C");
  lv_label_set_text(objects.label_temp_max, "--.-- °C");
  lv_label_set_text(objects.label_temp_min, "--.-- °C");
  lv_label_set_text(objects.label_humidity, "--%");
  lv_label_set_text(objects.label_wind, "-- km/h");
  lv_label_set_text(objects.label_pressure, "-- hPa");
  lv_label_set_text(objects.label_info, "--");
}

// ===================== WiFi =====================

// เชื่อมต่อ WiFi โดยใช้ ssid และ password
void connect_to_wifi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  int attempt = 0;
  while (WiFi.status() != WL_CONNECTED && attempt < 20) {
    delay(500);
    Serial.print(".");
    attempt++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n❌ Failed to connect to WiFi.");
  }
}

// ===================== NTP Time Sync =====================

// ตั้งค่า timezone และ sync เวลาจาก NTP server
void setup_time() {
  configTime(7 * 3600, 0, "pool.ntp.org", "time.nist.gov");
  Serial.print("Waiting for NTP time sync");
  struct tm timeinfo;
  while (!getLocalTime(&timeinfo)) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\n⏰ Time synchronized via NTP.");
}

// ===================== Get City From IP =====================

// ดึงข้อมูลเมืองจาก IP ด้วย API สำรอง
void get_city_from_ip() {
  if (WiFi.status() != WL_CONNECTED) return;
  HTTPClient http;
  http.begin("http://ip-api.com/json");
  int httpCode = http.GET();
  if (httpCode == 200) {
    String payload = http.getString();
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, payload);
    const char* city = doc["city"];
    const char* country = doc["country"];
    if (city && country) {
      current_city = String(city) + ", " + String(country);
      Serial.println("🌐 City Detected: " + current_city);
    }
  } else {
    Serial.println("⚠️ Failed to get IP info");
  }
  http.end();
}

// ===================== Weather API =====================

// ดึงข้อมูลอากาศจาก OpenWeatherMap
void fetch_weather_data() {
  if (WiFi.status() != WL_CONNECTED) return;
  WiFiClientSecure client;
  client.setInsecure();
  HTTPClient http;
  String city = "Chiang+Mai";
  String weather_api_url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + ",TH&units=metric&appid=" + String(api_key);
  http.begin(client, weather_api_url);
  int httpCode = http.GET();
  struct tm timeinfo;
  getLocalTime(&timeinfo);

  if (httpCode == 200) {
    String payload = http.getString();
    Serial.println(payload);
    DynamicJsonDocument doc(2048);
    DeserializationError error = deserializeJson(doc, payload);
    if (error) {
      Serial.println("❌ JSON parse failed!");
      return;
    }
    float temp = doc["main"]["temp"];
    float temp_min = doc["main"]["temp_min"];
    float temp_max = doc["main"]["temp_max"];
    float wind = doc["wind"]["speed"];
    int pressure = doc["main"]["pressure"];
    const char* city_name = doc["name"];
    const char* country = doc["sys"]["country"];
    const char* weather_main = doc["weather"][0]["main"];
    const char* weather_desc = doc["weather"][0]["description"];
    const char* weather_icon = doc["weather"][0]["icon"];

    char buf[32];
    if (useSensorData) {
      float t = read_sensor_temperature();
      sprintf(buf, "%.1f°C", t);
      lv_label_set_text(objects.label_temperature, buf);
    } else {
      sprintf(buf, "%.1f°C", temp);
      lv_label_set_text(objects.label_temperature, buf);
    }

    if (useSensorData) {
      float h = read_sensor_humidity();
      sprintf(buf, "%.0f%%", h);
      lv_label_set_text(objects.label_humidity, buf);
    } else {
      int humidity = doc["main"]["humidity"];
      sprintf(buf, "%d%%", humidity);
      lv_label_set_text(objects.label_humidity, buf);
    }

    sprintf(buf, "%.1f°C", temp_max);
    lv_label_set_text(objects.label_temp_max, buf);
    sprintf(buf, "%.1f°C", temp_min);
    lv_label_set_text(objects.label_temp_min, buf);
    sprintf(buf, "%.1f km/h", wind);
    lv_label_set_text(objects.label_wind, buf);
    sprintf(buf, "%d hPa", pressure);
    lv_label_set_text(objects.label_pressure, buf);

    if (city_name && country) {
      current_city = String(city_name) + ", " + String(country);
    }

    if (weather_main) lv_label_set_text(objects.label_weather_main, weather_main);
    if (weather_desc) lv_label_set_text(objects.label_weather_description, weather_desc);

    String icon = String(weather_icon);
    if (icon == "01d") lv_img_set_src(objects.image_icon_weather, &img_icon_label_01d);
    else if (icon == "01n") lv_img_set_src(objects.image_icon_weather, &img_icon_label_01n);
    else if (icon == "02d") lv_img_set_src(objects.image_icon_weather, &img_icon_label_02d);
    else if (icon == "02n") lv_img_set_src(objects.image_icon_weather, &img_icon_label_02n);
    else if (icon == "03d" || icon == "03n") lv_img_set_src(objects.image_icon_weather, &img_icon_label_03d);
    else if (icon == "04d" || icon == "04n") lv_img_set_src(objects.image_icon_weather, &img_icon_label_04d);
    else if (icon == "09d" || icon == "09n") lv_img_set_src(objects.image_icon_weather, &img_icon_label_09d);
    else if (icon == "10d") lv_img_set_src(objects.image_icon_weather, &img_icon_label_10d);
    else if (icon == "10n") lv_img_set_src(objects.image_icon_weather, &img_icon_label_10n);
    else if (icon == "11d" || icon == "11n") lv_img_set_src(objects.image_icon_weather, &img_icon_label_11d);
    else if (icon == "13d" || icon == "13n") lv_img_set_src(objects.image_icon_weather, &img_icon_label_13d);
    else if (icon == "50d" || icon == "50n") lv_img_set_src(objects.image_icon_weather, &img_icon_label_50d);

    const char* weekday_full_en[] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
    const char* month_short_en[] = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};
    sprintf(buf, "%s, %02d-%s-%04d", weekday_full_en[timeinfo.tm_wday], timeinfo.tm_mday, month_short_en[timeinfo.tm_mon], timeinfo.tm_year + 1900);
    lv_label_set_text(objects.label_date, buf);

    char info_buf[64];
    sprintf(info_buf, "Last Data Update : %02d:%02d:%02d (Succeed)", timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec);
    lv_label_set_text(objects.label_info, info_buf);
  } else {
    Serial.printf("❌ Failed to get weather data. HTTP Code: %d\n", httpCode);
    char info_buf[64];
    sprintf(info_buf, "Last Data Update : %02d:%02d:%02d (Failed)", timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec);
    lv_label_set_text(objects.label_info, info_buf);
  }
  http.end();
}

// ===================== Weather Timer =====================

// ฟังก์ชันนี้จะเรียกทุกวินาที เพื่ออัปเดตเวลาปัจจุบัน และดึงอากาศทุก 10 นาที
void update_weather_ui(lv_timer_t* timer) {
  char buf[32];
  struct tm timeinfo;
  if (getLocalTime(&timeinfo)) {
    sprintf(buf, "%02d:%02d:%02d", timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec);
    lv_label_set_text(objects.label_time, buf);
  }
  lv_label_set_text(objects.label_city, current_city.c_str());
  static unsigned long last_weather_update = 0;
  if (millis() - last_weather_update > 600000) {
    fetch_weather_data();
    last_weather_update = millis();
  }
}

// ===================== Setup =====================

// ฟังก์ชัน setup เรียกตอนเริ่มต้นเพื่อเตรียมทุกอย่าง
void setup() {
  Serial.begin(115200);
  connect_to_wifi();
  conf_lcd_init();
  lv_init();
  lv_display_t* disp = lv_display_create(EXAMPLE_LCD_WIDTH, EXAMPLE_LCD_HEIGHT);
  static lv_color_t* buf1 = (lv_color_t*)heap_caps_malloc(sizeof(lv_color_t) * EXAMPLE_LCD_WIDTH * 40, MALLOC_CAP_DMA);
  static lv_draw_buf_t draw_buf;
  lv_draw_buf_init(&draw_buf, EXAMPLE_LCD_WIDTH, 40, LV_COLOR_FORMAT_RGB565,
                   EXAMPLE_LCD_WIDTH * sizeof(lv_color_t), buf1,
                   sizeof(lv_color_t) * EXAMPLE_LCD_WIDTH * 40);
  lv_display_set_draw_buffers(disp, &draw_buf, NULL);
  lv_display_set_flush_cb(disp, [](lv_display_t* disp, const lv_area_t* area, uint8_t* px_map) {
    active_lcd->drawBitmap(area->x1, area->y1,
                           area->x2 - area->x1 + 1,
                           area->y2 - area->y1 + 1,
                           px_map);
    lv_display_flush_ready(disp);
  });
  lv_display_set_rotation(disp, LV_DISPLAY_ROTATION_0);
  ui_init();
  set_initial_display_of_labels();
  setup_time();
  get_city_from_ip();
  fetch_weather_data();
  lv_timer_create(update_weather_ui, 1000, NULL);
}

// ===================== Main Loop =====================

// ฟังก์ชัน loop ทำงานต่อเนื่องและตรวจสอบ WiFi เป็นระยะ
void loop() {
  unsigned long now = millis();
  if (now - last_wifi_check > 10000) {
    if (WiFi.status() != WL_CONNECTED) {
      connect_to_wifi();
      setup_time();
      get_city_from_ip();
      fetch_weather_data();
    }
    last_wifi_check = now;
  }
  static unsigned long last = 0;
  lv_tick_inc(now - last);
  last = now;
  lv_timer_handler();
  delay(5);
}