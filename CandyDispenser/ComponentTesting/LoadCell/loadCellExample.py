import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711

#this code is taken and slightly modified from a HX711 Libaray online

def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()

hx = HX711(6, 13)
hx.set_reading_format("LSB", "MSB")

 # HOW TO CALCULATE THE REFFERENCE UNIT
    # Set reference unit to 1 below and run the program
    #record the average output with nothing on the LOAD CELL (PREOUT) and then put a known weight (ACTUALWEIGHT) on the load cell and record the number(POSTOUT)
    #then stop the porgram and change the ref number below to (POSTOUT-PREOUT)/ACTUALWEIGHT
    # EX: (6683-0)/16 = 417.6875
hx.set_reference_unit(418.8322)

hx.reset()
hx.tare()

while True:
    try:
        val = hx.get_weight(5)
        print(val)

        time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
