import sys
import numpy as np
from scipy.optimize import curve_fit
import pickle

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel
from logbin import logbin

#standardise plots
from plot import set_plot_defaults
set_plot_defaults()

def gather_data(system_sizes, total_iterations):
    avalanche_sizes_dict = {}

    for L in system_sizes:
        #OM = OsloModel(L)
        #OM.run(total_iterations)
        name = "OM_"+str(L)+".pkl"
        with open(name, 'rb') as input:
            OM = pickle.load(input)
        avalanche_sizes_dict[L] = OM.avalanche_sizes[OM.first_drop_time:]

    return avalanche_sizes_dict

def display_data(data, scale = 1):
    for L in data.keys():
        x, y = logbin(data[L], scale = 1.3 + L/512, zeros = False)
        plt.loglog(x, y, "", label = "L = " + str(L))
    plt.grid()
    plt.xlabel(r"$s$")
    plt.ylabel(r"$\tilde{P}_N(s;L)$")
    plt.title(r"Processed avalanche-size probabilities at scale = " + str(scale) + " + L/512")
    plt.legend()
    plt.show()
    return


system_sizes = [4, 8, 16, 32, 64, 128, 256, 512]
total_iterations = 30000

avalanche_sizes_dict = gather_data(system_sizes, total_iterations)
display_data(avalanche_sizes_dict, scale = 1.3)


#%% 3b)
''' Estimate tau for large system sizes, in linear region of log log plot'''

def power_law(s, A, tau):
    return A * 1/(s ** tau)

def log10_power_law(s, A, tau):
    return np.log10(A) -tau*np.log10(s)

def modify_data(x, y, tau, L):
    D = 1/(2 - tau) # see paper for derivation
    collapsed_y = y * x**(tau)
    collapsed_x = x/(L**D)
    return collapsed_x, collapsed_y

def estimate_tau(avalanche_sizes, show_plot = False):
    x, y = logbin(avalanche_sizes, 1.4)

    log_x = np.log10(x)
    log_y = np.log10(y)

    fit, cov = curve_fit(log10_power_law, log_x, log_y, p0 = [0.4, 1.55])
    tau = fit[1]
    print("initial estimated value of tau = ", tau)
    if show_plot:
        A = fit[0]
        fit_x = np.logspace(0, np.log10(max(x)), 50)

        plt.loglog(x, y, "x")
        plt.loglog(fit_x, power_law(fit_x, A, tau))
        plt.show()
    return tau

system_sizes = [ 16, 32, 64, 128, 256] #exclude small system sizes to uphold large L approximations made in derivations
avalanche_sizes_dict = gather_data(system_sizes, 100000)
tau_0 = estimate_tau(avalanche_sizes_dict[max(system_sizes)])#estimate tau based on largest L

#iterate over range of taus around tau_0 to find best collapse by inspection
tau_range = np.linspace(0.95 * tau_0, 1.05 * tau_0, 20)
#for tau in tau_range:
    ##fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    #for L in system_sizes:
        #x, y = logbin(avalanche_sizes_dict[L], scale = 1.3 + L/512, zeros = False)
#
        ##fit_x = np.logspace(0, np.log10(max(x)), 50)
        ##plt.loglog(x, y, "x")
        ##plt.loglog(fit_x, power_law(fit_x, A, tau))
        ##plt.show()
#
        #collapsed_x, collapsed_y = modify_data(x, y, tau=tau, L = L)
        #plt.loglog(collapsed_x, collapsed_y, "x", label = "L = " + str(L))
    #plt.suptitle("tau = " + str(tau)[0:5])
    #plt.grid()
    #plt.legend()
    #plt.show()
#%%

tau_range = [1.5, 1.545, 1.59]
fig, axes = plt.subplots(1, 3,sharey = True, figsize = (12, 6))
for tau, axis in zip(tau_range, axes):
    for L in system_sizes:
        x, y = logbin(avalanche_sizes_dict[L], scale = 1.3 + L/512, zeros = False)

        #fit_x = np.logspace(0, np.log10(max(x)), 50)
        #plt.loglog(x, y, "x")
        #plt.loglog(fit_x, power_law(fit_x, A, tau))
        #plt.show()

        collapsed_x, collapsed_y = modify_data(x, y, tau=tau, L = L)
        axis.loglog(collapsed_x, collapsed_y, "x", label = "L = " + str(L))
    axis.set_title(r"$\tau_s$ = " + str(tau)[0:5])
    axis.set_xlabel(r"$s/L^D$")
    axis.set_ylabel(r"$\tilde{P}_N(s;L) s^{\tau_s}$")
    axis.grid()
    axis.legend()
    fig.suptitle(r"Data Collapse of $\mathcal{G}(s/L^D)$")
plt.show()
