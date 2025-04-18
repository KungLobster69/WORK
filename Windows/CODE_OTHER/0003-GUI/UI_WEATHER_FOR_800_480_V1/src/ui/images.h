#ifndef EEZ_LVGL_UI_IMAGES_H
#define EEZ_LVGL_UI_IMAGES_H

#include <lvgl.h>

#ifdef __cplusplus
extern "C" {
#endif

extern const lv_img_dsc_t img_icon_temp;
extern const lv_img_dsc_t img_icon_max_temp;
extern const lv_img_dsc_t img_icon_min_temp;
extern const lv_img_dsc_t img_icon_humd;
extern const lv_img_dsc_t img_icon_wind;
extern const lv_img_dsc_t img_icon_atmospheric_pressure;
extern const lv_img_dsc_t img_icon_location;
extern const lv_img_dsc_t img_icon_label_01d;
extern const lv_img_dsc_t img_icon_label_01n;
extern const lv_img_dsc_t img_icon_label_02d;
extern const lv_img_dsc_t img_icon_label_02n;
extern const lv_img_dsc_t img_icon_label_03d;
extern const lv_img_dsc_t img_icon_label_04d;
extern const lv_img_dsc_t img_icon_label_09d;
extern const lv_img_dsc_t img_icon_label_10d;
extern const lv_img_dsc_t img_icon_label_10n;
extern const lv_img_dsc_t img_icon_label_11d;
extern const lv_img_dsc_t img_icon_label_13d;
extern const lv_img_dsc_t img_icon_label_50d;

#ifndef EXT_IMG_DESC_T
#define EXT_IMG_DESC_T
typedef struct _ext_img_desc_t {
    const char *name;
    const lv_img_dsc_t *img_dsc;
} ext_img_desc_t;
#endif

extern const ext_img_desc_t images[19];


#ifdef __cplusplus
}
#endif

#endif /*EEZ_LVGL_UI_IMAGES_H*/