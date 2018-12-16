#when the pir sensor is activiated, move the servo 180 degrees

import RPi.GPIO as GPIO
import tkinter as tk
from tkinter import ttk
import time
import sys
#need class HX711 from file hx711
from hx711 import HX711
from candyTypes import CandySelection
from liveDataBar import *

SERVO = 27
PIR = 17
#Distance Sensor
TRIG = 5
ECHO = 16
TRIGGERDISTANCE = 6 #CM
#Load Cell
DT = 6
SCH = 13
#LED
LED = 25
#SERVO POSITIONS (PWM)
CLOSED = 7.5
OPEN = 10.5



#setup the PIR sensor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)


def cleanAndExit():
    GPIO.cleanup()
    sys.exit()

def setUpLoad():
    #takes the two pins we are using (DT, SCH) 
    hx = HX711(DT, SCH)
    hx.set_reading_format("LSB", "MSB")
    
    # HOW TO CALCULATE THE REFFERENCE UNIT
    # Set reference unit to 1 below and run the program
    #record the average output with nothing on the LOAD CELL (PREOUT) and then put a known weight (ACTUALWEIGHT) on the load cell and record the number(POSTOUT)
    #then stop the porgram and change the ref number below to (POSTOUT-PREOUT)/ACTUALWEIGHT
    # EX: (6683-0)/16 = 417.6875
    hx.set_reference_unit(418.8322)

    #sensore off and then back on again
    hx.reset()
    #zeros the scale
    hx.tare()
    
    return hx

def getWeight(hx):
    val1 = hx.get_weight(5)
    val2 = hx.get_weight(5)
    val = val1 - val2
    val = abs(val)
    #if the difference between the two weights is less that four than 4, try again
    if val < 2 :
        print("If nothing came out, you could try to shake me!")
        return 0
    #if the difference is greater than 30, something has gone wrong, try again
    elif (val > 30):
        print("There is no way that much candy came out son!")
        getWeight(hx)
    #else average the values and return the average weight measures
    else:
        weight = val/2
        #return asbsolute value
        return weight


def popUpNotification(calories):
    popup = tk.Tk()
    popup.wm_title("Calorie Kill Count")
    output = "You are about to consume ", calories, " calaries!"
    label = ttk.Label(popup, text=output, font = ("Verdana", 12))
    label.pack(side="top", fill="x", padx=20, pady=20)

    #after 3 second destroy the alert
    popup.after(3000, lambda: popup.destroy())
    popup.mainloop()


def recordAction(weight, candyInst):
    #if weight has not changed, stop
    if weight < 3:
        return

    ratio = candyInst.getCandySelectedRatio()

    calories = weight/ratio

    #call the pop up, to notify calorie consumption 
    popUpNotification(calories)
    
    #append onto a file
    f = open("record.txt", "a")
    f.write("Date: " + time.strftime("%m/%d/%Y %A ") + "Time: "+
            time.strftime("%I:%M:%S %p ") + "Calories: " + calories + "\n")
    f.close()
    #change the bar graph
    animate()

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

def turnLightOn():
    GPIO.output(LED, GPIO.HIGH)
    
def turnLightOff():
    GPIO.output(LED, GPIO.LOW)


def getDistance():
    GPIO.output(TRIG, True)
    time.sleep(.00001)
    GPIO.output(TRIG, False)
    
    check = time.time() + 2

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

def selectCandy():
    #making new instance of Candy Class
    candyInstance = CandySelection()

    #asking user to select Candy
    candyInstance.selectCandy()
    
    return candyInstance




def candy(hx, candyInst):
    turnLightOn()

    #scale starts at zero and then as candy dropps out goes negative
    hx.tare()
    
    # present time + 15 seconds
    timeout = time.time() + 15
    while True:
        
        #if we have reached time out
        #move servo to proper position and return
        if time.time() > timeout:
            moveServoDefault()
            return
        #else listen for the botton and move the servo accordingly
        elif(getDistance()):
            moveServo()
            stopWeight = getWeight(hx)
            if stopWeight != 0:
                #record the number of calories in the file, send alert
                recordAction(stopWeight, candyInst)
    
    turnLightOff()
    #time to make sure it is not activated twice
    time.sleep(1)

    

def main():
    #move arm to closed position
    moveServoDefault()

    #asks user what candy is in machine and record it
    candyInst = selectCandy()
    
    #set up load cell
    hx = setUpLoad()

    #initize visual
    setUpBar()
    
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
            elif i == 1:
                print("CANDY!")
                candy(hx, candyInst)
        
    except KeyboardInterrupt:
        print("\nThe session has been terminated...")
        cleanAndExit()
        

if __name__ == "__main__":
    main()