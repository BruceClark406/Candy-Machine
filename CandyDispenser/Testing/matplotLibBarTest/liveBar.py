import matplotlib.animation as animation
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


from datetime import datetime, timedelta



##import datetime
##from datetime import datetime, timedelta

fig = plt.figure()
y_pos = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
y_posInt = [1,2,3,4,5,6,7]

def whichDate(day):
    for i in range (len(y_pos)):
        if day == y_pos[i]:
            return i


def animate(i):
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

           
    plt.bar(y_posInt, performance, color=("#4286f4"), align='center')
            


ani = animation.FuncAnimation(fig, animate, interval=3000)
plt.show()
