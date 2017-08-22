import RPi.GPIO as GPIO
import time, os
from weather import handle

BUTTON = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)

while True:
    state = GPIO.input(BUTTON)
    if state:
        print("off")
    else:
        print("on")
        handle()
        os.system('mpg123 weather.mp3')
    time.sleep(1)
