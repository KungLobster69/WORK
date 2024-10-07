#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <HX711.h>

#define Tx_load_cell_01 5
#define Rx_load_cell_01 4
#define Tx_load_cell_02 6
#define Rx_load_cell_02 7

LiquidCrystal_I2C lcd(0x27, 16, 2);
HX711 scale01 (Tx_load_cell_01, Rx_load_cell_01);
HX711 scale02 (Tx_load_cell_02, Rx_load_cell_02);

void setup() {
  Serial.begin(115200);

  lcd.begin();
  lcd.backlight();
  lcd.setCursor(5, 0);  
  lcd.print("Weight");
  lcd.setCursor(2, 1);  
  lcd.print("Measurement");
  delay(1000);
}

void loop() {
  Read_load_cell01();
  Read_load_cell02();
}

void LCD() {
  LiquidCrystal_I2C lcd(0x27, 16, 2);  
  lcd.begin();
  lcd.setCursor(0, 0);     
  lcd.print("Weight = "); 
}

void LCD_Fail() {
  LiquidCrystal_I2C lcd(0x27, 16, 2);  
  lcd.begin();
  lcd.setCursor(2, 1);  
  lcd.print("Measurement");
  lcd.setCursor(6, 1);  
  lcd.print("Fail");
}

void Read_load_cell01() {
  float Weight_Loadcell01 = scale01.get_value();
  Serial.print("Weight 01: ");
  Serial.println(Weight_Loadcell01);
  delay(500);
}

void Read_load_cell02() {
  float Weight_Loadcell02 = scale02.get_value(); 
  Serial.print("Weight 02: ");
  Serial.println(Weight_Loadcell02);
  delay(500);
}