import RPi.GPIO as GPIO
import time




SERVO = 27
CLOSED = 7
OPEN = 10
TRIG = 5
ECHO = 16
TRIGGERDISTANCE = 8


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def moveServoDefault():
    #making sure candy is not continually falling out of the machine
    #sets up GPIO pin (SERVO) as output (servo motor)
    GPIO.setup(SERVO,GPIO.OUT)

    #set pin four to Pulse Width Modulation with 50hz frequency
    p = GPIO.PWM(SERVO,50)
    
    p.start(CLOSED)
    p.ChangeDutyCycle(CLOSED)
                                
    time.sleep(1)
    p.stop()

def moveServo():
    #sets up GPIO pin (SERVO) as output (servo motor)
    GPIO.setup(SERVO,GPIO.OUT)

    #set pin four to Pulse Width Modulation with 50hz frequency
    p = GPIO.PWM(SERVO,50)
    
    #duty cycle of 7.5, this is the neutral postion
    #2.5 and 12.5 are the extremes
    #must give the srevo enough time to fully rotate
    
    p.start(OPEN)
    
    p.ChangeDutyCycle(OPEN)
    time.sleep(.4)

    p.ChangeDutyCycle(CLOSED)
    time.sleep(.4)
    p.stop()
    
    time.sleep(2)


def getDistance():
    start = 0
    end = 0

    check = time.time() + 1

    #must make sure start gets assigned
    start = 0

    GPIO.output(TRIG, True)
    time.sleep(.00001)
    GPIO.output(TRIG, False)
 
    #sending out the echo
    while GPIO.input(ECHO) == False:
        if check < time.time():
            #since we have such close distances we need to make sure
            #that the echo has not already happend, if it has, try again
            print("distnace sensor failed")
            return 10000
        else:
            start = time.time()

    #recieving the echo
    while GPIO.input(ECHO) == True:
        end = time.time()
    
    #if start is assigned
    if start != 0:
        sigTime = end-start

        #cm
        distance = sigTime / .000058 #inches: .000148
        return distance
    else:
        #we know that start was missed, recurive call untill we get value
        return getDistance()

def getDistanceAverage():
    #making sure a faulty value was not returned
    dist1 = getDistance()
    dist2 = getDistance()

    #only trigger if the hand is closer than 8cm away
    if dist1 < TRIGGERDISTANCE and dist2 < TRIGGERDISTANCE:
        return True
    else:
        return False


def main():
    try:
        while True:
            if (getDistanceAverage()):
                moveServo()
    except KeyboardInterrupt:
        GPIO.cleanup()

main()