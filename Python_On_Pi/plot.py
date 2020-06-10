from mpl_toolkits import mplot3d
import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')
#x = [1]
#y = [1]
#z = [1]
#ax.scatter(x, y, z, c = 'r',marker = 'o')


def animate(i):
    graph_data = open('sample.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    zs = []
    for line in lines:
        if len(line) > 1 :
            x,y,z,k = line.split(' ')
            xs.append(float(x))
            ys.append(float(y))
            zs.append(float(z))

    ax.clear()
    ax.scatter(xs, ys, zs, c = 'b',marker = 'o')

ani = animation.FuncAnimation(fig, animate, interval = 1000)
plt.show()
