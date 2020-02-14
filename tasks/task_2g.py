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

def gauss(x, mu, sigma, a):
    return a/(sigma * np.sqrt(2*np.pi))*np.e**(-0.5*((x-mu)/sigma)**2)

def modify_data(height_probabilities_dict, height_std_devs, mean_heights):
    #plt.figure(figsize=(12, 8))
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True)
    i = 0 #colours
    for L in height_probabilities_dict.keys():
        height_probabilities = height_probabilities_dict[L]
        original_x = list(height_probabilities.keys())
        original_y = np.array(list((height_probabilities.values())))

        # subtract mean to align distributions' center
        # divide by std dev to have x axis in units of std dev

        collapsed_x = (original_x - mean_heights[L])/height_std_devs[L]
        collapsed_y = original_y * (height_std_devs[L])

        fit, cov = curve_fit(gauss, collapsed_x, collapsed_y)
        fit_x = np.linspace(-4, 4, 1000)
        fit_y = gauss(fit_x, fit[0], fit[1], fit[2])
        deltas = collapsed_y - gauss(collapsed_x, fit[0], fit[1], fit[2])
        ax1.plot(collapsed_x, collapsed_y, "C"+str(i)+"x", label = "L = " + str(L), markersize = 8)
        ax1.plot(fit_x, fit_y, "C"+str(i)+":")
        ax2.plot(collapsed_x, deltas, "C"+str(i)+"x", label = "L = " + str(L), markersize = 8)
        i += 1
    ax1.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_title("Collapsed Distribution of $P(h;L)$ at different L")
    ax2.set_title("Deviations of $P(h;L)$ from Gaussian")
    ax2.set_xlabel(r"$(h - <h>_t)/\sigma_h$", fontsize = "16")
    ax1.set_ylabel(r"$P(h;L)\sigma_h$")
    ax2.set_ylabel(r"$P(h;L)\sigma_h -$ fit")
    plt.show()
    return
if __name__ == "__main__":
    system_sizes = [4, 8, 16, 32, 64, 128, 256]
    total_iterations = 20000
    height_probabilities, height_std_devs, mean_heights= gather_data(system_sizes, total_iterations)

    display_data(height_probabilities)
    modify_data(height_probabilities, height_std_devs, mean_heights)
