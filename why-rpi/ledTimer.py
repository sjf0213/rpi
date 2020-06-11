#!/usr/bin/env python3
# LED Timer by jufeng
import time
from neopixel import *
import argparse

LED_COUNT      = 144 
LED_PIN        = 18  # GPIO pin 

parser = argparse.ArgumentParser()
parser.add_argument('num')
args = parser.parse_args()
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, 800000, 10, False, 255, 0)
strip.begin()
num = int(args.num)
for i in range(num):
    strip.setPixelColor(i, Color(128,0,128))
strip.show() 
while num > 0:
    for i in range(60):
        time.sleep(0.5)
        strip.setPixelColor(num, Color(128,0,128))
        strip.show() 
        time.sleep(0.5)
        strip.setPixelColor(num, Color(0,0,0))
        strip.show()
    num = num - 1
for i in range(LED_COUNT):
    strip.setPixelColor(i, Color(0,0,0))
strip.show()
