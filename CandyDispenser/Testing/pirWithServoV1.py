#when the pir sensor is activiated, move the servo 180 degrees

import RPi.GPIO as GPIO
import time

#setup the PIR sensor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

def moveServo(dutyCycle):
    #sets up GPIO pin 4 as output (servo motor)
    GPIO.setup(4,GPIO.OUT)

    #set pin four to Pulse Width Modulation with 50hz frequency
    p = GPIO.PWM(4,50)
    
    #duty cycle of 7.5, this is the neutral postion
    #2.5 and 12.5 are the extremes
    p.start(dutyCycle)
    p.ChangeDutyCycle(dutyCycle)    

    #must give the srevo enough time to fully rotate                                
    time.sleep(.4)
    p.stop()


def intruderDetected(dutyCycle):
    if dutyCycle == 2.5:
        dutyCycle = 12.5
    else:
        dutyCycle = 2.5



    
    moveServo(dutyCycle)
    #time to make sure it is not activated twice
    time.sleep(3)
    return dutyCycle


def main():
    #we are setting duty cycle to 7.5 (neutral)
    dutyCycle = 7.5
    
    try:
        #give PIR sensor time to warm up
        time.sleep(2)
        
        while True:
            time.sleep(.5)
            i = GPIO.input(17)
        
            if i == 0:
                print("no intruders", i)
            elif i == 1:
                print("intruder detected", i)
                dutyCycle = intruderDetected(dutyCycle)
                
            else:
                print("no sensor detected")
                break
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nthe session has been terminated.")

main()
