import sys
import numpy as np
import pickle
from task_2b import get_avg_tc

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

#standardise plots
from plot import set_plot_defaults
set_plot_defaults()

def get_processed_height(L, total_iterations, number_repetitions):

    height_arrays = []
    for i in range(number_repetitions):
        OM = OsloModel(L)
        OM.run(total_iterations)
        height_arrays.append(OM.height_over_time)
    return np.mean(height_arrays, axis = 0)

def gather_data(system_sizes, total_iterations, number_repetitions):
    processed_heights = {}
    avg_tcs           = {}

    for L in system_sizes:
        processed_heights[L] = get_processed_height(L, total_iterations, number_repetitions)
        avg_tcs[L] = get_avg_tc(L, number_repetitions)
    return processed_heights, avg_tcs

def display_data(total_iterations, avg_tcs, processed_heights, tau = 1/2):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (14, 8))
    for L in list(avg_tcs.keys()): #have 2 at end to stay consistent in colourscheme
        tc = avg_tcs[L]
        processed_height = processed_heights[L]
        t = np.logspace(0, np.log10(total_iterations), 100, dtype = int) #ensures even spacing of datapoints in log log plot
        x = t/(L**2)
        x_scaling_func = t/tc
        y = processed_height[t-1]/L
        y_scaling_func = 1/(t**(tau)) * processed_height[t - 1]
        ax1.loglog(x, y, "", label = "L = " + str(L))
        ax2.loglog(x_scaling_func, y_scaling_func, "")

    ax1.set_title(r"$\tilde{h}(t;L)/L$ vs scaled time $t/L^2$")
    ax2.set_title(r"$\mathcal{F}(t/t_c)$ vs scaled time $t/t_c$")
    ax1.set_xlabel("$t/L^2$")
    ax1.set_ylabel(r"$\tilde{h}(t;L)/L$")
    ax2.set_xlabel(r"$t/t_c$")
    ax2.set_ylabel(r"$\mathcal{F}(t/t_c)$")
    ax1.legend()
    ax1.grid()
    ax2.grid()
    plt.show()
    return


if __name__ == "__main__":
    total_iterations   = 90000
    number_repetitions = 5 #number of simulation runs at every L to obtain processed height
    system_sizes       = [4, 8, 16, 32, 64, 128, 256]

    processed_heights, avg_tcs = gather_data(system_sizes, total_iterations, number_repetitions)

    display_data(total_iterations, avg_tcs, processed_heights)


    for L in processed_heights.keys():
        t = np.logspace(0, np.log10(total_iterations), 50, dtype = int) #ensures even spacing of datapoints in log log plot
        plt.loglog(t, [processed_heights[L][time - 1] for time in t]) #shift time index by 1
    plt.show()
