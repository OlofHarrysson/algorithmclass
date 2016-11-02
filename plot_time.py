import matplotlib.pyplot as plt
import numpy as np
import glob
import sys


def read_data(path):
    file = open(path, 'r')
    return file.read().splitlines()

# =*==*=*=*=*=*=*=START=*==*=*=*=*=*=*=
algorithm_type = sys.argv[1]
path = 'time/{:s}/*.dat'.format(algorithm_type)

files = glob.glob(path)
data = []
for name in files:
    file = open(name, 'r')
    temp = file.read().split(" ")
    float_list = list(map(float, temp))
    data.append(float_list)


# Greedy

# fig = plt.figure()
# plt.scatter(*zip(*data))
# plt.ylabel('Time (s)')
# plt.xlabel('Instance Size')
# plt.ylim((0, 0.00004))


# Brute Force

fig = plt.figure(1)
plt.scatter(*zip(*data))
plt.ylabel('Time (s)')
plt.xlabel('Instance Size')
plt.ylim((0, 10)) # For greedy
plt.xlim((2, 22))


plt.show()
plt.close(fig)
