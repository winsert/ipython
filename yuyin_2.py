#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#设置对话变量:
answer = '回'
title = '大人'
ss = 2 #录音时长X秒

# 初始化AipSpeech参数
APP_ID = "XXXXXXXXXX" #填写你申请的百度APP_ID
API_KEY = "XXXXXXXXX" #填写你申请的百度APP_KEY
SECRET_KEY = "XXXXXX" #填写你申请的百度SECRET_KEY

import RPi.GPIO as GPIO
import sys, os, time
import pyaudio, wave

reload(sys)
sys.setdefaultencoding("utf-8")

# 引入百度Speech SDK
from aip import AipSpeech
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#设置ReSpeak Button
BUTTON = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)

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
    except Exception ,e:
        getAudio(title+"语音合成出现问题,请再试一次.")
        print "语言合成错误：", e

        for i in dict.keys():
            print i, " \t: ", dict[i]

        error_code = u"""
        错误代码说明：
        500 = 不支持输入
        501 = 输入参数不正确
        502 = token验证失败
        503 = 合成后端错误
        """
        print "错误码：", error_code

# 读取文件
def get_file_content(filePath):
    try:
        with open(filePath, 'rb') as fp:
            return fp.read()
    except:
        getAudio(title+"没有找到您的录音文件，无法进行语音识别.")


# 将录音转化为文本模块
def getText():
    try:
        text_dict = aipSpeech.asr(get_file_content('myRecord.wav'), 'wav', 16000, {'lan': 'zh',})
        result_text = text_dict['result']
        print "语音识别结果：",
        for rt in result_text:
            print rt
        return rt
    except Exception ,e:
        print "语言识别错误：", e

        for i in text_dict.keys():
            print i, " \t: ", text_dict[i]

        error_code = u"""
        3300 = 输入参数不正确
        3301 = 识别错误
        3302 = 验证失败
        3303 = 语音服务器后端问题
        3304 = 请求 GPS 过大，超过限额
        3305 = 产品线当前日请求数超过
        """
        print "错误代码说明：", error_code

        rt = u'错误'
        return rt

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

        print "开始录音......"

        frames = []

        for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print "录音结束!"

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
        getAudio(title+"录音过程出现错误，请您检查后重新录音.")

# 查询树莓派CPU的温度
def getCpuTemp():
    cputemp=os.popen('vcgencmd measure_temp').readline()
    sumcputemp=float(cputemp.replace("temp=","").replace("'C\n",""))
    cpuMsg =  u'当前树莓派的温度是'+str(sumcputemp)+u'度'
    return cpuMsg


if __name__ == "__main__":

    print("*******************************************************")
    print("*                 yuyin.py 版本:0.2                   *")
    print("*                                                     *")
    print("*          通过百度语音API实现语音操作命令            *")
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
    print("* 运行python yuyin_2.py                               *")
    print("* 按下ReSpeak上的button，听到语音提示后说出命令       *")
    print("*                                                     *")
    print("* 基础功能：                                          *")
    print("* '结束'退出本应用                                    *")
    print("* '日期'查询今天的年月日                              *")
    print("* '温度'查询树莓派CPU当前的温度                       *")
    print("* '时间'或'几点了'查询当前的时间                      *")
    print("*******************************************************")
    time.sleep(2)

    while True:
        state = GPIO.input(BUTTON)
        if state:
            print("Button Status : OFF")
        else:
            print("Button Status : ON")
            try:
                getAudio(title+"请吩咐.") #语音提示
                getRecord(ss) #录音时长为X秒
                result_text = getText() #语音识别
                text_list = list(result_text)
                #print text_list
                if len(text_list) <= 3:
                    comm_text = text_list[0]+text_list[1] #识前2个字
                elif len(text_list) <= 4:
                    comm_text = text_list[0]+text_list[1]+text_list[2] #识前3个字
                else:
                    comm_text = text_list[0]+text_list[1]+text_list[2]+text_list[3] #识别前4个字
                print 'yuyin的识别结果：', comm_text

                if comm_text == '结束':
                    getAudio(title+"再见.") #语音提示
                    sys.exit(0)
                elif comm_text == '错误':
                    getAudio(title+"语音识别有错误,请您按键后再说一遍.") 
                elif comm_text == '日期':
                    tt = time.localtime(time.time())
                    dateMsg = answer+title+'今天是'+str(tt.tm_year)+'年'+str(tt.tm_mon)+'月'+str(tt.tm_mday)+'日'
                    print dateMsg
                    getAudio(dateMsg)
                elif comm_text == '时间' or comm_text == '几点了':
                    tt = time.localtime(time.time())
                    dateMsg = answer+title+'现在的时间是'+str(tt.tm_hour)+'点'+str(tt.tm_min)+'分'+str(tt.tm_sec)+'秒'
                    print dateMsg
                    getAudio(dateMsg)
                elif comm_text == '温度':
                    cpuMsg = answer+title+getCpuTemp()
                    print cpuMsg
                    getAudio(cpuMsg)
                else:
                    getAudio(title+"我不明白你的话,请您重新按键后再说一遍.") 
            except Exception, e:
                getAudio(title+"遇到错误了,请您重新按键后再说一遍.") 
                print "Comm_text 识别错误： ",e
        time.sleep(1)
