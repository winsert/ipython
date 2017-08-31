from gpiozero import Button
import time
import sys
import os

button = Button(17)

count = 0
dingdangrun = False
#os.system('amixer sset Headphone 76%')
while True: 
    if button.is_pressed:
        time.sleep(0.015)
        if button.is_pressed:
            now = time.time()
            while button.is_pressed and time.time() - now < 1:
                pass
            if button.is_pressed:
                if not dingdangrun:
                    os.system('python /home/pi/ipython/button_test.py &')
                    dingdangrun = True
                else:
                    count += 1
                    if count == 2:
                        dingdangrun = False
                        count = 0
                        os.system("ps -ef|grep "button_test.py"|grep -v grep |awk '{print "kill -9 "$2}' | sh &")
                while button.is_pressed:
                    pass
            else:
                count = 0
    time.sleep(0.010)
