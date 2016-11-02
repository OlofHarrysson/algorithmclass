import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import glob
import sys
import re


def read_data(path):
    file = open(path, 'r')
    return file.read().splitlines()

# =*==*=*=*=*=*=*=START=*==*=*=*=*=*=*=
algorithm_type = sys.argv[1]
path = 'error/{:s}/*.dat'.format(algorithm_type)

files = glob.glob(path)
avg_rel_error = []
percent_error = []
max_rel_error = []
for name in files:
    instance_size = re.sub("\D", "", str(name))
    file = open(name, 'r')
    temp = file.read().split(" ")
    temp = list(map(float, temp))
    incorrect_ratio = temp.pop()
    percent_error.append([instance_size, incorrect_ratio])
    max_rel_error.append([instance_size, max(temp)])
    avg_rel_error.append([instance_size, sum(temp) / float(len(temp))])




fig = plt.figure(1)
plt.ylabel('Relative Error')
plt.xlabel('Instance Size')
plt.ylim((0, 0.5))

plt.scatter(*zip(*max_rel_error), color='red')
red_patch = mpatches.Patch(color='red', label='Max Error')

plt.scatter(*zip(*avg_rel_error), color='blue')
blue_patch = mpatches.Patch(color='blue', label='Average Error')
plt.legend(handles=[red_patch, blue_patch])

plt.show()
plt.close(fig)


fig = plt.figure(1)
plt.scatter(*zip(*percent_error), color='red')
plt.ylabel('Probability of Incorrect Solution')
plt.xlabel('Instance Size')

plt.show()
plt.close(fig)
