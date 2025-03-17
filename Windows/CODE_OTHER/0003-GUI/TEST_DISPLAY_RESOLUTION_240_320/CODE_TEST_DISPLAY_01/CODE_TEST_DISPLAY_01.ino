//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 01_Test_Displaying_Text_and_Drawing_Shapes
//---------------------------------------- Including Libraries.
#include <TFT_eSPI.h>
#include <SPI.h>
//---------------------------------------- 

// Invoke custom library.
TFT_eSPI tft = TFT_eSPI();



//________________________________________________________________________________ VOID SETUP()
void setup() {
  // put your setup code here, to run once:

  tft.init();
}
//________________________________________________________________________________ 



//________________________________________________________________________________ VOID LOOP()
void loop() {
  // put your main code here, to run repeatedly:

  for (byte i = 0; i < 4; i++) {
    tft.setRotation(i);  //--> Range from 0 to 3.

    // Clear the screen to defined colour.
    // To see the list of colors, open the file "TFT_eSPI.h" (Arduino IDE library folder -> TFT_eSPI -> TFT_eSPI.h).
    // Look at "Section 6" (on line 302).
    tft.fillScreen(TFT_WHITE);
  
    tft.setCursor(10, 10);
    tft.setTextColor(TFT_BROWN); tft.setTextSize(1);
    tft.print("LCD TFT Touchscreen");
    tft.setCursor(9, 25);
    tft.print("ILI9341 240*320 Pixel");
    tft.setTextColor(TFT_GREEN); tft.setTextSize(2);
    tft.setCursor(10, 40);
    tft.print("with ESP32");
    tft.setCursor(10, 60);
    tft.print("& TFT_eSPI Library");
    tft.setTextColor(TFT_CYAN); tft.setTextSize(2);
    tft.setCursor(10, 85);
    tft.print("UTEH STR");
  
    // Draw a filled rectangle.
    tft.fillRect(10, 110, 20, 20, TFT_PURPLE);  //--> fillRect(x, y, w, h, color);
  
    // Draw a filled circle.
    tft.fillCircle(45, 120, 10, TFT_OLIVE);  //--> fillCircle(x, y, radius, color);
  
    // Draw a filled triangle.
    tft.fillTriangle(70, 110, 60, 130, 80, 130, TFT_BLUE);  //--> fillTriangle(x0, y0, x1, y1, x2, y2, color);

    delay(2000);
  }
}
//________________________________________________________________________________ 
//<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
