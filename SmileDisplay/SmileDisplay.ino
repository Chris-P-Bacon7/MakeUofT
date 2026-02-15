#include <Arduino_GFX_Library.h>


// ----- Color Definitions (RGB565) -----
#define BLACK 0x0000
#define BLUE 0x001F
#define RED 0xF800
#define YELLOW 0xFFE0
#define WHITE 0xFFFF
#define SKIN 0xFDCB  // Light orange/flesh for hands
#define DEEP_BLUE 0x011F


// ----- Pin Definitions for ESP8266 (NodeMCU) -----
#define TFT_CS D8
#define TFT_DC D2
#define TFT_RST D0


Arduino_DataBus *bus = new Arduino_HWSPI(TFT_DC, TFT_CS);
Arduino_GFX *gfx = new Arduino_GC9A01(bus, TFT_RST, 0, true);


// ----- Global Variables -----
char currentMood = '4';  // No mood initially


// Animation step counters
int heartsFrame = 0;
int politeFrame = 0;
int peekFrame = 0;
int floodHeight = 0;
int thinkingFrame = 0;


// ----- Helper: Draw Heart -----
void drawHeart(int16_t x, int16_t y, int16_t size, uint16_t color) {
  gfx->fillCircle(x - size / 2, y, size / 2, color);
  gfx->fillCircle(x + size / 2, y, size / 2, color);
  gfx->fillTriangle(x - size, y + size / 4, x + size, y + size / 4, x, y + size * 1.5, color);
}


// ----- Animation Steps -----
void animationHeartsStep() {
  gfx->fillScreen(BLACK);
  gfx->fillCircle(120, 120, 100, YELLOW);           // Large face
  gfx->drawArc(100, 110, 15, 10, 200, 340, BLACK);  // Left eye
  gfx->drawArc(140, 110, 15, 10, 200, 340, BLACK);  // Right eye
  gfx->drawArc(120, 130, 40, 35, 20, 160, BLACK);   // Smile


  if (heartsFrame % 2 == 0) {
    drawHeart(50, 60, 20, RED);
    drawHeart(190, 70, 25, RED);
    drawHeart(70, 190, 30, RED);
  }


  heartsFrame++;
  if (heartsFrame > 5) heartsFrame = 0;  // Loop frames
  delay(400);
}


void animationPoliteSmileStep() {
  gfx->fillScreen(BLACK);
  gfx->fillCircle(120, 120, 100, YELLOW);
  gfx->fillCircle(90, 110, 10, BLACK);   // Left eye
  gfx->fillCircle(150, 110, 10, BLACK);  // Right eye


  if (politeFrame % 2 == 0) {
    gfx->fillRect(90, 160, 60, 6, BLACK);  // Straight line mouth
  } else {
    gfx->fillRect(90, 150, 65, 20, YELLOW);          // Clear old mouth
    gfx->drawArc(120, 150, 35, 30, 20, 160, BLACK);  // Curve smile
  }


  politeFrame++;
  if (politeFrame > 5) politeFrame = 0;
  delay(500);
}


void animationPeekStep() {
  gfx->fillScreen(BLACK);
  gfx->fillCircle(120, 120, 100, YELLOW);  // Face
  gfx->fillCircle(85, 110, 20, WHITE);     // Left Eye
  gfx->fillCircle(155, 110, 20, WHITE);    // Right Eye
  gfx->fillCircle(85, 110, 8, BLACK);      // Left pupil
  gfx->fillCircle(155, 110, 8, BLACK);     // Right pupil


  if (peekFrame % 2 == 0) {
    gfx->fillRoundRect(60, 90, 50, 80, 10, SKIN);
    gfx->fillRoundRect(130, 90, 50, 80, 10, SKIN);
  } else {
    gfx->fillRoundRect(30, 90, 50, 80, 10, SKIN);
    gfx->fillRoundRect(160, 90, 50, 80, 10, SKIN);
  }


  peekFrame++;
  if (peekFrame > 5) peekFrame = 0;
  delay(600);
}


void animationFloodStep() {
  gfx->fillCircle(120, 120, 100, YELLOW);
  gfx->drawArc(90, 110, 20, 15, 200, 340, BLACK);   // Left eye
  gfx->drawArc(150, 110, 20, 15, 200, 340, BLACK);  // Right eye
  gfx->fillEllipse(120, 170, 30, 20, BLACK);        // Mouth


  gfx->fillRect(80, 115, 15, 125, BLUE);   // Left tear
  gfx->fillRect(145, 115, 15, 125, BLUE);  // Right tear


  gfx->fillRect(0, 240 - floodHeight, 240, floodHeight, DEEP_BLUE);  // Flood


  floodHeight += 15;
  if (floodHeight > 240) floodHeight = 0;
  delay(150);
}


void animationThinkingStep(int step) {
  // 1. Draw Static Face Parts (Base)
  gfx->fillCircle(120, 120, 100, YELLOW); // Face
  
  // 2. The Skeptical Eyes & Eyebrows
  // Left: Normal eye, Right: Slightly smaller/skeptical
  gfx->fillCircle(85, 100, 12, BLACK);    
  gfx->fillCircle(155, 105, 10, BLACK);   
  
  // Slanted Eyebrows (The key to the emoji look)
  gfx->drawLine(70, 85, 105, 75, BLACK);  // Left angled up
  gfx->drawLine(140, 80, 175, 85, BLACK); // Right angled down

  // 3. The "Thinking" Mouth (Small smirk/flat line)
  gfx->fillRect(100, 160, 45, 4, BLACK);

  // 4. The Hand (Under the Chin)
  // Hand moves slightly up and down to look like it's tapping the chin
  int yOffset = (step % 2 == 0) ? 0 : -5; 

  // Hand/Palm area
  gfx->fillRoundRect(100, 185 + yOffset, 50, 25, 10, SKIN); 
  
  // Finger touching chin (The Pointer)
  gfx->fillRoundRect(140, 155 + yOffset, 12, 40, 5, SKIN); 
  
  // Thumb (rested along the bottom)
  gfx->fillRoundRect(90, 185 + yOffset, 30, 12, 5, SKIN); 
}


// ----- Setup -----
void setup() {
  Serial.begin(115200);  // Laptop input
  gfx->begin();
  gfx->fillScreen(BLACK);
}


void loop() {
  // 1. Check for new serial input
  if (Serial.available() > 0) {
    char input = Serial.read();

    // Clear out any trailing characters (like \n) to keep the line clean
    while(Serial.available() > 0) Serial.read();

    // Only reset if the mood has actually changed
    if (input != currentMood && (input >= '0' && input <= '4')) {
      currentMood = input;     
      gfx->fillScreen(BLACK);  
      
      // Reset all animation states to start fresh
      heartsFrame = 0;
      politeFrame = 0;
      peekFrame = 0;
      floodHeight = 0;
      thinkingFrame = 0;
    }
  }

  // 2. Run current animation step
  switch (currentMood) {
    case '0': 
      animationHeartsStep(); 
      break;
    case '1': 
      animationPoliteSmileStep(); 
      break;
    case '2': 
      animationPeekStep(); 
      break;
    case '3': 
      animationFloodStep(); 
      break;
    case '4':
    default: 
      // Pass thinkingFrame to match your "void animationThinkingStep(int step)" signature
      animationThinkingStep(thinkingFrame); 
      thinkingFrame++;
      if (thinkingFrame > 20) thinkingFrame = 0; // Keep frame count low for tapping logic
      delay(300); // Standard thinking tap speed
      break;
  }
}