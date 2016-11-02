import glob
import math
import sys
from abc import ABC, abstractmethod
import operator
import time

class Item:
    def __init__(self, weight, cost, id):
        self.cost = cost
        self.weight = weight
        self.cost_weight_ratio = cost/weight
        self.id = id


class Brute_force():
    def solve(self, id, n, max_weight, items):
        max_cost = 0
        max_config_var = []

        for i in range(int(math.pow(2, n))):
            temp = list('{:040b}'.format(i)) # Makes a list of 0 or 1 for example [0,1,1,1,0]
            config_var = temp[-n:]

            cost = 0
            weight = 0
            for index, xi in enumerate(config_var):
                if xi == '1':
                    cost += items[index].cost
                    weight += items[index].weight
                if weight > max_weight: # Dont bother with to heavy config_vars
                    break

            if cost > max_cost and weight <= max_weight:
                max_cost = cost
                max_config_var = config_var


        config_var_str = " ".join(max_config_var)
        return (max_cost, '{:s}'.format(config_var_str))

class Greedy():
    def solve(self, id, n, max_weight, items):
        max_config_var = []
        items.sort(key=operator.attrgetter('cost_weight_ratio'), reverse=True)

        weight = 0
        cost = 0
        for item in items:
            if weight + item.weight <= max_weight:
                weight += item.weight
                cost += item.cost
                max_config_var.append(item.id)

        config_var = [0] * n # Creates a list of size n filled with 0
        for var in max_config_var:
            config_var[var] = 1

        config_var_str = " ".join(map(str, config_var))
        return (cost, '{:s}'.format(config_var_str))


def choose_algorithm(algorithm_type):
    if algorithm_type == 'bruteforce':
        return Brute_force()
    elif algorithm_type == 'greedy':
        return Greedy()
    else:
        print('Wrong input: size algorithm number_loops(optional)')
        sys.exit(1)

def format_input_variables(instance):
    input_var = instance.split()
    return list(map(int, input_var)) # Converts from string to int


def read_file(path):
    file = open(path, 'r')
    return file.read().splitlines()


def write_file(lines_output, path):
    file = open(path, 'w')
    file.write(lines_output)

def check_results(algorithm, instance_size):
    sol_path = 'sol/knap_{:s}.sol.dat'.format(instance_size)
    sol_file = read_file(sol_path)

    computed_sol_path = 'output/{:s}/{:s}.dat'.format(algorithm, instance_size)
    computed_sol_file = read_file(computed_sol_path)

    nbr_correct = 0
    nbr_failed = 0
    relative_errors = []
    for i in range(len(sol_file)):
        sol_line = format_input_variables(sol_file[i])

        computed_sol_line = format_input_variables(computed_sol_file[i])

        if sol_line[2] == computed_sol_line[2]:
            nbr_correct += 1
        else:
            nbr_failed += 1
            r_error = (sol_line[2] - computed_sol_line[2]) / sol_line[2]
            relative_errors.append(r_error)

    return (relative_errors, len(relative_errors) / len(sol_file))


# =*==*=*=*=*=*=*=START=*==*=*=*=*=*=*=
instance_size = sys.argv[1]
path = 'inst/knap_{:s}.inst.dat'.format(instance_size)
problem_instances = read_file(path)
algorithm_type = sys.argv[2]
algorithm = choose_algorithm(algorithm_type)

if len(sys.argv) > 3:
    nbr_loop = int(sys.argv[3])
else:
    nbr_loop = 1


output_string = ""
nbr_instances = len(problem_instances)

start_time = time.time()
for instance in problem_instances:
    instance = format_input_variables(instance)
    id = instance.pop(0)
    n = instance.pop(0)
    max_weight = instance.pop(0)
    items = []

    for i in range(0, n, 1):
        item = Item(instance[i*2], instance[i*2+1], i)
        items.append(item)

    for i in range(int(nbr_loop)):
        solution = algorithm.solve(id, n, max_weight, items)
    max_cost = solution[0]
    max_config_var = solution[1]
    solution_string = '{:d} {:d} {:d}  {:s}'.format(id, n, max_cost, max_config_var)
    output_string += solution_string + '\n'

compute_time = time.time() - start_time

nbr_solves = nbr_instances * nbr_loop
print('The algorithm took approximatley {:f} seconds to run {:d} times'.format(compute_time, nbr_solves))
average_time = compute_time / nbr_solves
time_string = '{:s} {:f}'.format(instance_size, average_time)
time_path = 'time/{:s}/{:s}.dat'.format(algorithm_type, instance_size)
write_file(time_string, time_path)


output_path = 'output/{:s}/{:s}.dat'.format(algorithm_type, instance_size)
write_file(output_string, output_path)

error_tuple = check_results(algorithm_type, instance_size)
error_path = 'error/{:s}/{:s}.dat'.format(algorithm_type, instance_size)
error_string = " ".join(str(item) for item in error_tuple[0])
error_string += ' {:f}'.format(error_tuple[1])
write_file(error_string, error_path)
