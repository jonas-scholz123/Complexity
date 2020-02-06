import sys
import numpy as np
import pickle
from task_2e import get_mean_height
from scipy.optimize import curve_fit

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

#standardise plots
from plot import set_plot_defaults
set_plot_defaults()

def gather_data(system_sizes, total_iterations):
    height_std_devs      = {}

    for L in system_sizes:
        #OM = OsloModel(L)
        #OM.run(total_iterations)
        name = "OM_"+str(L)+".pkl"
        with open(name, 'rb') as input:
            OM = pickle.load(input)

        height_std_devs[L] = get_height_std_dev(OM)
    return height_std_devs

def get_height_std_dev(OM):
    ''' Gets average height after first dropped grain'''

    sq_heights_over_time = [h*h for h in OM.height_over_time[OM.first_drop_time:]]
    mean_squared_height = get_mean_squared_height(OM)
    mean_height_squared = get_mean_height(OM)**2

    return np.sqrt(mean_squared_height - mean_height_squared)

def get_mean_squared_height(OM):
    sq_heights_over_time = [h*h for h in OM.height_over_time[OM.first_drop_time:]]
    return np.average(sq_heights_over_time)

def fit_func(L, A, gamma):
    return A*L**gamma

if __name__ == "__main__":
    system_sizes = [4, 8, 16, 32, 64, 128, 256]
    total_iterations = 100000
    height_std_devs = gather_data(system_sizes, total_iterations)

    fit, cov = curve_fit(fit_func, system_sizes, list(height_std_devs.values()))

    A = fit[0]
    gamma = fit[1]
    print("gamma = ", gamma)


    plt.loglog(system_sizes, list(height_std_devs.values()), "x", label = "Measured Std. Deviations")
    plt.loglog(system_sizes, fit_func(system_sizes, A, gamma), ":", label = "Fit")
    plt.title(r"Standard Deviation of Height $\sigma_h(L)$ vs L")
    plt.xlabel("$L$")
    plt.ylabel(r"$\sigma_h(L)$")
    plt.legend()
    plt.grid()
    plt.show()
