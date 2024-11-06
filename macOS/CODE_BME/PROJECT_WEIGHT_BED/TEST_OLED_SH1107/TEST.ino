#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

// กำหนดพิน SDA และ SCL สำหรับ ESP32
#define SDA_PIN 21
#define SCL_PIN 22

// กำหนดออบเจกต์สำหรับจอแสดงผล SH1107 ที่มีความละเอียด 128x128
Adafruit_SH1107 display = Adafruit_SH1107(128, 128, &Wire);

void setup() {
    // เริ่มต้นการเชื่อมต่อ I2C โดยระบุพิน SDA และ SCL
    Wire.begin(SDA_PIN, SCL_PIN);

    // เริ่มต้นการทำงานของจอแสดงผล
    if (!display.begin(0x3C)) { // 0x3C คือ default I2C address ของ SH1107
        Serial.println("SH1107 ไม่สามารถเชื่อมต่อได้");
        while (1);
    }

    display.display(); // เปิดจอแสดงผล
    display.clearDisplay(); // เคลียร์หน้าจอ
    display.setRotation(0); // ตั้งค่าหมุนหน้าจอ (ปรับค่าได้ระหว่าง 0-3)
}

void loop() {
    display.clearDisplay();  // เคลียร์หน้าจอทุกครั้งก่อนเริ่มการแสดงผลใหม่

    display.setTextSize(1);             // กำหนดขนาดตัวอักษร
    display.setTextColor(SH110X_WHITE); // กำหนดสีตัวอักษร
    display.setCursor(0, 0);            // กำหนดตำแหน่งเริ่มต้นการแสดงผล
    display.print("Hello ESP32!");

    display.setCursor(0, 16); // ตั้งตำแหน่งแถวที่สอง
    display.print("Hello World!");

    display.setCursor(0, 32); // ตั้งตำแหน่งแถวที่สาม
    display.print("My ESP32!");

    display.display();        // อัพเดตจอแสดงผล
    delay(2000);              // รอ 2 วินาทีก่อนแสดงผลใหม่
}
