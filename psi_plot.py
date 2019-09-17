import argparse
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Ellipse, Circle, Rectangle
from numpy import loadtxt
import random
from collections import deque
from matplotlib import colors as mcolors

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
rect_width = 0.4
rect_height = 0.4
square_length = 0.35

pre_x = 0
pre_y = 0

dq = deque(maxlen=60)

scenario_dist = {
  "queue": [(1, 1, 90), (2, 2, 90), (3, 3, 90)],
  "art": [(1, 1, 180)],
  "formation": [(1, 1, 90), (2, 2, 180), (3, 3, 270)]
}# initial dummy dictionary

parser = argparse.ArgumentParser()

parser.add_argument('file1', help='Path to the traditional trajectory file')
parser.add_argument('file2', help='Path to the social trajectory file')
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

data = get_data(args.file1)
san_data = get_data(args.file2)
print (data.shape)
animation_count = data.shape[0]

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(0, 25), ylim=(0, 25))
# ax.axis('off')
ax.set_xticks([])
ax.set_yticks([])
ax.grid(color='k', linestyle=':', linewidth=0.25)
ax.plot(0,0, '.c', label='Human')
ax.plot(0,0, '.r', label='Robot')
ax.plot(0,0, colors['darkgray'], label='Art work')
# patch = Ellipse(xy=(0.5, 0.5), width=0.5, height=0.2, angle=60)
# patch1 = Circle((5, -5), 0.1, fc='k')

# Create a Rectangle patch
rect = Rectangle(xy=(3,3), width=rect_width, height=rect_height, fc='r')
#square = Rectangle(xy=(3,3), width=square_length, height=square_length, fc='k')
#furniture = Rectangle(xy=(16,12-1.5), width=1, height=3, fc=colors['saddlebrown'])
frame1 = Rectangle(xy=(24.5,10-1.5), width=0.5, height=3, fc=colors['darkgray'])
frame2 = Rectangle(xy=(24.5,15-1.5), width=0.5, height=3, fc=colors['darkgray'])
frame3 = Rectangle(xy=(24.5,5-1.5), width=0.5, height=3, fc=colors['darkgray'])

#Add people as list comprehension
people = [Ellipse(xy=(people_pose[i][0], people_pose[i][1]),
                width=1.0, height=0.4,
                angle=people_pose[i][2], fc='c')
        for i in range(num_people)]

heads = [Circle((people_pose[i][0], people_pose[i][1]), radius=0.2, fc='k')
        for i in range(num_people)]

for person in people:
    ax.add_patch(person)
for head in heads:
    ax.add_patch(head)

t_x = 5
t_y = 5

rect.xy=(data[0, 0]-0.2, data[0, 1]-0.2) 
ax.add_patch(rect)
# ax.add_patch(furniture)
ax.add_patch(frame1)
ax.add_patch(frame2)
ax.add_patch(frame3)

ax.plot(data[:, 0], data[:, 1], 'k', linewidth=2.0, label='Traditional Trajectory')
ax.plot(san_data[:, 0], san_data[:, 1], 'b', linewidth=2.0, label='Social Trajectory')

# def animate(i):
#     # print (i)
#     global pre_y, pre_x, dq
#     x, y = rect.xy
#     # x = 5 + 3 * np.sin(np.radians(i))
#     # y = 5 + 3 * np.cos(np.radians(i))
#     x = data[i, 0]
#     y = data[i, 1]
#     alpha = np.rad2deg(np.arctan2(y - pre_y, x - pre_x))
#     dq.append(alpha)
#     angle = np.mean(dq)
#     rect.xy = (x - np.sqrt(2)*rect_height/2*np.cos(np.radians(45+angle)), y -np.sqrt(2)*rect_height/2*np.sin(np.radians(45+angle)))
#     rect.angle = angle


#     pre_x = x
#     pre_y = y
#     lst = []
#     lst.append(rect)

#     lst.append(frame1)
#     lst.append(frame2)
#     lst.append(frame3)

#     for index, person in enumerate(people):
#         if random.uniform(0, 9) <= 1:
#             if person.angle == 90 or person.angle == 270:
#                 person.center = (people_pose[index][0], people_pose[index][1]+random.uniform(-0.03, 0.03))
#                 heads[index].center = (people_pose[index][0], people_pose[index][1]+random.uniform(-0.03, 0.03))
#             else:
#                 person.center = (people_pose[index][0]+random.uniform(-0.03, 0.03), people_pose[index][1])
#                 heads[index].center = (people_pose[index][0]+random.uniform(-0.03, 0.03), people_pose[index][1])
#         lst.append(person)
#         lst.append(heads[index])
#     return lst

# anim = animation.FuncAnimation(fig, animate, 
#                                init_func=init, 
#                                frames=animation_count, 
#                                interval=100,
#                                blit=True)

ax.legend()

if args.save == "1":
    #Save the animation
    # anim.save('animation.mp4', fps=30, 
    #       extra_args=['-vcodec', 'h264', 
    #                   '-pix_fmt', 'yuv420p'])
    pass
else:
    #Show animation
    plt.show()