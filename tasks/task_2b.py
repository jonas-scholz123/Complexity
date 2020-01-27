import sys
import numpy as np
from scipy.optimize import curve_fit

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

#standardise plots
from plot import set_plot_defaults
set_plot_defaults()

system_sizes = [4, 8, 16, 32, 64, 128, 256]
total_iterations = 100000

def gather_data(system_sizes, total_iterations):
    avg_tc_values = {}

    for L in system_sizes:
        nr_repetitions = int(256/L) #higher L requires fewer repetitions
        avg_tc_values[L] = get_avg_tc(L, nr_repetitions)

    L = list(avg_tc_values.keys())
    avg_tc = list(avg_tc_values.values())

    fit, cov = curve_fit(log_power_law, L, np.log10(avg_tc))

    A = fit[0]
    beta = fit[1]
    print(beta)

    return avg_tc_values, A, beta

def log_power_law(L, A, beta):
    return np.log10(A) + beta*np.log10(L)

def get_avg_tc(L, nr_repetitions):
    tc_list = []

    for i in range(nr_repetitions):

        OM = OsloModel(L)
        OM.stop_at_first_drop = True
        OM.run(total_iterations)
        tc_list.append(OM.first_drop_time)

    return np.average(tc_list)

def display_data(datapoints, A, beta):
    x = list(datapoints.keys())
    y = list(datapoints.values())

    plt.loglog(x, y, "x", label = "Measured values")

    #annotate above for low L
    for x_coord, y_coord in zip(x[0:-2], y[0:-2]):
        plt.annotate("L = " + str(x_coord), (x_coord, y_coord*3))
    #annotate below for high L
    for x_coord, y_coord in zip(x[-2:], y[-2:]):
        plt.annotate("L = " + str(x_coord), (x_coord, y_coord/3))

    plt.loglog(x, A*x**beta, ":", label = "Fitted data")
    plt.title("Average Cross-over time vs. System Size $<t_c>(L)$")
    plt.xlabel("$L$")
    plt.ylabel("$<t_c>(L)$")
    plt.legend()
    plt.grid()
    plt.show()

avg_tc_values, A, beta = gather_data(system_sizes, total_iterations)
display_data(avg_tc_values, A, beta)
