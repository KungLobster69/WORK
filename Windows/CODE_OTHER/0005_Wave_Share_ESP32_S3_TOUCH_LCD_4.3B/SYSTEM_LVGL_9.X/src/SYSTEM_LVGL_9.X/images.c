#include "images.h"

const ext_img_desc_t images[7] = {
    { "icon_temp", &img_icon_temp },
    { "icon_max_temp", &img_icon_max_temp },
    { "icon_min_temp", &img_icon_min_temp },
    { "icon_humd", &img_icon_humd },
    { "icon_wind", &img_icon_wind },
    { "icon_atmospheric_pressure", &img_icon_atmospheric_pressure },
    { "icon_location", &img_icon_location },
};
