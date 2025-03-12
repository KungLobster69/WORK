#include <string.h>

#include "screens.h"
#include "images.h"
#include "fonts.h"
#include "actions.h"
#include "vars.h"
#include "styles.h"
#include "ui.h"

#include <string.h>

objects_t objects;
lv_obj_t *tick_value_change_obj;

void create_screen_main() {
    lv_obj_t *obj = lv_obj_create(0);
    objects.main = obj;
    lv_obj_set_pos(obj, 0, 0);
    lv_obj_set_size(obj, 320, 170);
    lv_obj_set_style_bg_color(obj, lv_color_hex(0xff464653), LV_PART_MAIN | LV_STATE_DEFAULT);
    {
        lv_obj_t *parent_obj = obj;
        {
            lv_obj_t *obj = lv_obj_create(parent_obj);
            objects.obj0 = obj;
            lv_obj_set_pos(obj, 5, 5);
            lv_obj_set_size(obj, 310, 80);
            lv_obj_set_style_border_opa(obj, 0, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_border_width(obj, 0, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_bg_color(obj, lv_color_hex(0xff262635), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_img_create(parent_obj);
            lv_obj_set_pos(obj, 8, 10);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_img_set_src(obj, &img_icon_location_11p);
        }
        {
            // label_city
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_city = obj;
            lv_obj_set_pos(obj, 24, 8);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "City");
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            // label_time
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_time = obj;
            lv_obj_set_pos(obj, 8, 21);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "00:00:00");
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_40, LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            // label_date
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_date = obj;
            lv_obj_set_pos(obj, 8, 65);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "Wednesday, 00-Dec-2025");
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            // image_icon_weather
            lv_obj_t *obj = lv_img_create(parent_obj);
            objects.image_icon_weather = obj;
            lv_obj_set_pos(obj, 238, 9);
            lv_obj_set_size(obj, 72, 72);
            lv_img_set_src(obj, &img_icon_01d_72p);
        }
        {
            // label_weather_description
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_weather_description = obj;
            lv_obj_set_pos(obj, 166, 65);
            lv_obj_set_size(obj, 72, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "Clear sky");
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_align(obj, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            // label_weather_main
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_weather_main = obj;
            lv_obj_set_pos(obj, 166, 9);
            lv_obj_set_size(obj, 72, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "Clear");
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_align(obj, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_obj_create(parent_obj);
            objects.obj1 = obj;
            lv_obj_set_pos(obj, 5, 88);
            lv_obj_set_size(obj, 153, 50);
            lv_obj_set_style_border_opa(obj, 0, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_border_width(obj, 0, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_bg_color(obj, lv_color_hex(0xff262635), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_obj_create(parent_obj);
            objects.obj2 = obj;
            lv_obj_set_pos(obj, 162, 88);
            lv_obj_set_size(obj, 153, 50);
            lv_obj_set_style_border_opa(obj, 0, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_border_width(obj, 0, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_bg_color(obj, lv_color_hex(0xff262635), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_img_create(parent_obj);
            lv_obj_set_pos(obj, 8, 102);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_img_set_src(obj, &img_icon_temp_22p);
        }
        {
            // label_temperature
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_temperature = obj;
            lv_obj_set_pos(obj, 24, 106);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "-00.0°C");
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj3 = obj;
            lv_obj_set_pos(obj, 70, 123);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "Feel like");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj4 = obj;
            lv_obj_set_pos(obj, 108, 123);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, ":");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            // label_feels_like
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_feels_like = obj;
            lv_obj_set_pos(obj, 121, 123);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "-00.0°C");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_obj_create(parent_obj);
            objects.obj5 = obj;
            lv_obj_set_pos(obj, 5, 141);
            lv_obj_set_size(obj, 310, 23);
            lv_obj_set_style_border_opa(obj, 0, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_border_width(obj, 0, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_bg_color(obj, lv_color_hex(0xff262635), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_img_create(parent_obj);
            lv_obj_set_pos(obj, 75, 95);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_img_set_src(obj, &img_icon_max_11p);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj6 = obj;
            lv_obj_set_pos(obj, 87, 96);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "MAX");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj7 = obj;
            lv_obj_set_pos(obj, 109, 96);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, ":");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            // label_temp_max
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_temp_max = obj;
            lv_obj_set_pos(obj, 121, 96);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "-00.0°C");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_img_create(parent_obj);
            lv_obj_set_pos(obj, 75, 110);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_img_set_src(obj, &img_icon_min_11p);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj8 = obj;
            lv_obj_set_pos(obj, 87, 111);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "MIN");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj9 = obj;
            lv_obj_set_pos(obj, 109, 111);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, ":");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            // label_temp_min
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_temp_min = obj;
            lv_obj_set_pos(obj, 121, 111);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "-00.0°C");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_img_create(parent_obj);
            lv_obj_set_pos(obj, 238, 108);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_img_set_src(obj, &img_icon_pressure_11p);
        }
        {
            lv_obj_t *obj = lv_img_create(parent_obj);
            lv_obj_set_pos(obj, 166, 102);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_img_set_src(obj, &img_icon_humd_22p);
        }
        {
            lv_obj_t *obj = lv_img_create(parent_obj);
            lv_obj_set_pos(obj, 238, 93);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_img_set_src(obj, &img_icon_wind_11p);
        }
        {
            lv_obj_t *obj = lv_img_create(parent_obj);
            lv_obj_set_pos(obj, 238, 122);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_img_set_src(obj, &img_icon_visibility_11p);
        }
        {
            // label_humidity
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_humidity = obj;
            lv_obj_set_pos(obj, 187, 107);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "000%");
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj10 = obj;
            lv_obj_set_pos(obj, 252, 93);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, ":");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj11 = obj;
            lv_obj_set_pos(obj, 252, 108);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, ":");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj12 = obj;
            lv_obj_set_pos(obj, 252, 123);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, ":");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            // label_wind
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_wind = obj;
            lv_obj_set_pos(obj, 265, 93);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "000.0 km/h");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            // label_pressure
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_pressure = obj;
            lv_obj_set_pos(obj, 272, 108);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "0000 hPa");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            // label_visibility
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_visibility = obj;
            lv_obj_set_pos(obj, 278, 123);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_text(obj, "00.0 km");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_8, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            // label_info
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.label_info = obj;
            lv_obj_set_pos(obj, 38, 145);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            lv_label_set_long_mode(obj, LV_LABEL_LONG_SCROLL);
            lv_label_set_text(obj, "Last data update : 00 : 00 : 00 ( Succeed )");
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xfff0f0f0), LV_PART_MAIN | LV_STATE_DEFAULT);
        }
    }
    
    tick_screen_main();
}

void tick_screen_main() {
}



typedef void (*tick_screen_func_t)();
tick_screen_func_t tick_screen_funcs[] = {
    tick_screen_main,
};
void tick_screen(int screen_index) {
    tick_screen_funcs[screen_index]();
}
void tick_screen_by_id(enum ScreensEnum screenId) {
    tick_screen_funcs[screenId - 1]();
}

void create_screens() {
    lv_disp_t *dispp = lv_disp_get_default();
    lv_theme_t *theme = lv_theme_default_init(dispp, lv_palette_main(LV_PALETTE_BLUE), lv_palette_main(LV_PALETTE_RED), false, LV_FONT_DEFAULT);
    lv_disp_set_theme(dispp, theme);
    
    create_screen_main();
}
