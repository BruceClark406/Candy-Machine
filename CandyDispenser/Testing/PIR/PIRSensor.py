##tests the pir Sensor on GPIO pin 17

import RPi.GPIO as GPIO
import time




GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)


try:
    
    time.sleep(1)
    while True:
        i = GPIO.input(17)
        if i == 0:
            print("no intruders", i)
        elif i == 1:
            print("intruder detected", i)
            
        else:
            print("no sensor detected")
            break
        
except KeyboardInterrupt:
    #GPIO.output(17, False)
    GPIO.cleanup()
    i = 0
    print("the session has been terminated.")




