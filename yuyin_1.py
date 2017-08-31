#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 通过百度API实现语音合成、语音识别功能

__author__ = 'winsert@163.com'

import RPi.GPIO as GPIO
import sys, os, time
import pyaudio, wave

reload(sys)
sys.setdefaultencoding("utf-8")

# 引入百度Speech SDK
from aip import AipSpeech

#设置ReSpeak Button
BUTTON = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)

# 初始化AipSpeech对象
APP_ID = "XXXXXXXXXXX" #你申请的百度APP_ID
API_KEY = "XXXXXXXXXX" #你申请的百度APP_KEY
SECRET_KEY = "XXXXXXX" #你申请的百度SECRET_KEY
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 文本合成语音模块
def getAudio(guide_text):
    try:
        text = guide_text #要合成语音的文本
        result = aipSpeech.synthesis(text, 'zh', 1, {'vol':5, 'per':0, 'pit':5, 'spd':5})
        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            with open('guide.mp3', 'wb') as f:
                f.write(result)
        os.system('mpg123 guide.mp3') #开始录音的语音提示
    except:
        getAudio("主人,语音合成出现问题，请您先继续录音.")

        error_code = u"""
        错误代码说明：
        500 = 不支持输入
        501 = 输入参数不正确
        502 = token验证失败
        503 = 合成后端错误
        """
        print "错误码：", error_code

# 读取文件模块
def get_file_content(filePath):
    try:
        with open(filePath, 'rb') as fp:
            return fp.read()
    except:
        getAudio("主人,没有找到您的录音文件，无法进行语音识别..")


# 将录音转化为文本模块
def getText():
    try:
        text_dict = aipSpeech.asr(get_file_content('myRecord.wav'), 'wav', 16000, {'lan': 'zh',})
        result_text = text_dict['result']
        print "语音识别结果：",
        for h in result_text:
            print h
    except:
        for i in text_dict.keys():
            print i, " \t: ", text_dict[i]

        error_code = u"""
        错误代码说明：
        3300 = 输入参数不正确
        3301 = 识别错误
        3302 = 验证失败
        3303 = 语音服务器后端问题
        3304 = 请求 GPS 过大，超过限额
        3305 = 产品线当前日请求数超过
        """

        print "错误码：", error_code

# 录音模块
def getRecord(recTime):
    try:
        #设置录音参数
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        RECORD_SECONDS = recTime #录音时长
        WAVE_OUTPUT_FILENAME = 'myRecord.wav'

        pa = pyaudio.PyAudio()

        stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        print "start recording"

        frames = []

        for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print "* done recording"

        stream.stop_stream()
        stream.close()
        pa.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pa.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    except:
        getAudio("主人，录音过程出现错误，请您检查后重新录音.")

if __name__ == "__main__":

    print("*******************************************************")
    print("*                 yuyin.py 版本:0.1                   *")
    print("*                                                     *")
    print("*        通过百度语音API实现语音识别和语音合成        *")
    print("*              author: winsert@163.com                *")
    print("*                                                     *")
    print("* 所需硬件：                                          *")
    print("* Raspberry3B                                         *")
    print("* Respeaker 2 Mics Pi HAT                             *")
    print("*                                                     *")
    print("* 所需软件：                                          *")
    print("* python 2                                            *")
    print("* 因aplay不能播放百度合成的MP3,需安装mpg123来播放MP3  *")
    print("* 安装python的pyaudio、wave模块，用于录音             *")
    print("* 需要向百度语音yuyin.baidu.com申请APP_ID和KEY        *")
    print("*                                                     *")
    print("* 使用方法：                                          *")
    print("* 运行python yuyin.py                                 *")
    print("* 按下ReSpeak上的button后，听到语音提示               *")
    print("* 根据语音提示，先完成录音，然后再将录音转成文本      *")
    print("*******************************************************")

    while True:
        state = GPIO.input(BUTTON)
        if state:
            print("Button Status : OFF")
        else:
            print("Button Status : ON")
            getAudio("主人,现在开始录音.") #开始录音前的提示
            getRecord(8) #录音时长为8秒
            getAudio("主人，现在开始将您的录音转成文本，请稍候.") #开始语音转文本的语音提示
            getText() #语音转文本
        time.sleep(1)
