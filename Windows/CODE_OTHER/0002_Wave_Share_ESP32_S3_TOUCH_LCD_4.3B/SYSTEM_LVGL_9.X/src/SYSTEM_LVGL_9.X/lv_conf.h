#ifndef LV_CONF_H
#define LV_CONF_H

#define LV_HOR_RES_MAX      800
#define LV_VER_RES_MAX      480
#define LV_COLOR_DEPTH      16

#define LV_USE_OS           LV_OS_NONE     // ไม่มี RTOS (Arduino style)
#define LV_USE_LOG          1

#define LV_USE_DRAW         1
#define LV_USE_DRAW_SW      1
#define LV_USE_DISPLAY      1
#define LV_USE_TOUCHPAD     1

// Widgets
#define LV_USE_WIDGETS      1
#define LV_USE_LABEL        1
#define LV_USE_BTN          1
#define LV_USE_SLIDER       1

// Demos (สำหรับทดสอบ)
// #define LV_USE_DEMO_WIDGETS 1

#define LV_FONT_MONTSERRAT_20 1
#define LV_FONT_MONTSERRAT_28 1
#define LV_FONT_MONTSERRAT_30 1
#define LV_FONT_MONTSERRAT_40 1
#define LV_FONT_MONTSERRAT_48 1

#endif // LV_CONF_H
