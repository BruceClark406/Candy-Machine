import time


def inputFunc():
    number = input("Give me a string: ")
    return number

def writeToFile(number):
    f = open("record.txt", "a")
    f.write("Date: " + time.strftime("%m/%d/%Y %A ") + "Time: "+
            time.strftime("%I:%M:%S %p ") + "Number: " + number + "\n")
    f.close()



def main():
    while True:
        number = inputFunc()
        writeToFile(number)
main()
