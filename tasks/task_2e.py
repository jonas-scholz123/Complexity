import sys
import numpy as np
from scipy.optimize import curve_fit
import pickle

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

#standardise plots
from plot import set_plot_defaults
set_plot_defaults()

def gather_data(system_sizes, total_iterations):
    average_heights      = {}

    for L in system_sizes:

        # load OsloModel
        name = "OM_"+str(L)+".pkl"
        with open(name, 'rb') as input:
            OM = pickle.load(input)

        average_heights[L] = get_mean_height(OM)
    return average_heights

def get_mean_height(OM):
    return np.average(OM.height_over_time[OM.first_drop_time:])

def fit_func(L, a_0, a_1, omega_1):
    return a_0 * L * (1 - a_1 * 1/(L**(omega_1)))

if __name__ == "__main__":
    system_sizes = [4, 8, 16, 32, 64, 128, 256]
    total_iterations = 20000
    average_heights = gather_data(system_sizes, total_iterations)

    fit, cov = curve_fit(fit_func, system_sizes, list(average_heights.values()))
    fit_L = np.logspace(np.log10(system_sizes[0]), np.log10(system_sizes[-1]), 300)
    fit_y = fit_func(fit_L, fit[0], fit[1], fit[2])

    plt.loglog(system_sizes, list(average_heights.values()), "x", label = "Measured avg. heights")
    plt.loglog(fit_L, fit_y, ":", label = "First Order Corrected Fit")
    plt.title("Time averaged system height vs L up to first order corrections")
    plt.xlabel("$L$")
    plt.ylabel("$<h(t;L)>_t$")
    plt.legend()
    plt.grid()
    plt.show()
    print("a_0 = ", fit[0])
    print("a_1 = ", fit[1])
    print("omega_1 = ", fit[2])
    print(cov)
