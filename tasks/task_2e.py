import sys
import numpy as np
from scipy.optimize import curve_fit

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

def gather_data(system_sizes, total_iterations):
    average_heights      = {}

    for L in system_sizes:
        OM = OsloModel(L)
        OM.run(total_iterations)

        average_heights[L] = get_mean_height(OM)
    return average_heights

def get_mean_height(OM):
    return np.average(OM.height_over_time[OM.first_drop_time:])

def fit_func(L, a_0, a_1, omega_1):
    return a_0 * L * (1 - a_1 * 1/(L**(omega_1)))

if __name__ == "__main__":
    system_sizes = [4, 8, 16, 32, 64]
    total_iterations = 20000
    average_heights = gather_data(system_sizes, total_iterations)
    #%%
    fit, cov = curve_fit(fit_func, system_sizes, list(average_heights.values()))
    fit_L = np.logspace(np.log10(system_sizes[0]), np.log10(system_sizes[-1]), 300)
    fit_y = fit_func(fit_L, fit[0], fit[1], fit[2])

    plt.loglog(system_sizes, list(average_heights.values()), "x")
    plt.loglog(fit_L, fit_y)
    plt.show()
