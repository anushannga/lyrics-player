#include <Arduino.h>
#include <U8g2lib.h>
#include <SPI.h>
#include "lyrics_bits.h"

// Existing wiring: SCK=13, MOSI=11, CS=10, RESET=8.
// Page buffer leaves ample SRAM for the Uno's stack and serial buffers.
U8G2_ST7920_128X64_1_HW_SPI lcd(U8G2_R0, 10, 8);
char command[24];
uint8_t used = 0;
bool overflowed = false;
int8_t currentLine = -1;
uint16_t transitionMs = 300;

// Ordered dissolve: replace 25%, 50%, 75%, then 100% of the old pixels.
// The LCD is monochrome, so this gives a short fade without moving the text.
void dissolveFrame(int8_t oldIndex, uint8_t newIndex, uint8_t step) {
  uint8_t strip[128];  // Eight scanlines; keep the Uno's small SRAM usage bounded.
  lcd.firstPage();
  do {
    uint8_t y = lcd.getBufferCurrTileRow() * 8;
    for (uint8_t row = 0; row < 8; ++row) {
      uint8_t mask;
      if (step == 4) mask = 0xff;
      else if (step == 1) mask = ((y + row) & 1) ? 0x00 : 0x55;
      else if (step == 2) mask = ((y + row) & 1) ? 0xaa : 0x55;
      else mask = ((y + row) & 1) ? 0xaa : 0xff;
      uint16_t offset = (uint16_t)(y + row) * 16;
      for (uint8_t x = 0; x < 16; ++x) {
        uint8_t before = oldIndex < 0 ? 0 : pgm_read_byte(&lyrics_bits[oldIndex][offset + x]);
        uint8_t after = pgm_read_byte(&lyrics_bits[newIndex][offset + x]);
        strip[row * 16 + x] = (before & (uint8_t)~mask) | (after & mask);
      }
    }
    lcd.drawXBM(0, y, 128, 8, strip);
  } while (lcd.nextPage());
}

void showLine(uint8_t n) {
  if (n >= LYRICS_COUNT) return;
  if (currentLine != n) {
    uint8_t index = pgm_read_byte(&lyric_index[n]);
    int8_t previous = currentLine < 0 ? -1 : pgm_read_byte(&lyric_index[currentLine]);
    uint32_t started = millis();
    for (uint8_t step = 1; step <= 4; ++step) dissolveFrame(previous, index, step);
    transitionMs = (uint16_t)(millis() - started);
    currentLine = n;
  }
  Serial.print(F("OK L")); Serial.println(n);
}

void clearDisplay() {
  lcd.firstPage();
  do {} while (lcd.nextPage());
  currentLine = -1;
  Serial.println(F("OK C"));
}

void handleCommand() {
  command[used] = '\0';
  if (!strcmp(command, "?")) {
    Serial.print(F("LYRICS " LYRICS_ID " ")); Serial.println(LYRICS_COUNT);
  } else if (!strcmp(command, "D")) {
    Serial.print(F("DRAW_MS ")); Serial.println(transitionMs);
  } else if (!strcmp(command, "C")) {
    clearDisplay();
  } else if (used >= 2 && command[0] == 'L') {
    char *end;
    long n = strtol(command + 1, &end, 10);
    if (*end == '\0' && n >= 0 && n < LYRICS_COUNT) showLine((uint8_t)n);
    else Serial.println(F("ERR line"));
  } else Serial.println(F("ERR command"));
}

void setup() {
  Serial.begin(9600);
  lcd.begin();
  showLine(0);
  Serial.println(F("READY " LYRICS_ID));
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      if (!overflowed && used) handleCommand();
      used = 0; overflowed = false;
    } else if (c != '\r') {
      if (used < sizeof(command)-1) command[used++] = c;
      else overflowed = true;
    }
  }
}
