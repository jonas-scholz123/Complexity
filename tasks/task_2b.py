import sys
import numpy as np

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

nr_repetitions = 3
system_sizes = [4, 8, 16, 32]
total_iterations = 3000

def gather_data(system_sizes, total_iterations, nr_repetitions):
    avg_tc_values = {}

    for L in system_sizes:
        avg_tc_values[L] = get_avg_tc(L, nr_repetitions)
    return avg_tc_values

def get_avg_tc(L, nr_repetitions):
    tc_list = []

    for i in range(nr_repetitions):

        OM = OsloModel(L)
        OM.run(total_iterations)
        tc_list.append(OM.first_drop_time)

    return np.average(tc_list)

def display_data(datapoints):
    x = list(datapoints.keys())
    y = list(datapoints.values())

    plt.loglog(x, y, "x")
    plt.show()

avg_tc_values = gather_data(system_sizes, total_iterations, nr_repetitions)
display_data(avg_tc_values)
