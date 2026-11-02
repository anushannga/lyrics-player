#include <Arduino.h>
#include <U8g2lib.h>
#include <SPI.h>

// Existing wiring: CS=10, RESET=8, MOSI=11, SCK=13.
U8G2_ST7920_128X64_F_HW_SPI lcd(U8G2_R0,10,8);
uint8_t state=0, headerPos=0, crcPos=0;
uint16_t sequence=0, payloadSize=0, received=0, outputPos=0;
uint16_t checksum=0xffff, suppliedCRC=0;
uint8_t literalLeft=0, header[4];
bool invalid=false;
uint32_t lastByte=0;

uint16_t crcByte(uint16_t crc,uint8_t value) {
  crc^=(uint16_t)value<<8;
  for(uint8_t b=0;b<8;++b) crc=(crc&0x8000)?(crc<<1)^0x1021:crc<<1;
  return crc;
}
void outputByte(uint8_t value) {
  if(outputPos<1024) lcd.getBufferPtr()[outputPos++]=value;
  else invalid=true;
  checksum=crcByte(checksum,value);
}
void resetPacket() {state=0;headerPos=0;literalLeft=0;}
void setup() {
  Serial.begin(115200);
  lcd.begin();lcd.clearBuffer();lcd.sendBuffer();
  Serial.println(F("STREAMLCD 1"));
}
void loop() {
  if(state && (uint32_t)(millis()-lastByte)>1000) {resetPacket();Serial.println(F("ERR timeout"));}
  while(Serial.available()) {
    uint8_t value=Serial.read();lastByte=millis();
    if(state==0) {
      if(value=='?') Serial.println(F("STREAMLCD 1"));
      else if(value=='T') {
        // Independent U8g2 reference for the host's bitmap packing test.
        lcd.clearBuffer();
        lcd.drawPixel(0,0);lcd.drawPixel(7,0);lcd.drawPixel(8,1);
        lcd.drawPixel(13,17);lcd.drawPixel(127,63);
        lcd.drawFrame(20,25,31,19);
        uint16_t expected=0xffff;
        for(uint16_t i=0;i<1024;++i) expected=crcByte(expected,lcd.getBufferPtr()[i]);
        lcd.sendBuffer();Serial.print(F("TEST "));Serial.println(expected);
      }
      else if(value=='C') {lcd.clearBuffer();lcd.sendBuffer();Serial.println(F("OK C"));}
      else if(value=='F') {state=1;headerPos=0;}
    } else if(state==1) {
      header[headerPos++]=value;
      if(headerPos==4) {
        sequence=header[0]|((uint16_t)header[1]<<8);
        payloadSize=header[2]|((uint16_t)header[3]<<8);
        received=0;outputPos=0;checksum=0xffff;invalid=false;literalLeft=0;
        if(!payloadSize || payloadSize>2048) {resetPacket();Serial.println(F("ERR size"));}
        else state=2;
      }
    } else if(state==2) {
      ++received;
      if(literalLeft) {outputByte(value);--literalLeft;}
      else if(value&0x80) {uint8_t n=(value&0x7f)+1;while(n--)outputByte(0);}
      else literalLeft=value+1;
      if(received==payloadSize) {state=3;crcPos=0;suppliedCRC=0;}
    } else {
      if(crcPos++==0)suppliedCRC=value;
      else {
        suppliedCRC|=(uint16_t)value<<8;
        if(!invalid && !literalLeft && outputPos==1024 && checksum==suppliedCRC) {
          lcd.sendBuffer();Serial.print(F("OK "));Serial.println(sequence);
        } else {Serial.print(F("ERR "));Serial.println(sequence);}
        resetPacket();
      }
    }
  }
}
