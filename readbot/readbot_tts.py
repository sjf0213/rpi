import sys
import os
from tts import AipSpeech
 
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

client = AipSpeech(AppID, APPKEY, APPSECRET)
formatStr = FORMATS[AUE]
text = """作者按语 本书内容均来自于现实生活。虽然处于修辞的目的，已经进行了很大改动，但请读者务必从本质上视其为事实。不过，不要将其与正统禅宗佛教徒修行的大量相关真实信息等同视之。书中关于摩托车的部分也并非十分准确。"""
fname = '/home/pi/Desktop/rt2.mp3'
result = client.synthesis(text, 'zh', 1, {'per': SPEAKER, 'spd': SPEED, 'pit': PITCH, 'vol': VOLUME, })

if not isinstance(result, dict):
    print("文件名：" + fname)
    with open(fname, 'wb') as fp:
        fp.write(result)
os.system("mpg123 " + fname)
