import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random



def animate(i):
    
    

    x_pos = [1,2,3,4,5,6,7]
    performance = []
    for i in range(7):
        number = random.randrange(0,500)
        performance.append(number)
    print(performance)
    plt.cla()
    
    
    return plt.bar(x_pos, performance, color=("#4286f4"), align='center')


fig = plt.figure()

plt.ylim(0,1000)
ani = animation.FuncAnimation(fig, animate, interval=5000, blit=True)
plt.show()