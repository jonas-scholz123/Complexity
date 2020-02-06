import sys
import numpy as np
import pickle
from scipy.optimize import curve_fit
from task_2f import get_height_std_dev
from task_2e import get_mean_height

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

#standardise plots
from plot import set_plot_defaults
set_plot_defaults()

def gather_data(system_sizes, total_iterations):
    height_probabilities = {}
    height_std_devs      = {}
    mean_heights         = {}

    for L in system_sizes:
        #OM = OsloModel(L)
        #OM.run(total_iterations)
        name = "OM_"+str(L)+".pkl"
        with open(name, 'rb') as input:
            OM = pickle.load(input)

        height_probabilities[L] = get_height_probability(OM)
        height_std_devs[L]      = get_height_std_dev(OM)
        mean_heights[L]         = get_mean_height(OM)

    return height_probabilities, height_std_devs, mean_heights

def get_height_probability(OM):
    steady_state_heights = OM.height_over_time[OM.first_drop_time:]

    heights, counts = np.unique(steady_state_heights, return_counts = True)
    return dict(zip(heights, counts/len(steady_state_heights)))

def display_data(datapoints):
    for L in datapoints.keys():
        heights = list(datapoints[L].keys())
        counts  = list(datapoints[L].values())
        plt.plot(heights, counts, label = "L = " + str(L))
    plt.legend()
    plt.grid()
    plt.title("Unaltered height probability distribution, P(h;L)")
    plt.xlabel(r"$h$", fontsize = "16")
    plt.ylabel(r"$P(h;L)$")
    plt.show()
    return

def modify_data(height_probabilities_dict, height_std_devs, mean_heights):
    plt.figure(figsize=(12, 8))
    for L in height_probabilities_dict.keys():
        height_probabilities = height_probabilities_dict[L]
        original_x = list(height_probabilities.keys())
        original_y = list(height_probabilities.values())

        # subtract mean to align distributions' center
        # divide by std dev to have x axis in units of std dev

        collapsed_x = (original_x - mean_heights[L])/height_std_devs[L]
        #collapsed_x = (original_x - mean_heights[L])
        collapsed_y = original_y/max(original_y)

        plt.plot(collapsed_x, collapsed_y, "x", label = "L = " + str(L), markersize = 8)
    plt.legend()
    plt.grid()
    plt.title("Collapsed Distribution of P(h;L) at different L")
    plt.xlabel(r"$h - <h>_t$ in units of $\sigma_h$", fontsize = "16")
    plt.ylabel(r"$P(h;L)/P_{max}$")
    plt.show()
    return

system_sizes = [4, 8, 16, 32, 64, 128, 256]
total_iterations = 20000
height_probabilities, height_std_devs, mean_heights= gather_data(system_sizes, total_iterations)

display_data(height_probabilities)
modify_data(height_probabilities, height_std_devs, mean_heights)
