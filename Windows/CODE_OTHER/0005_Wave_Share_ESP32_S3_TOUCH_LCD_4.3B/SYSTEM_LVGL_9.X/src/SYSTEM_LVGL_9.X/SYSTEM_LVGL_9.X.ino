#include "conf_lcd.h"
#include <lvgl.h>

extern LCD *active_lcd;

void lvgl_flush_cb(lv_display_t *disp, const lv_area_t *area, uint8_t *color_p)
{
  if (active_lcd) {
    active_lcd->drawBitmap(
        area->x1,
        area->y1,
        area->x2 - area->x1 + 1,
        area->y2 - area->y1 + 1,
        reinterpret_cast<const uint8_t *>(color_p)
    );
  }
  lv_disp_flush_ready(disp);
}

void setup() {
  Serial.begin(115200);
  Serial.println("LVGL 9.2.2 RGB LCD example start");

  conf_lcd_init();
  lv_init();

  uint32_t hor_res = EXAMPLE_LCD_WIDTH;
  uint32_t ver_res = EXAMPLE_LCD_HEIGHT;
  uint32_t stride = hor_res * sizeof(lv_color16_t);
  uint32_t buf_pixels = hor_res * 40;
  uint32_t buf_size = buf_pixels * sizeof(lv_color16_t);

  static lv_color_t *buf1 = (lv_color_t *)heap_caps_malloc(buf_size, MALLOC_CAP_DMA);
  static lv_draw_buf_t draw_buf;
  lv_draw_buf_init(&draw_buf, hor_res, 40, LV_COLOR_FORMAT_RGB565, stride, buf1, buf_size);

  static lv_display_t *disp = lv_display_create(hor_res, ver_res);
  lv_display_set_flush_cb(disp, lvgl_flush_cb);
  lv_display_set_draw_buffers(disp, &draw_buf, nullptr);  // single buffer

  lv_obj_t *label = lv_label_create(lv_screen_active());
  lv_label_set_text(label, "Hello LVGL 9.2.2!");
  lv_obj_center(label);

  Serial.println("LVGL initialized and label created.");
}

void loop() {
  lv_timer_handler();
  delay(5);
}
