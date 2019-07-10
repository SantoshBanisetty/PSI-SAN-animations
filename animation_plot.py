import argparse
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Ellipse, Circle

scenario =	{
  "queue": [(1, 1, 90), (2, 2, 90), (3, 3, 90)],
  "art": [(1, 1, 180)],
  "formation": [(1, 1, 90), (2, 2, 180), (3, 3, 270)]
}

parser = argparse.ArgumentParser()

parser.add_argument('file', help='Path to the file')
parser.add_argument('scenario', help='SAN scenario[queue, art, formation]')
parser.add_argument('--save', help='1 to save the animation')

args = parser.parse_args()
print(args)

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
patch = Ellipse(xy=(0.5, 0.5), width=0.5, height=0.2, angle=60)
patch1 = Circle((5, -5), 0.1, fc='k')

def init():
    patch.center = (5, 5)
    patch1.center = (5, 5)
    ax.add_patch(patch)
    ax.add_patch(patch1)
    return patch, patch1

def animate(i):
    x, y = patch.center
    x = 5 + 3 * np.sin(np.radians(i))
    y = 5 + 3 * np.cos(np.radians(i))
    patch.center = (x, y)
    patch1.center = (x, y)
    return patch, patch1

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=100,
                               blit=True)

plt.show()