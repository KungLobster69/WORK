#include <lvgl.h>
#include <TFT_eSPI.h>
#include "ui.h"

// กำหนดค่าขนาดหน้าจอ
#define SCREEN_WIDTH  320
#define SCREEN_HEIGHT 240
#define DRAW_BUF_SIZE (SCREEN_WIDTH * SCREEN_HEIGHT / 10 * (LV_COLOR_DEPTH / 8))

TFT_eSPI tft = TFT_eSPI();  // สร้างอ็อบเจ็กต์จอ TFT
uint8_t *draw_buf;
uint32_t lastTick = 0;

// ฟังก์ชันแสดง log ข้อความสำหรับ debug
void log_print(lv_log_level_t level, const char * buf) {
  LV_UNUSED(level);
  Serial.println(buf);
  Serial.flush();
}

void update_UI() {
  lv_tick_inc(millis() - lastTick);
  lastTick = millis();
  lv_timer_handler();
}

void setup() {
  Serial.begin(115200);
  delay(3000);

  Serial.println("Initializing LVGL...");
  lv_init();
  lv_log_register_print_cb(log_print);

  Serial.println("Initializing TFT Display...");
  tft.init();  // ✅ ใช้ tft.init() แต่ไม่ใช้ tft.setRotation()

  Serial.println("Setting up LVGL Display...");
  draw_buf = new uint8_t[DRAW_BUF_SIZE];
  lv_display_t * disp = lv_tft_espi_create(SCREEN_HEIGHT, SCREEN_WIDTH, draw_buf, DRAW_BUF_SIZE);
  
  // ✅ หมุนจอผ่าน LVGL
  lv_display_set_rotation(disp, LV_DISPLAY_ROTATION_270);

  Serial.println("LVGL Initialized.");

  // เรียกใช้งาน UI จาก EEZ Studio
  ui_init();
}

void loop() {
  update_UI();
  delay(1);
}
