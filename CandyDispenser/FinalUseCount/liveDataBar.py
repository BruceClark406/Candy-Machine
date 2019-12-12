import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from datetime import datetime, timedelta


yPosInt = [1,2,3,4,5,6,7]
performance = [50,60,70,80,90,100,110]
y_pos = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
blit_bool = False
dayDict = {"Monday" : 0,
         "Tuesday" : 1,
         "Wednesday" : 2,
         "Thursday" : 3,
         "Friday" : 4,
         "Saturday" : 5,
         "Sunday" : 6}


def update():
    #x-labels/positions
    global yPosInt
    dayOfWeek = datetime.today().weekday()
    for i in range(7):
        yPosInt[dayOfWeek - i] = 7 - i

    #summing up calories from text file
    global performance
    performance = [0,0,0,0,0,0,0]

    for line in reversed(list(open("record.txt"))):
        if len(line) > 1:
            #split up the line
            singleLine = line.split(" ")

            #grab the date "11/01/2018"
            numberDate = singleLine[1].split("/")

            #set cut off date
            now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            lastWeek = 144 + now.hour
            cutOffDate = now - timedelta(hours = lastWeek)
            
            # if date in folder is greater than the cuttOff date, include it in graph
            if datetime(int(numberDate[2]), int(numberDate[0]), int(numberDate[1]))  >= cutOffDate:
                #grab the week day "Thursday"
                dayNum = dayDict[singleLine[2]]
                performance[dayNum] += int(singleLine[7])
            #once we have hit this else statement, we are beyond the cutoff date
            else:
                break

def animate(a):
    global blit_bool
    if blit_bool == False:
        print("updated")
        plt.cla()
        update()
        plt.xticks(yPosInt, y_pos, rotation=30)
    blit_bool = True
    return plt.bar(yPosInt, performance, color=("#4286f4"), align='center')



def setUpBar():    
    fig = plt.figure()
    style.use("seaborn-dark")
    plt.title('Calories by Weekday')
    fig.canvas.set_window_title('Consumption Of Calories')
    plt.ylabel('Calories')
    #changes the space at the botton of the graph for the x labels
    plt.gcf().subplots_adjust(bottom=0.15)
    ani = animation.FuncAnimation(fig, animate, interval=10000, blit=blit_bool)
    plt.show()




if __name__ == "__main__":
    setUpBar()