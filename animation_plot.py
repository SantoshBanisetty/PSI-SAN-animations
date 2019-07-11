import argparse
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Ellipse, Circle, Rectangle
from numpy import loadtxt

rect_width = 0.5
rect_height = 0.3
square_length = 0.2

scenario_dist = {
  "queue": [(1, 1, 90), (2, 2, 90), (3, 3, 90)],
  "art": [(1, 1, 180)],
  "formation": [(1, 1, 90), (2, 2, 180), (3, 3, 270)]
}# initial dummy dictionary

parser = argparse.ArgumentParser()

parser.add_argument('file', help='Path to the file')
parser.add_argument('scenario', help='SAN scenario[queue, art, formation]')
parser.add_argument('--save', help='1 to save the animation')

args = parser.parse_args()
print(args)

def get_data(file):
    np_data = loadtxt(file, delimiter='\t') # skips header
    return np_data

#Update function to replace dictionary values
def update_people(scenario):
    if scenario == "queue":
        scenario_dist[scenario] = [(11, 12, 90), (13, 12, 90), (15, 12, 90)]
    if scenario == "formation":
        scenario_dist[scenario] = [(11, 12, 90), (13, 14, 0), (15, 12, 270)]
    if scenario == "art":
        scenario_dist[scenario] = [(22.37, 10.96, 90)]
    else:
        print("Invalid scenario")

update_people(args.scenario)

people_pose = scenario_dist[args.scenario]
num_people = len(people_pose)
print(people_pose)

print (get_data(args.file))

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(0, 25), ylim=(0, 25))
ax.grid(color='k', linestyle=':', linewidth=0.25)
patch = Ellipse(xy=(0.5, 0.5), width=0.5, height=0.2, angle=60)
patch1 = Circle((5, -5), 0.1, fc='k')

# Create a Rectangle patch
rect = Rectangle(xy=(3,3), width=rect_width, height=rect_height, fc='r')
square = Rectangle(xy=(3,3), width=square_length, height=square_length, fc='k')

#Add people as list comprehension
people = [Ellipse(xy=(people_pose[i][0], people_pose[i][1]),
                width=0.5, height=0.2,
                angle=people_pose[i][2])
        for i in range(num_people)]

heads = [Circle((people_pose[i][0], people_pose[i][1]), 0.1, fc='k')
        for i in range(num_people)]

def init():
    for person in people:
        ax.add_patch(person)
    for head in heads:
          ax.add_patch(head)
    patch.center = (5, 5)
    patch1.center = (5, 5)
    rect.xy=(4-rect_width/2, 4-rect_height/2) #adjust for lower corner of the rectangle
    square.xy=(4-square_length/2, 4-square_length/2)
    ax.add_patch(patch)
    ax.add_patch(patch1)
    ax.add_patch(rect)
    ax.add_patch(square)
    return patch, patch1, rect, square

def animate(i):
    x, y = patch.center
    x = 5 + 3 * np.sin(np.radians(i))
    y = 5 + 3 * np.cos(np.radians(i))
    patch.center = (x, y)
    patch1.center = (x, y)
    return patch, patch1, rect, square

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=100,
                               blit=True)

plt.show()