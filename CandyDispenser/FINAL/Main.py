#when the pir sensor is activiated, move the servo 180 degrees

import RPi.GPIO as GPIO
import time
import sys
#need class HX711 from file hx711
from hx711 import HX711

SERVO = 27
PIR = 17
TRIG = 5
ECHO = 16
TRIGGERDISTANCE = 8



#setup the PIR sensor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def moveServoDefault():
    #making sure candy is not continually falling out of the machine
    #sets up GPIO pin (SERVO) as output (servo motor)
    GPIO.setup(SERVO,GPIO.OUT)

    #set pin four to Pulse Width Modulation with 50hz frequency
    p = GPIO.PWM(SERVO,50)
    
    p.start(4.5)
    p.ChangeDutyCycle(4.5)
                                
    time.sleep(2)
    p.stop()

def moveServo():
    #sets up GPIO pin (SERVO) as output (servo motor)
    GPIO.setup(SERVO,GPIO.OUT)

    #set pin four to Pulse Width Modulation with 50hz frequency
    p = GPIO.PWM(SERVO,50)
    
    #duty cycle of 7.5, this is the neutral postion
    #2.5 and 12.5 are the extremes
    #must give the srevo enough time to fully rotate
    
    p.start(9.5)
    
    p.ChangeDutyCycle(9.5)
    time.sleep(.4)

    p.ChangeDutyCycle(4.5)
    time.sleep(.4)
    p.stop()
    
    time.sleep(2)

def getDistance():
    #time.sleep(.0001)
    GPIO.output(TRIG, True)
    time.sleep(.00001)
    GPIO.output(TRIG, False)
    #time.sleep(1)
    
    check = time.time() + 5

    #sending out the echo
    while GPIO.input(ECHO) == False:
        if check < time.time():
            #since we have such close distances we need to make sure
            #that the echo has not already happend
            return
        else:
            start = time.time()

    #recieving the echo
    while GPIO.input(ECHO) == True:
        end = time.time()
    
    sigTime = end-start

    #cm
    distance = sigTime / .000058 #inches: .000148

    #print("Distance: {} cm".format(distance))

    #only trigger if the hand is closer than 8cm away
    if distance < TRIGGERDISTANCE:
        return True
    else:
        return False



def candy():
    #trigger the servo once and the use then distance sensor 
    moveServo()
    # present time + 10 seconds
    timeout = time.time() + 10
    while True:
        
        #if we have reached time out
        #move servo to proper position and return
        if time.time() > timeout:
            moveServoDefault()
            return
        #else listen for the botton and move the servo accordingly
        elif(getDistance()):
            moveServo()
            
    
    #time to make sure it is not activated twice
    time.sleep(1)
    


def main():
    try:
        #give PIR sensor time to warm up
        time.sleep(2)
        
        while True:
            #only checks sesnor every .5 seconds
            time.sleep(.5)

            #pir input
            i = GPIO.input(PIR)
        
            if i == 0:
                print("No candy for you fat lard!")
            elif i == 1 and getDistance():
                print("CANDY!")
                candy()
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nthe session has been terminated.")

main()
