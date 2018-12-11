import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711

def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()

DT = 6
SCH = 13

def setUpLoad():
    #takes the two pins we are using (DT, SCH) Labeled on Board
    hx = HX711(DT, SCH)
    hx.set_reading_format("LSB", "MSB")
    
    # HOW TO CALCULATE THE REFFERENCE UNIT
    # To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
    # In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
    # and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
    # If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
    #hx.set_reference_unit(1)
    hx.set_reference_unit(418)
    return hx
    

def getWeight(hx):
    #sensore off and then back on again
    hx.reset()
    #zeros the scale
    hx.tare()

    val = hx.get_weight(5)
    return val
    print(val)
    

def main():
    hx = setUpLoad()
    weight = getWeight(hx)
    print(weight)
    
    
    
main()

cleanAndExit()


##while True:
##    try:        
##        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
##        #val = hx.get_weight(5)
##        val = hx.get_weight()
##        print(val)
##
##        #hx.power_down()
##        #hx.power_up()
##        time.sleep(0.5)
##    except (KeyboardInterrupt, SystemExit):
##        cleanAndExit()
