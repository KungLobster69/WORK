#include <lvgl.h>
#include "waveshare_lcd_port.h"
#include "lvgl_port.h"
#include "ui.h"  // <<== เพิ่ม header ของ EEZ UI

void setup() {
  waveshare_lcd_init();     // เริ่มจอ LCD
  lvgl_port_init();         // เริ่มระบบ LVGL

  ui_init();                // <<== ใช้ UI จาก EEZ Studio แทน
}

void loop() {
  lv_timer_handler();       // ประมวลผล UI
  delay(5);
}
