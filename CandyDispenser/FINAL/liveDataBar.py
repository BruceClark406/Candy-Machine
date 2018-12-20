import matplotlib.animation as animation
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import time

from datetime import datetime, timedelta


def whichDate(day):
    y_pos = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    for i in range (6):
        if day == y_pos[i]:
            return i
        
#def animate(i):
def animate():
    #returns the week day as a number (monday = 0)
    dayOfWeek = datetime.today().weekday()

    #x axis
    y_posInt = [1,2,3,4,5,6,7]
    y_pos = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

    #orders the y_posInt according to which day it is
    for i in range(7):
        y_posInt[6-i] = dayOfWeek
        if dayOfWeek == 0:
            dayOfWeek = 6
        else:
            dayOfWeek -= 1

    
    #calaroies per day (y axis)
    performance = [0,0,0,0,0,0,0]
    graph_data = open('record.txt','r').read()

    #grabbing line from file
    lines = graph_data.split('\n')

    #calculting date 7 days ago
    cutOffDate = datetime.now() - timedelta(days = 7)
    
    for line in lines:
        if len(line) > 1:
            #split up the line
            singleLine = line.split(" ")

            #grab the date "11/01/2018"
            numberDate = singleLine[1].split("/")
            
            # if date in folder is greater than the cuttOff date, include it in graph
            if datetime(int(numberDate[2]), int(numberDate[0]), int(numberDate[1]))  > cutOffDate:
                #grab the week day "Thursday"
                dayNum = whichDate(singleLine[2])
                performance[dayNum] += int(singleLine[7])

            plt.xticks(y_posInt, y_pos, rotation=40)
            
            plt.bar(y_posInt, performance, color=("#4286f4"), align='center')
            
def setUpBar():
    fig = plt.figure()
    
    plt.ylabel('Calories')
    #changes the space at the botton of the graph for the x labels
    plt.gcf().subplots_adjust(bottom=0.15)

    plt.title('Calories by Weekday')
    fig.canvas.set_window_title('Consumption Of Calories')
    animate()
    #ani = animation.FuncAnimation(fig, animate, interval=3000)
    plt.show(block=False)

def main():
    time.sleep(5)
    animate()


if __name__ == "__main__":
    setUpBar()
    main()
