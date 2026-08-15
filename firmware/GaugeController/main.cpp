/*
 MIT License
 Copyright (c) 2017 Paweł Stawicki
 Modifications (c) 2026 Al_Niz
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
 */
#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <string.h>

LiquidCrystal_I2C lcd(0x27, 20, 4); // set the LCD address to 0x27 for a 16 chars and 2 line display

// pins - voltage on outputs are ~1.5V so we use the ADC
#define DataPin A0
#define ClkPin A1
#define LedPin 13

// Dial Indicator resolution: 100 - 0.01mm, 1000 - 0.001mm
//#define Resolution 100
#define Resolution 1000

// UART speed
#define UARTBaudRate 9600

// ADC threshold, ADC values greater than this are interpreted as logical 1, see loop()
#define ADC_Threshold 140

// data format
#define DATA_BITS_LEN 24
#define INCH_BIT 23
#define SIGN_BIT 20
#define START_BIT -1 // -1 - no start bit

// data capture and decode functions
bool getRawBit()
{
  bool data;
  while (analogRead(ClkPin) > ADC_Threshold)
    ;
  while (analogRead(ClkPin) < ADC_Threshold)
    ;
  data = analogRead(DataPin) > ADC_Threshold;
  return data;
}

long getRawData()
{
  long out = 0;
  for (int i = 0; i < DATA_BITS_LEN; i++)
  {
    out |= getRawBit() ? 1L << DATA_BITS_LEN : 0L;
    out >>= 1;
  }
  return out;
}

long getValue(bool &inch)
{
  long out = getRawData();
  inch = out & (1L << INCH_BIT);
  bool sign = out & (1L << SIGN_BIT);
  out &= (1L << SIGN_BIT) - 1L;
  out >>= (START_BIT + 1);
  if (sign)
    out = -out;
  return out;
}

void toggleLed()
{
#ifdef LedPin
  static bool state = false;
  state = !state;
  digitalWrite(LedPin, state);
#endif
}

// Arduino setup and main loop

// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

void setup()
{
  pinMode(8, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP); // Pint to toggle between Serial Command or direct measurement without any serial communication
  // set ADC prescale to 16 (set ADC clock to 1MHz)
  // this gives as a sampling rate of ~77kSps
  sbi(ADCSRA, ADPS2);
  cbi(ADCSRA, ADPS1);
  cbi(ADCSRA, ADPS0);

  Serial.begin(UARTBaudRate);
#ifdef LedPin
  pinMode(LedPin, OUTPUT);
#endif

  lcd.init(); // initialize the lcd
  lcd.backlight();
}

double value_mm = -1;
double offset = 0;
void OverSerialCom();
void loop()
{

  if (digitalRead(7) == LOW)
  {
    bool inch;
    value_mm = getValue(inch) / 100.0;
    lcd.clear();
    lcd.printstr(String(value_mm).c_str());
  }
  else
  {
    OverSerialCom();
  }

  toggleLed();
}

void OverSerialCom()
{
  if (Serial.available() > 0)
  {
    lcd.clear();
    // read the incoming cmd:
    String cmd = Serial.readStringUntil('\n');

    cmd.replace("\n", "");
    cmd.replace("\r", "");
    cmd.toLowerCase();
    lcd.clear();
    lcd.printstr(cmd.c_str());
    if (cmd == "m")
    {
      bool inch; // this info comes from the gauge itself! there is an Inch bit is set if gauge measure in Inch

      Serial.print("OK\n");
      do
      {
        value_mm = getValue(inch) / 100.0;
      } while (-26 > value_mm || value_mm > 26);
    }
    else
    {
      if (cmd == "g")
      {
        Serial.println(value_mm);
        lcd.clear();
        lcd.printstr(String(value_mm).c_str());
      }
      else
      {
        Serial.println("Error Unknown cmd: " + cmd);
        lcd.printstr(String("Error Unknown cmd: " + cmd).c_str());
      }
    }
  }
}