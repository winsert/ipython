from gpiozero import Button
import time
import sys
import os

button = Button(17)

#os.system('amixer sset Headphone 84%')   
while True: 
    if button.is_pressed:
        num = os.system("ps -aux | grep python | awk '/ipython\.py/{print $2}'")
        print (num)
        if not num:
            os.system('python /home/pi/ipython/button_test.py &')
        else:
            os.system("kill -9 $(ps -aux | grep python | awk '/ipython\.py/{print $2}') &")   
    else:
        pass
        
