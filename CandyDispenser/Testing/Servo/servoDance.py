import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(27,GPIO.OUT)

p = GPIO.PWM(27,50)
p.start(7.5)

try:
    while True:
        p.ChangeDutyCycle(7.5)
        time.sleep(3)
        p.ChangeDutyCycle(12.5)
        time.sleep(2)
        p.ChangeDutyCycle(2.5)
        time.sleep(1)

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
