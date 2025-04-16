#ifndef __LCD_PORT_H
#define __LCD_PORT_H

#pragma once

#include <Arduino.h>
#include <esp_display_panel.hpp>
using namespace esp_panel::drivers;

#define EXAMPLE_LCD_NAME                        ST7262
#define EXAMPLE_LCD_WIDTH                       (800)
#define EXAMPLE_LCD_HEIGHT                      (480)
#define EXAMPLE_LCD_COLOR_BITS                  (16)
#define EXAMPLE_LCD_RGB_DATA_WIDTH              (16)
#define EXAMPLE_LCD_RGB_COLOR_BITS              (16)
#define EXAMPLE_LCD_RGB_TIMING_FREQ_HZ          (16 * 1000 * 1000)

#define EXAMPLE_LCD_RGB_TIMING_HPW              (10)
#define EXAMPLE_LCD_RGB_TIMING_HBP              (40)
#define EXAMPLE_LCD_RGB_TIMING_HFP              (5)
#define EXAMPLE_LCD_RGB_TIMING_VPW              (10)
#define EXAMPLE_LCD_RGB_TIMING_VBP              (8)
#define EXAMPLE_LCD_RGB_TIMING_VFP              (8)

#define EXAMPLE_LCD_RGB_IO_DISP                 (-1)
#define EXAMPLE_LCD_RGB_IO_VSYNC                (3)
#define EXAMPLE_LCD_RGB_IO_HSYNC                (46)
#define EXAMPLE_LCD_RGB_IO_DE                   (5)
#define EXAMPLE_LCD_RGB_IO_PCLK                 (7)

#define EXAMPLE_LCD_RGB_IO_DATA0                (14)
#define EXAMPLE_LCD_RGB_IO_DATA1                (38)
#define EXAMPLE_LCD_RGB_IO_DATA2                (18)
#define EXAMPLE_LCD_RGB_IO_DATA3                (17)
#define EXAMPLE_LCD_RGB_IO_DATA4                (10)
#define EXAMPLE_LCD_RGB_IO_DATA5                (39)
#define EXAMPLE_LCD_RGB_IO_DATA6                (0)
#define EXAMPLE_LCD_RGB_IO_DATA7                (45)
#define EXAMPLE_LCD_RGB_IO_DATA8                (48)
#define EXAMPLE_LCD_RGB_IO_DATA9                (47)
#define EXAMPLE_LCD_RGB_IO_DATA10               (21)
#define EXAMPLE_LCD_RGB_IO_DATA11               (1)
#define EXAMPLE_LCD_RGB_IO_DATA12               (2)
#define EXAMPLE_LCD_RGB_IO_DATA13               (42)
#define EXAMPLE_LCD_RGB_IO_DATA14               (41)
#define EXAMPLE_LCD_RGB_IO_DATA15               (40)

#define EXAMPLE_LCD_RST_IO                      (-1)
#define EXAMPLE_LCD_RGB_BOUNCE_BUFFER_SIZE      (EXAMPLE_LCD_WIDTH * 10)

#define _EXAMPLE_LCD_CLASS(name, ...) LCD_##name(__VA_ARGS__)
#define EXAMPLE_LCD_CLASS(name, ...)  _EXAMPLE_LCD_CLASS(name, ##__VA_ARGS__)

extern LCD *lcd;
void waveshare_lcd_init();

#endif
