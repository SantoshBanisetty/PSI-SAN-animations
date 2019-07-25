import argparse
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Ellipse, Circle, Rectangle
from numpy import loadtxt
import random

rect_width = 0.5
rect_height = 0.5
square_length = 0.35

pre_x = 0
pre_y = 0

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
    elif scenario == "formation":
        scenario_dist[scenario] = [(11, 12, 90), (13, 14, 0), (15, 12, 270)]
    elif scenario == "art":
        scenario_dist[scenario] = [(22.37, 10.96, 90)]
    else:
        print("Invalid scenario")

update_people(args.scenario)

people_pose = scenario_dist[args.scenario]
num_people = len(people_pose)
print(people_pose)

data = get_data(args.file)
print (data.shape)
animation_count = data.shape[0]

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(0, 25), ylim=(0, 25))
#ax.axis('off')
# ax.set_xticks([])
# ax.set_yticks([])
ax.grid(color='k', linestyle=':', linewidth=0.25)
ax.plot(0,0, '.b', label='Human')
ax.plot(0,0, '.r', label='Robot')
# patch = Ellipse(xy=(0.5, 0.5), width=0.5, height=0.2, angle=60)
# patch1 = Circle((5, -5), 0.1, fc='k')

# Create a Rectangle patch
rect = Rectangle(xy=(3,3), width=rect_width, height=rect_height, fc='r')
#square = Rectangle(xy=(3,3), width=square_length, height=square_length, fc='k')

#Add people as list comprehension
people = [Ellipse(xy=(people_pose[i][0], people_pose[i][1]),
                width=1.0, height=0.4,
                angle=people_pose[i][2])
        for i in range(num_people)]

heads = [Circle((people_pose[i][0], people_pose[i][1]), radius=0.2, fc='k')
        for i in range(num_people)]

def init():
    for person in people:
        ax.add_patch(person)
    for head in heads:
        ax.add_patch(head)
    # patch.center = (5, 5)
    # patch1.center = (5, 5)
    t_x = 5
    t_y = 5
    # rad = np.radians(90)
    # new_x = t_x*np.cos(rad) - t_y*np.sin(rad)
    # new_y = t_x*np.sin(rad) + t_y*np.cos(rad)
    print (t_x, t_y)
    rect.xy=(t_x, t_y) #adjust for lower corner of the rectangle
    #square.xy=(4-square_length/2, 4-square_length/2)
    # ax.add_patch(patch)
    # ax.add_patch(patch1)
    print(rect.angle)
    ax.add_patch(rect)
    #ax.add_patch(square)
    return rect,

def animate(i):
    # print (i)
    global pre_y, pre_x
    x, y = rect.xy
    # x = 5 + 3 * np.sin(np.radians(i))
    # y = 5 + 3 * np.cos(np.radians(i))
    x = data[i, 0]
    y = data[i, 1]
    angle = np.rad2deg(np.arctan2(y - pre_y, x - pre_x))
    rect.xy = (x-rect_width/2, y-rect_height/2)
    #square.xy = (x-square_length/2, y-square_length/2)
    rect.angle = angle + 90
    #square.angle = angle + 90

    pre_x = x
    pre_y = y
    lst = []
    lst.append(rect)
    #lst.append(square)

    for index, person in enumerate(people):
        #p_x, p_y = person.center
        if person.angle == 90 or person.angle == 270:
            person.center = (people_pose[index][0], people_pose[index][1]+random.uniform(-0.025, 0.025))
            heads[index].center = (people_pose[index][0], people_pose[index][1]+random.uniform(-0.025, 0.025))
        else:
            person.center = (people_pose[index][0]+random.uniform(-0.025, 0.025), people_pose[index][1])
            heads[index].center = (people_pose[index][0]+random.uniform(-0.025, 0.025), people_pose[index][1])
        lst.append(person)
        lst.append(heads[index])
    return lst

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=animation_count, 
                               interval=100,
                               blit=True)

ax.legend()

if args.save == "1":
    #Save the animation
    anim.save('animation.mp4', fps=10, 
          extra_args=['-vcodec', 'h264', 
                      '-pix_fmt', 'yuv420p'])
else:
    #Show animation
    plt.show()