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
    
def animate(a):
    #returns the week day as a number (monday = 0)
    dayOfWeek = datetime.today().weekday()
    y_pos = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    #x axis
    y_posInt = [1,2,3,4,5,6,7]
    for i in range(7):
        y_posInt[dayOfWeek - i] = 7 - i

    #calories per day (y axis)
    performance = [0,0,0,0,0,0,0]
    graph_data = open('record.txt','r').read()

    graph_data.split('\n')
    
    #calculating date 7 days ago

    #makes sure not to delete the calories in the middle of the day
    #want to track everything for the past 6 days + the hours in today
    now = datetime.now()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    lastWeek = 144 + now.hour
    cutOffDate = now - timedelta(hours = lastWeek)



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
    plt.cla()
    plt.xticks(y_posInt, y_pos, rotation=30)
    plt.ylim(0,500)
    #plt.bar(x value of bar graph, height of bar graph)
    return plt.bar(y_posInt, performance, color=("#4286f4"), align='center')
    
    
def setUpBar():
    
    #style.use("dark_background")
    #style.use("classic")
    #style.use("grayscale")
    #style.use("ggplot")
    style.use("seaborn-dark")
    #style.use("seaborn-darkgrid")
    fig = plt.figure()
    plt.ylabel('Calories')
    #changes the space at the botton of the graph for the x labels
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.title('Calories by Weekday')
    
    fig.canvas.set_window_title('Consumption Of Calories')
    ani = animation.FuncAnimation(fig, animate, interval=5000, blit=True)
    plt.show()


if __name__ == "__main__":
    setUpBar()
