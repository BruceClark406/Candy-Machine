#when the pir sensor is activiated, move the servo 180 degrees

import RPi.GPIO as GPIO
import time

#setup the PIR sensor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

#set up the button
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def moveServo(dutyCycle):
    #sets up GPIO pin 4 as output (servo motor)
    GPIO.setup(4,GPIO.OUT)

    #set pin four to Pulse Width Modulation with 50hz frequency
    p = GPIO.PWM(4,50)
    
    #duty cycle of 7.5, this is the neutral postion
    #2.5 and 12.5 are the extremes
    dutyCycle = float(dutyCycle)
    p.start(dutyCycle)
    p.ChangeDutyCycle(dutyCycle)    

    #must give the srevo enough time to fully rotate                                
    time.sleep(.4)
    p.stop()


def getDutyCycle(dutyCycle):
    if dutyCycle == 2.5:
        dutyCycle = 12.5
    else:
        dutyCycle = 2.5
    return dutyCycle


def useBotton(dutyCycle):
    
    
    # present time + 10 seconds
    timeout = time.time() + 10
    while True:
        #if we have reached time out
        #move servo to proper position and return
        if time.time() > timeout:
            moveServo(dutyCycle)
            return
        #else listen for the botton and move the servo accordingly
        else:
            inputState = GPIO.input(27)
            if inputState == False:
                dutyCycle = getDutyCycle(dutyCycle)
                moveServo(dutyCycle)
            

def intruderDetected(dutyCycle):
    
    dutyCycle = getDutyCycle(dutyCycle)
    #trigger the servo once and the use th botton for 
    moveServo(dutyCycle)

    ##dutyCycle = getDutyCyle(dutyCycle)
    useBotton(dutyCycle)
    
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
            #only checks sesnor every .5 seconds
            time.sleep(.5)

            #pir input
            i = GPIO.input(17)
        
            if i == 0:
                print("No candy for you fat lard!")
            elif i == 1:
                print("CANDY!")
                #dutyCycle = intruderDetected(dutyCycle)
                
            elif i !=1 and i != 0:
                print("no sensor detected")
                break
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nthe session has been terminated.")

main()
