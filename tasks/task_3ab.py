import sys
import numpy as np
from scipy.optimize import curve_fit

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel
from logbin import logbin

def gather_data(system_sizes, total_iterations):
    avalanche_sizes_dict = {}

    for L in system_sizes:
        OM = OsloModel(L)
        OM.run(total_iterations)
        avalanche_sizes_dict[L] = OM.avalanche_sizes[OM.first_drop_time:]

    return avalanche_sizes_dict

def display_data(data, scale = 1):
    plt.figure(figsize = (12, 8))
    for L in data.keys():
        x, y = logbin(data[L], scale = scale, zeros = False)
        plt.loglog(x, y, "", label = "L = " + str(L))
    plt.grid()
    plt.legend()
    plt.show()
    return


system_sizes = [4, 8, 16, 32, 64, 128]
total_iterations = 30000

#avalanche_sizes_dict = gather_data(system_sizes, total_iterations)
#%%
display_data(avalanche_sizes_dict, scale = 1.2)

#%% 3b)
''' Estimate tau for large system sizes, in linear region of log log plot'''

def power_law(s, A, tau):
    return A * 1/(s ** tau)

def modify_data(x, y, tau, D, L):
    collapsed_y = y * x**(tau)
    collapsed_x = x/(L**D)
    return collapsed_x, collapsed_y

#avalanche_sizes = gather_data([L], 100000)

#fit, cov = curve_fit(power_law, x, y, p0 = [1.7, 1])
#tau = fit[1]
#A = fit[0]
#tau = 1.427 # my value for tau
tau = 1.5556 # accepted value for tau
#fit_x = np.logspace(0, np.log10(max(x)), 50)

#plt.loglog(x, y, "x")
#plt.loglog(fit_x, power_law(fit_x, A, tau))
#plt.show()

system_sizes = [4, 8, 16, 32, 64, 128]
#avalanche_sizes = gather_data(system_sizes, 100000)

#for D in [1.8, 1.9, 2, 2.1, 2.2]:
D = 9/4 #accepted value for D
for D in [2, 9/4]:
    for tau in [1.427, 1.5556]:

        for L in system_sizes:

            x, y = logbin(avalanche_sizes[L], scale = 1.3, zeros = False)

            #fit_x = np.logspace(0, np.log10(max(x)), 50)
            #plt.loglog(x, y, "x")
            #plt.loglog(fit_x, power_law(fit_x, A, tau))
            #plt.show()

            collapsed_x, collapsed_y = modify_data(x, y, tau=tau, D=D, L = L)
            plt.loglog(collapsed_x, collapsed_y, "", label = "L = " + str(L))
        plt.grid()
        plt.legend()
        plt.show()
