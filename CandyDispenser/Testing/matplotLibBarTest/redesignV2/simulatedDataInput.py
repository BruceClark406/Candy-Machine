import time
import random

def inputFunc():
    #number = random.randrange(10,100)
    number = 10
    time.sleep(5)
    return str(number)


def writeToFile(number):
        
    f = open("record.txt", "a")
    f.write("Date: " + time.strftime("%m/%d/%Y %A ") + "Time: "+
            time.strftime("%I:%M:%S %p ") + "Number: " + number + "\n")
    f.close()
    print("10 added")

def main():
    while True:
        number = inputFunc()
        writeToFile(number)

if __name__ == "__main__":
    main()