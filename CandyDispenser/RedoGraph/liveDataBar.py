import matplotlib.animation as animation
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib import style
from datetime import datetime, timedelta


dayDict = {"Monday" : 0,
         "Tuesday" : 1,
         "Wednesday" : 2,
         "Thursday" : 3,
         "Friday" : 4,
         "Saturday" : 5,
         "Sunday" : 6}

firstWeekDay = 8
yPosInt = [1,2,3,4,5,6,7]
highestNumber = 0
blit

def animate(a):
    global firstWeekDay
    global yPosInt
    global highestNumber

    firstWeekDay = yPosInt[0]

    #returns the week day as a number (monday = 0)
    dayOfWeek = datetime.today().weekday()
    y_pos = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    
    for i in range(7):
        yPosInt[dayOfWeek - i] = 7 - i


    #this code canges the day of week every animation
    #for i in range(7):
    #    if yPosInt[i] != 7:
    #        yPosInt[i] = yPosInt[i] + 1
    #    else:
    #        yPosInt[i] = 1


    #decides if the day has changed
    dayChange = False
    if firstWeekDay != yPosInt[0]:
        dayChange = True
    yPosInt = yPosInt

    #calories per day (y axis)
    graph_data = open('record.txt','r').read()
    graph_data.split('\n')
    
    #calculating date 7 days ago

    #makes sure not to delete the calories in the middle of the day
    #want to track everything for the past 6 days + the hours in today
    now = datetime.now()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    lastWeek = 144 + now.hour
    cutOffDate = now - timedelta(hours = lastWeek)

    performance = [0,0,0,0,0,0,0]
    #reading the file from back to front
    for line in reversed(list(open("record.txt"))):
        if len(line) > 1:
            #split up the line
            singleLine = line.split(" ")

            #grab the date "11/01/2018"
            numberDate = singleLine[1].split("/")
            
            # if date in folder is greater than the cuttOff date, include it in graph
            if datetime(int(numberDate[2]), int(numberDate[0]), int(numberDate[1]))  >= cutOffDate:
                #grab the week day "Thursday"
                dayNum = dayDict[singleLine[2]]
                performance[dayNum] += int(singleLine[7])
            #once we have hit this else statement, we are beyond the cutoff date
            else:
                break
    #clear the axis on the graph
    #plt.cla()
    plt.xticks(yPosInt, y_pos, rotation=30)
    #plt.bar(x value of bar graph, height of bar graph)
    if max(performance) > highestNumber or dayChange == True:
        highestNumber = max(performance)
        plt.draw()
        print("Had to redraw")
    return plt.bar(yPosInt, performance, color=("#4286f4"), align='center')
    
    
    
def setUpBar():
    
    style.use("seaborn-dark")
    #style.use("seaborn-darkgrid")
    fig = plt.figure()
    plt.ylabel('Calories')
    #changes the space at the botton of the graph for the x labels
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.title('Calories by Weekday')
    
    fig.canvas.set_window_title('Consumption Of Calories')
    ani = animation.FuncAnimation(fig, animate, interval=5000, blit=False)
    plt.show()
    


if __name__ == "__main__":
    setUpBar()