import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 5#4
ECHO = 16#18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)



def getDistance():
    GPIO.output(TRIG, True)
    time.sleep(.0001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO) == False:
        start = time.time()

    while GPIO.input(ECHO) == True:
        end = time.time()

    sigTime = end-start

    #cm
    distance = sigTime / .000058 #inches: .000148

    print("Distance: {} cm".format(distance))

def main():
    try:
        while True:
            time.sleep(.2)
            getDistance()
            

    except:
        print("exiting")
        GPIO.cleanup()


main()
