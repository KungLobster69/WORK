#include "lvgl.h" 
#include "waveshare_lcd_port.h"

// == Global LVGL objects ==
static lv_display_t *disp;
static lv_color_t *draw_buf;
static lv_display_draw_buf_t disp_buf;

// == Flush callback: เชื่อมกับ lcd->drawBitmap() ของ Waveshare ==
extern LCD *lcd; // <-- ต้องกำหนด extern จาก waveshare_lcd_port.cpp

void my_flush_cb(lv_display_t *disp, const lv_area_t *area, uint8_t *px_map) {
  int w = lv_area_get_width(area);
  int h = lv_area_get_height(area);
  lcd->drawBitmap(area->x1, area->y1, px_map, w, h);
  lv_display_flush_ready(disp);
}

// == UI ตัวอย่าง ==
void create_ui() {
  lv_obj_t *btn = lv_button_create(lv_screen_active());
  lv_obj_center(btn);

  lv_obj_t *label = lv_label_create(btn);
  lv_label_set_text(label, "Hello LVGL!");
  lv_obj_center(label);

  lv_obj_add_event_cb(btn, [](lv_event_t *e) {
    static bool toggle = false;
    lv_obj_t *lbl = lv_obj_get_child(e->current_target, 0);
    lv_label_set_text(lbl, toggle ? "Hello LVGL!" : "Clicked!");
    toggle = !toggle;
  }, LV_EVENT_CLICKED, NULL);
}

// == Setup LVGL buffer/display ==
void setup_lvgl() {
  lv_init();

  draw_buf = (lv_color_t *)heap_caps_malloc(sizeof(lv_color_t) * LV_HOR_RES_MAX * 40, MALLOC_CAP_DMA);
  if (!draw_buf) {
    Serial.println("Failed to allocate LVGL draw buffer!");
    while (1);
  }

  lv_display_draw_buf_init(&disp_buf, draw_buf, NULL, LV_HOR_RES_MAX * 40);
  disp = lv_display_create(LV_HOR_RES_MAX, LV_VER_RES_MAX);
  lv_display_set_flush_cb(disp, my_flush_cb);
  lv_display_set_draw_buffers(disp, &disp_buf);
}

void setup() {
  Serial.begin(115200);

  // เริ่มจอจาก waveshare_lcd_port.cpp (จะ set lcd pointer ให้อัตโนมัติ)
  waveshare_lcd_init();

  // เริ่ม LVGL + UI
  setup_lvgl();
  create_ui();
}

void loop() {
  lv_timer_handler();
  delay(5);
}
