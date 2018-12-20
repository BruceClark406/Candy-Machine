import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)




def animate(i):
    graph_data = open('record.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    x = []
    i=0
    for line in lines:
        if len(line) > 1:
            x = line.split(" ")
            xs.append(float(i))
            ys.append(float(x[7]))
            i+=1
    ax1.clear()
    ax1.plot(xs, ys)


    
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
