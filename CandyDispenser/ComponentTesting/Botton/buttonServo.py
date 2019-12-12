#press CTRL+C to exit the program

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)#refer to the pins by the channel name
#GPIO.setmode(GPIO.BOARD)#refer to the pins by number


#set up button
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def listenButton():
    dutyCycle = 7.5
    try:
        while True:
            inputstate = GPIO.input(27)
            if inputstate == False:                
                print("Button Press")
                if dutyCycle == 2.5:
                    dutyCycle = 12.5
                else:
                    dutyCycle = 2.5
                moveServo(dutyCycle)           
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("button has stopped listening, and system has been turned off")

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
    

def main():
    listenButton();

main()
