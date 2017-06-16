#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'winsert@163.com'

import os
import requests
import json,time,string

#获取cpu温度
def getcputemperature():
    cputemp=os.popen('vcgencmd measure_temp').readline()
    sumcputemp=cputemp.replace("temp=","").replace("'C\n","")
    return sumcputemp

#获取CPU及内存使用情况
def getcpuused():
    return(os.popen("top -n1"))

#apikey为用户id
apiheaders={'U-ApiKey':'ada679ed152da2419e450917fe58ed44','content-type': 'application/json'}

#CPU温度使用 405362 传感器
cputemp_apiurl="http://api.yeelink.net/v1.0/device/357296/sensor/405363/datapoints"

#cpu 使用情况使用 405365 传感器
cpuused_apiurl="http://api.yeelink.net/v1.0/device/357296/sensor/405365/datapoints"

#内存占用率使用 405366 传感器
memeryused_apiurl="http://api.yeelink.net/v1.0/device/357296/sensor/405366/datapoints"

if __name__=='__main__':
    while 1:
        #上传cpu温度
        cpu_temp=getcputemperature()
        cputemp_payload={'value':cpu_temp}
        r=requests.post(cputemp_apiurl, headers=apiheaders, data=json.dumps(cputemp_payload))
        print "CPU温度:%r'C。" % cpu_temp

        #上传cpu占用率及内存使用率
        tempcpuused=getcpuused()

        for cpuline in tempcpuused:

            if cpuline[:3]=="%Cp":
                #cpulineused=cpuline.split(":")[1].split(",")[0].strip("us").split(" ")[1]
                cpulineused=cpuline.split(":")[1].split(",")[0].split(" ")[-2]
                cpuused_payload={'value':cpulineused}
                r=requests.post(cpuused_apiurl, headers=apiheaders, data=json.dumps(cpuused_payload))
                print "CPU已使用："+cpulineused

            if "Mem:" in cpuline:
                #提取数值，仅用字符串操作时，发现在数值前后有多个不可见字符，这里没怎么搞清楚这些字符是些什么
                memlineused=cpuline.split(":")[1].split(",")[1].strip("used").split(" ")[-2]
                memlinetotal=cpuline.split(":")[1].split(",")[0].strip("total").split(" ")[-2]
                memeryusedratio=float(str(memlineused))/float(str(memlinetotal))
                memeryusedratiostr="%.2f"%(memeryusedratio*100)
                memeryused_payload={'value':memeryusedratiostr}
                r=requests.post(memeryused_apiurl, headers=apiheaders, data=json.dumps(memeryused_payload))
                
                print "内存已使用：%r" % memeryusedratiostr
                print "================"
        time.sleep(20)
