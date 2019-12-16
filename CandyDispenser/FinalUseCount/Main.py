import RPi.GPIO as GPIO
import tkinter as tk
from tkinter import ttk
import time
import sys
from candyTypes import CandySelection
import liveDataBar
import threading
import Jokes
from pynput.keyboard import Key, Controller
from joke.jokes import *


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
OPEN = 10.5
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




def popUpNotification():
    popup = tk.Tk()
    label = ttk.Label(popup, text=Jokes.get_joke(), font = ("Verdana", 12), wraplength=WIDTHOFPOPUP-50)
    label.pack(side="top", fill="x", padx=20, pady=20)

    #after 3 second destroy the alert

    widthOfScreen = (popup.winfo_screenwidth() /2) - (WIDTHOFPOPUP/2)
    heightOfScreen = (popup.winfo_screenheight() /2) - (HEIGHTOFSCREEN/2)

    popup.after(7000, lambda: popup.destroy())
    popup.geometry("%dx%d+%d+%d" % (WIDTHOFPOPUP, HEIGHTOFSCREEN, widthOfScreen, heightOfScreen))
    popup.mainloop()



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
    #must give the servo enough time to fully rotate
    
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
    #must make sure start/end gets assigned
    start = 0
    end = 0

    check = time.time() + 1

    GPIO.output(TRIG, True)
    time.sleep(.00001)
    GPIO.output(TRIG, False)
 
    #sending out the echo
    while GPIO.input(ECHO) == False:
        if check < time.time():
            #since we have such close distances we need to make sure
            #that the echo has not already happend, if it has, try again
            #print("distnace sensor failed")
            return 10000
        else:
            start = time.time()

    #receiving the echo
    while GPIO.input(ECHO) == True:
        end = time.time()
    
    #if start is assigned
    if start != 0:
        sigTime = end-start

        #cm
        distance = sigTime / .000058 #inches: .000148
        return distance
    else:
        #we know that start was missed, recursive call until we get value
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
    candyInstance = CandySelection()
    candyInstance.selectCandy()
    return candyInstance

def triggerd(candyInst):
    #record the event in the log
    t1 = threading.Thread(target=recordAction, args=((str(10)),))
    #call the pop up, to notify calorie consumption 
    t2 = threading.Thread(target=popUpNotification,)
    t1.start()
    t2.start()
    #Tell the graph to do a hard refresh
    liveDataBar.blit_bool = False


def candy(candyInst):
    #sets a time for 15 seconds once the PIR sensor is triggered
    timeOut = time.time() + 15

    while time.time() < timeOut:
        #else listen for the botton and move the servo accordingly
        if(getDistanceAverage()):
            moveServo()
            task = threading.Thread(target=triggerd, args=(candyInst,))
            task.start()

   

def main():
    #move arm to closed position
    moveServoDefault()
    turnLightOff()

    #start an ongoing threat to set up/refresh bar garaph
    task = threading.Thread(target=liveDataBar.setUpBar)
    task.start()

    #creates activity which wakes screen
    keyboard = Controller()

    #asks user what candy is in machine and record it
    candyInst = selectCandy()
    
    try:
        while True:
            #only checks sensor every .5 seconds
            time.sleep(.5)

            #pir input
            i = GPIO.input(PIR)
        
            if i == 0:
                turnLightOff()
                #print("No candy for you, fat lard!")
            elif i == 1:
                #creating and event to wake the screen
                keyboard.press(Key.space)
                keyboard.release(Key.space)
                
                turnLightOn()
                #print("CANDY!")
                candy(candyInst)
        
    except KeyboardInterrupt:
        print("\nThe session has been terminated...")
        cleanAndExit()
        

if __name__ == "__main__":
    main()