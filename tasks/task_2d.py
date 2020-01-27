import sys
import numpy as np
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
    for L in list(avg_tcs.keys())[1:] + [2]: #have 2 at end to stay consistent in colourscheme
        tc = avg_tcs[L]
        processed_height = processed_heights[L]
        t = np.logspace(0, np.log10(total_iterations), 50, dtype = int) #ensures even spacing of datapoints in log log plot

        x = t/tc
        y = 1/(t**(tau)) * processed_height[t - 1]
        plt.loglog(x, y, "", label = "L = " + str(L))
    plt.title("Scaling Function $\mathcal{F}(t/t_c)$ vs scaled time $t/t_c$")
    plt.xlabel("$t/t_c$")
    plt.ylabel("$\mathcal{F}(t/t_c)$")
    plt.legend()
    plt.grid()
    plt.show()
    return


total_iterations   = 90000
number_repetitions = 5 #number of simulation runs at every L to obtain processed height
system_sizes       = [2, 4, 8, 16, 32, 64, 128, 256]

processed_heights, avg_tcs = gather_data(system_sizes, total_iterations, number_repetitions)

#for tau in [0.5, 0.55, 0.6]:
#    display_data(total_iterations, avg_tcs, processed_heights, tau = tau)
display_data(total_iterations, avg_tcs, processed_heights)


for L in processed_heights.keys():
    t = np.logspace(0, np.log10(total_iterations), 50, dtype = int) #ensures even spacing of datapoints in log log plot
    plt.loglog(t, [processed_heights[L][time - 1] for time in t])
plt.show()


#processed_heights_over_time = {}

#for L in system_sizes:
#    height_arrays = []
#    for i in range(number_repetitions):
#        OM = OsloModel(L)
#        OM.run(total_iterations)
#        #t = np.array(range(total_iterations - averaging_range + 1)) #for linear plot
#        #t = np.logspace(0, np.log10(total_iterations- averaging_range), 50, dtype = int) #ensures even spacing of datapoints in log log plot
#        height_arrays.append(OM.height_over_time)
#
#    processed_heights_over_time[L] = processed_height(height_arrays)
#
#for L in system_sizes:
#    t = np.logspace(0, np.log10(total_iterations), 50, dtype = int) #ensures even spacing of datapoints in log log plot
#    processed_height = processed_heights_over_time[L]
#    processed_height = [processed_height[time - 1] for time in t]
#    plt.loglog(t, processed_height, "x")
#plt.show()
