import RPi.GPIO as GPIO
import tkinter as tk
from tkinter import ttk
import time
import sys
#need class HX711 from file hx711
from hx711 import HX711
from candyTypes import CandySelection
from liveDataBar import *
import threading
from pynput.keyboard import Key, Controller

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
CLOSED = 7
OPEN = 10
#Pop Up Notification
WIDTHOFPOPUP = 600
HEIGHTOFSCREEN = 200


#setup the PIR sensor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)


def cleanAndExit():
    turnLightOff()
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

    #if the difference between both readings is greater than 30, something has gone wrong
    #making sure the two numbers we pulled from the load cell are reasonable
    i = 0
    while (val > 30):
        if i == 5:
            t1 = threading.Thread(target=popUpNotification, args=(("Error cannot determing calorie count. :("),))
            t1.start()
            print("Error cannot determing calorie count. :(")
            return 0
        print("load cell produced faulty value")
        val1 = hx.get_weight(5)
        val2 = hx.get_weight(5)
        val = val1 - val2
        val = abs(val)
        i+=1
    
    # if readings make sence, take average 
    weight = (val1 + val2)/2
    #if the difference between the two weights is less that four than 4, try again
    if weight < 2:
        t1 = threading.Thread(target=popUpNotification, args=(("If nothing came out, you could try to shake me!"),))
        t1.start()
        print("If nothing came out, you could try to shake me!")
        return 0
    #else average the values and return the average weight measures
    else:
        return weight


def popUpNotification(output):
    popup = tk.Tk()
    popup.wm_title("Calorie Kill Count")
    label = ttk.Label(popup, text=output, font = ("Verdana", 12))
    label.pack(side="top", fill="x", padx=20, pady=20)

    #after 3 second destroy the alert

    widthOfScreen = (popup.winfo_screenwidth() /2) - (WIDTHOFPOPUP/2)
    heightOfScreen = (popup.winfo_screenheight() /2) - (HEIGHTOFSCREEN/2)

    popup.after(3000, lambda: popup.destroy())
    popup.geometry("%dx%d+%d+%d" % (WIDTHOFPOPUP, HEIGHTOFSCREEN, widthOfScreen, heightOfScreen))
    popup.mainloop()


def getCalorieCount(weight, candyInst):
    ratio = candyInst.getCandySelectedRatio()
    calories = weight/ratio
    return int(calories)


def recordAction(calories):
    #append onto a file
    f = open("record.txt", "a")
    f.write("Date: " + time.strftime("%m/%d/%Y %A ") + "Time: "+
            time.strftime("%I:%M:%S %p ") + "Calories: " + calories + "\n")
    f.close()

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


def selectCandy():
    #making new instance of Candy Class
    candyInstance = CandySelection()

    #asking user to select Candy
    candyInstance.selectCandy()
    
    return candyInstance

def triggerd():
    weight = getWeight(hx)
    calories = getCalorieCount(weight, candyInst)
    #if Candy actually came out
    if calories > 3:
        calories = str(calories)
        #record the event in the log
        t1 = threading.Thread(target=recordAction, args=((calories),))
        #call the pop up, to notify calorie consumption 
        t2 = threading.Thread(target=popUpNotification, args=(("You are about to consume %s calaries!" % (calories)),))
        #scale starts at zero and then as candy dropps out goes negative
        t3 = threading.Thread(target=hx.tare)
        t1.start()
        t2.start()
        t3.start()


def candy(hx, candyInst):
    #sets a time for 15 seconds one the PIR sensor is triggerd
    timeOut = time.time() + 15

    while time.time() < timeOut:
        #else listen for the botton and move the servo accordingly
        if(getDistanceAverage()):
            moveServo()
            task = threading.Thread(target=triggerd)
            task.start()

   

def main():
    #move arm to closed position
    moveServoDefault()
    turnLightOff()

    #start an ongoing threat to set up/refresh bar garaph
    task = threading.Thread(target=setUpBar)
    task.start()
    
    #set up load cell
    hx = setUpLoad()

    #creates activity which wakes screen
    keyboard = Controller()

    #asks user what candy is in machine and record it
    candyInst = selectCandy()
    
    try:
        while True:
            #only checks sesnor every .5 seconds
            time.sleep(.5)

            #pir input
            i = GPIO.input(PIR)
        
            if i == 0:
                turnLightOff()
                print("No candy for you fat lard!")
            elif i == 1:
                #creating and event to wake the screen
                keyboard.press(Key.space)
                keyboard.release(Key.space)
                
                turnLightOn()
                print("CANDY!")
                candy(hx, candyInst)
        
    except KeyboardInterrupt:
        print("\nThe session has been terminated...")
        cleanAndExit()
        

if __name__ == "__main__":
    main()