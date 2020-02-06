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

system_sizes = [4, 8, 16, 32, 64, 128, 256]
total_iterations = 100000

def gather_data(system_sizes, total_iterations):
    avg_tc_values = {}

    for L in system_sizes:
        nr_repetitions = 4*int(256/L) #higher L requires fewer repetitions
        avg_tc_values[L] = get_avg_tc(L, nr_repetitions)

    L = list(avg_tc_values.keys())
    avg_tc = list(avg_tc_values.values())

    #now find fit for different range of system sizes to show it approaches 2

    max_system_size_vs_beta = {}

    for smallest_L_index in range(0, len(system_sizes)- 2):

        partial_L = L[smallest_L_index: smallest_L_index + 3]
        partial_avg_tc = avg_tc[smallest_L_index: smallest_L_index + 3]
        fit, cov = curve_fit(log_power_law, partial_L, np.log10(partial_avg_tc))
        A = fit[0]
        beta = fit[1]
        max_system_size_vs_beta[max(partial_L)] = beta

    full_fit, cov = curve_fit(log_power_law, L, np.log10(avg_tc))
    A = full_fit[0]
    beta = full_fit[1]

    return avg_tc_values, A, beta, max_system_size_vs_beta

def log_power_law(L, A, beta):
    return np.log10(A) + beta*np.log10(L)

def get_avg_tc(L, nr_repetitions):
    tc_list = []

    for i in range(nr_repetitions):

        #name = "OM_"+str(L)+".pkl"
        #with open(name, 'rb') as input:
            #OM = pickle.load(input)

        OM = OsloModel(L)
        OM.stop_at_first_drop = True
        OM.run(total_iterations)
        tc_list.append(OM.first_drop_time)

    return np.average(tc_list)

def display_full_fit(datapoints, A, beta):
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

def display_beta_vs_system_size(max_system_size_vs_beta):
    x = list(max_system_size_vs_beta.keys())
    y = list(max_system_size_vs_beta.values())

    plt.plot(x, y, "x", label = r"Estimated Values of $\beta$")

    #annotate above
    for x_coord, y_coord in zip(x, y):
        Ls = [x_coord//4, x_coord//2, x_coord]
        plt.annotate("L = " + str(Ls), (x_coord + 3, y_coord-0.001), annotation_clip = False)

    plt.plot(x, [2 for i in x], "r", label = r"Theoretical Value of $\beta$")
    plt.title(r"Estimates of $\beta$ vs Considered System Sizes")
    plt.ylabel(r"Estimates of $\beta$")
    plt.xlabel("Max system size considered")
    plt.legend()
    plt.grid()
    plt.show()

avg_tc_values, A, beta, max_system_size_vs_beta = gather_data(system_sizes, total_iterations)
display_beta_vs_system_size(max_system_size_vs_beta)
display_full_fit(avg_tc_values, A, beta)
print(beta)
