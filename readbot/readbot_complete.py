from RPi import GPIO
import time
from time import sleep
from picamera import PiCamera
from PIL import Image
from pytesseract import *
import numpy as np
import os
import sys
from tts import  AipSpeech
 
# 采用BCM引脚编号
GPIO.setmode(GPIO.BCM)
# 关闭警告
GPIO.setwarnings(False)
# 输入引脚
channel = 5
# 设置GPIO输入模式, 使用GPIO内置的上拉电阻, 即开关断开情况下输入为HIGH
GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# 检测HIGH -> LOW的变化
GPIO.add_event_detect(channel, GPIO.FALLING, bouncetime = 200)


AppID='11378601'
APPKEY="5KuYlT9jzIgnPGv3jw05rrRT"
APPSECRET="ONIQz4BT783zkxcLOEFS74VSZZOoDyqE"

SPEAKER=0   # 发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫
SPEED=5     # Speed, 0 ~ 15; 语速，取值0-15
PITCH=5     # Pitch, 0 ~ 15; 音调，取值0-15
VOLUME=15   # Volume, 0 ~ 15; 音量，取值0-15
AUE=3       # Aue,下载音频的格式 3为mp3格式(默认)； 4为pcm-16k；5为pcm-8k；6为wav（内容同pcm-16k）;
                # 注意AUE=4或者6是语音识别要求的格式，但是音频内容不是语音识别要求的自然人发音，所以识别效果会受影响。
FORMATS = {3:".mp3",4:".pcm",5:".pcm",6:".wav"}

# TTS
def txt2speech(text):
    client = AipSpeech(AppID, APPKEY, APPSECRET)
    formatStr = FORMATS[AUE]

    fname = '/home/pi/Desktop/rt.mp3'
    result = client.synthesis(text, 'zh', 1, {'per': SPEAKER, 'spd': SPEED, 'pit': PITCH, 'vol': VOLUME, })
    
    if not isinstance(result, dict):
        print("文件名：" + fname)
        with open(fname, 'wb') as fp:
            fp.write(result)
    os.system("mpg123 " + fname)
    
# OCR
def pic2txt(imgpath):
    print(imgpath)
    img0 = Image.open(imgpath)
    print(img0)
    img1 = img0.convert('L')
    img1.save("/home/pi/Desktop/img_gray.png")
    print(img1)
    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    threshold = 120
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # 图片二值化
    photo = img1.point(table, '1')
    photo.save("/home/pi/Desktop/img_blackwhite.png")
    print(photo)
    mychars = image_to_string(photo,'chi_sim').strip()
    print(mychars)
    
    txt2speech(mychars)
    
# 开关闭合的处理
def on_switch_pressed():
    print('open')
    camera = PiCamera()
    #camera.brightness = 50
    #camera.shutter_speed = 1000 
    camera.start_preview()
    sleep(5)
    imgpath = '/home/pi/Desktop/img_capture.png'
    camera.capture(imgpath)
    camera.stop_preview()
    
    file = "/home/pi/Desktop/iphoneshutter.mp3"
    os.system("mpg123 " + file)
    
    pic2txt(imgpath)
 
try:
    while True:
        # 如果检测到电平FALLING, 说明开关闭合
        if GPIO.event_detected(channel):
            on_switch_pressed()
        # 可以在循环中做其他检测
        time.sleep(0.5)     # 500毫秒的检测间隔
except Exception as e:
    print(e)
 
# 清理占用的GPIO资源
GPIO.cleanup()