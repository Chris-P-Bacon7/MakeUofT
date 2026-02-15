#include <Arduino_GFX_Library.h>

// ----- Color Definitions (RGB565) -----
#define BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define YELLOW  0xFFE0
#define WHITE   0xFFFF
#define SKIN    0xFDCB // Light orange/flesh for hands
#define DEEP_BLUE 0x011F

// ----- Pin Definitions for ESP8266 (NodeMCU) -----
#define TFT_CS   D8   
#define TFT_DC   D2   
#define TFT_RST  D0   

Arduino_DataBus *bus = new Arduino_HWSPI(TFT_DC, TFT_CS);
Arduino_GFX *gfx = new Arduino_GC9A01(bus, TFT_RST, 0, true);

void setup() {
  Serial.begin(115200); // Higher baud for smoother laptop input
  gfx->begin();
  gfx->fillScreen(BLACK);
}

// ----- Helper: Draw Heart (Ref 1) -----
void drawHeart(int16_t x, int16_t y, int16_t size, uint16_t color) {
  gfx->fillCircle(x - size/2, y, size/2, color);
  gfx->fillCircle(x + size/2, y, size/2, color);
  gfx->fillTriangle(x - size, y + size/4, x + size, y + size/4, x, y + size * 1.5, color);
}

// ----- 0: Smiley with Blinking Hearts -----
void animationHearts() {
  for (int i = 0; i < 6; i++) {
    gfx->fillScreen(BLACK);
    gfx->fillCircle(120, 120, 100, YELLOW); // Large face
    // Squinting eyes (Ref 1)
    gfx->drawArc(100, 110, 15, 10, 200, 340, BLACK);
    gfx->drawArc(140, 110, 15, 10, 200, 340, BLACK);
    gfx->drawArc(120, 130, 40, 35, 20, 160, BLACK); // Smile
    
    if (i % 2 == 0) {
      drawHeart(50, 60, 20, RED);
      drawHeart(190, 70, 25, RED);
      drawHeart(70, 190, 30, RED);
    }
    delay(400);
  }
}

// ----- 1: Polite Smile (Morphing Line) -----
void animationPoliteSmile() {
  for (int i = 0; i < 6; i++) {
    gfx->fillCircle(120, 120, 100, YELLOW);
    gfx->fillCircle(90, 110, 10, BLACK); // Static eyes
    gfx->fillCircle(150, 110, 10, BLACK);
    
    // Mouth morphing
    if (i % 2 == 0) {
      gfx->fillRect(90, 160, 60, 6, BLACK); // Straight line
    } else {
      gfx->fillRect(90, 150, 65, 20, YELLOW); // Clear old mouth
      gfx->drawArc(120, 150, 35, 30, 20, 160, BLACK); // Curve
    }
    delay(500);
  }
}

// ----- 2: Secretly Interested (Peek-a-boo) -----
void animationPeek() {
  for (int i = 0; i < 6; i++) {
    gfx->fillScreen(BLACK);
    gfx->fillCircle(120, 120, 100, YELLOW);
    gfx->fillCircle(85, 110, 20, WHITE); // Left Eye
    gfx->fillCircle(155, 110, 20, WHITE); // Right Eye
    gfx->fillCircle(85, 110, 8, BLACK);  // Pupil
    gfx->fillCircle(155, 110, 8, BLACK); // Pupil

    if (i % 2 == 0) {
      // Hands covering eyes
      gfx->fillRoundRect(60, 90, 50, 80, 10, SKIN);
      gfx->fillRoundRect(130, 90, 50, 80, 10, SKIN);
    } else {
      // Move hands slightly apart for peak
      gfx->fillRoundRect(30, 90, 50, 80, 10, SKIN);
      gfx->fillRoundRect(160, 90, 50, 80, 10, SKIN);
    }
    delay(600);
  }
}

// ----- 3: Crying & Flooding Screen -----
void animationFlood() {
  for (int h = 0; h < 240; h += 15) {
    gfx->fillCircle(120, 120, 100, YELLOW);
    // Crying Eyes
    gfx->drawArc(90, 110, 20, 15, 200, 340, BLACK);
    gfx->drawArc(150, 110, 20, 15, 200, 340, BLACK);
    // Open Mouth
    gfx->fillEllipse(120, 170, 30, 20, BLACK);
    
    // Tear Streams
    gfx->fillRect(80, 115, 15, 125, BLUE);
    gfx->fillRect(145, 115, 15, 125, BLUE);
    
    // The Flood
    gfx->fillRect(0, 240 - h, 240, h, DEEP_BLUE);
    delay(150);
  }
}

void loop() {
  // animationHearts();
  // delay(2000);
  // animationPoliteSmile();
  // delay(2000);
  // animationPeek();
  // delay(2000);
  // animationFlood();
  // delay(2000);
  if (Serial.available() > 0) {
    char input = Serial.read();
    gfx->fillScreen(BLACK);

    switch (input) {
      case '0': animationHearts();      break;
      case '1': animationPoliteSmile(); break;
      case '2': animationPeek();        break;
      case '3': animationFlood();       break;
    }
  }
}


