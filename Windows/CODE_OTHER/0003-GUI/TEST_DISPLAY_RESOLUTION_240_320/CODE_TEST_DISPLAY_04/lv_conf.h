#ifndef LV_CONF_H
#define LV_CONF_H

/*====================
   LVGL Configuration
 *====================*/

/* Enable LVGL */
#define LV_USE_LVGL 1

/* Set LVGL color depth */
#define LV_COLOR_DEPTH 16

/* Display resolution */
#define LV_HOR_RES_MAX 320
#define LV_VER_RES_MAX 240

/* Enable log (for debugging) */
#define LV_USE_LOG 1
#define LV_LOG_LEVEL LV_LOG_LEVEL_WARN

/* Enable built-in fonts */
/* Enable built-in fonts */
#define LV_FONT_MONTSERRAT_10  1
#define LV_FONT_MONTSERRAT_12  1
#define LV_FONT_MONTSERRAT_14  1 
#define LV_FONT_MONTSERRAT_24  1
#define LV_FONT_MONTSERRAT_48  1


/* Enable features */
#define LV_USE_IMG 1
#define LV_USE_LABEL 1
#define LV_USE_BTN 1
#define LV_USE_SLIDER 1

/* Enable display driver */
#define LV_USE_TFT_ESPI 1

#endif /* LV_CONF_H */
