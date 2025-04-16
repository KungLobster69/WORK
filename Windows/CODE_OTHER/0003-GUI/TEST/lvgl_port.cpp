#define LV_CONF_INCLUDE_SIMPLE
#include <lvgl.h>

#include "lvgl_port.h"
#include "waveshare_lcd_port.h"

extern LCD *lcd;

static lv_disp_draw_buf_t draw_buf;
static lv_color_t *buf1;
static lv_color_t *buf2;

static void my_flush_cb(lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *px_map) {
    int w = area->x2 - area->x1 + 1;
    int h = area->y2 - area->y1 + 1;

    lcd->drawBitmap(area->x1, area->y1, w, h, reinterpret_cast<const uint8_t *>(px_map));
    lv_disp_flush_ready(disp);
}

void lvgl_port_init(void) {
    lv_init();

    buf1 = (lv_color_t *)heap_caps_malloc(EXAMPLE_LCD_WIDTH * 40 * sizeof(lv_color_t), MALLOC_CAP_DMA);
    buf2 = (lv_color_t *)heap_caps_malloc(EXAMPLE_LCD_WIDTH * 40 * sizeof(lv_color_t), MALLOC_CAP_DMA);

    lv_disp_draw_buf_init(&draw_buf, buf1, buf2, EXAMPLE_LCD_WIDTH * 40);

    static lv_disp_drv_t disp_drv;
    lv_disp_drv_init(&disp_drv);
    disp_drv.hor_res = EXAMPLE_LCD_WIDTH;
    disp_drv.ver_res = EXAMPLE_LCD_HEIGHT;
    disp_drv.flush_cb = my_flush_cb;
    disp_drv.draw_buf = &draw_buf;
    lv_disp_drv_register(&disp_drv);
}
