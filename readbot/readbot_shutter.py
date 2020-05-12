from RPi import GPIO
import time
import os
from time import sleep
from picamera import PiCamera
 
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


# 开关闭合的处理
def on_switch_pressed():
    print('shutter ')
    camera = PiCamera()
    camera.start_preview()
    sleep(5)
    imgpath = '/home/pi/Desktop/imgcapture.jpg'
    camera.capture(imgpath)
    camera.stop_preview()

    file = "/home/pi/Desktop/iphoneshutter.mp3"
    os.system("mpg123 " + file)
 
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