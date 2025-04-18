#include <lvgl.h>
#include "ui.h"
#include <conf_lcd.h>

int temperature = 25;
int humidity = 60;
float wind = 5.0;
int pressure = 1010;

void update_weather_ui(lv_timer_t* timer) {
  char buf[32];

  // Mock weather update
  static int temperature = 25;
  static int humidity = 60;
  static float wind = 5.0;
  static int pressure = 1010;

  temperature++;
  if (temperature > 35) temperature = 25;

  humidity += 3;
  if (humidity > 100) humidity = 60;

  wind += 0.4;
  if (wind > 15.0) wind = 4.0;

  pressure += 1;
  if (pressure > 1020) pressure = 1010;

  // Temperature
  sprintf(buf, "%d°C", temperature);
  lv_label_set_text(objects.label_temperature, buf);

  sprintf(buf, "%d°C", temperature + 2);
  lv_label_set_text(objects.label_temp_max, buf);

  sprintf(buf, "%d°C", temperature - 2);
  lv_label_set_text(objects.label_temp_min, buf);

  // Humidity
  sprintf(buf, "%d%%", humidity);
  lv_label_set_text(objects.label_humidity, buf);

  // Wind
  sprintf(buf, "%.1f km/h", wind);
  lv_label_set_text(objects.label_wind, buf);

  // Pressure
  sprintf(buf, "%d hPa", pressure);
  lv_label_set_text(objects.label_pressure, buf);

  // Info
  sprintf(buf, "Updated at %lu", millis() / 1000);
  lv_label_set_text(objects.label_info, buf);

  // ✅ Time (hh:mm:ss)
  unsigned long seconds = millis() / 1000;
  int hours = (seconds / 3600) % 24;
  int minutes = (seconds / 60) % 60;
  int secs = seconds % 60;
  sprintf(buf, "%02d:%02d:%02d", hours, minutes, secs);
  lv_label_set_text(objects.label_time, buf);

  // ✅ Date (Friday, 18-Apr-2025)
  int days_since_start = seconds / 86400;

  // Starting date: Friday, 18-Apr-2025
  int base_day = 18;
  int base_month = 4;
  int base_year = 2025;
  int base_weekday = 5;  // 0=Sunday, ..., 5=Friday

  int day = base_day + days_since_start;
  int month = base_month;
  int year = base_year;
  int weekday = (base_weekday + days_since_start) % 7;

  // Adjust day/month/year (simple logic: 30 days/month)
  while (day > 30) {
    day -= 30;
    month++;
    if (month > 12) {
      month = 1;
      year++;
    }
  }

  // Full weekday & short month names
  const char* weekday_full_en[] = {
    "Sunday", "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday"
  };

  const char* month_short_en[] = {
    "", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  };

  sprintf(buf, "%s, %02d-%s-%04d", weekday_full_en[weekday], day, month_short_en[month], year);
  lv_label_set_text(objects.label_date, buf);

  // Label: label_city
  lv_label_set_text(objects.label_city, "Chiang Mai, Thailand");
}

void setup() {
  Serial.begin(115200);
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

  // Timer อัปเดตค่า mock ทุก 2 วินาที
  lv_timer_create(update_weather_ui, 1000, NULL);
}

void loop() {
  static unsigned long last = 0;
  unsigned long now = millis();
  lv_tick_inc(now - last);
  last = now;

  lv_timer_handler();
  delay(5);
}