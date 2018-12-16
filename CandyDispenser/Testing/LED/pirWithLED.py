import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#LED output pin
LED = 25

GPIO.setup(LED, GPIO.OUT)


while True:
    #Turn OFF LED
    GPIO.output(LED, GPIO.HIGH)  
    time.sleep(3)

    #Turn ON LED
    GPIO.output(LED, GPIO.LOW)  
    time.sleep(3)

    
        
