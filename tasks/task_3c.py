import sys
import numpy as np
import pandas as  pd

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

def gather_data(system_sizes, total_iterations):
    avalanche_sizes_dict = {}

    for L in system_sizes:
        OM = OsloModel(L)
        OM.run(total_iterations)
        avalanche_sizes_dict[L] = OM.avalanche_sizes[OM.first_drop_time:]

    return avalanche_sizes_dict

def get_kth_moment(avalanche_sizes, k):
    return np.average(np.power(avalanche_sizes, k))

def fit_kth_moment(L, k, tau):
    return L**((k + 1 - tau)/(2 - tau))

def linear(x, a_0, a_1):
    return a_0 + a_1 * x

def calculate_L_k_data(system_sizes, avalanche_sizes_dict):
    L_k_moments = {}

    for L in system_sizes:
        kth_moments = {}
        for k in ks:
            kth_moment_collector = []
            for i in range(repetitions):
                kth_moment_collector.append(get_kth_moment(avalanche_sizes_dict[L], k))
            kth_moments[k] = np.average(kth_moment_collector)
        L_k_moments[L] = kth_moments

    return pd.DataFrame.from_dict(L_k_moments)

def estimate_crit_exponents(df, show_plots = False):
    ''' Returns estimates for Tau, D through moment analysis as described in paper '''
    k_exponents = {}
    #stores values of the scaling exponent of L, (k+1-tau_s)D for various k

    for k in df.index:
        kth_moments = df.loc[k, 0:].values
        L = df.columns

        log_kth_moments = np.log10(kth_moments)
        log_L = np.log10(L)

        fit = np.polyfit(log_L, log_kth_moments, 1)
        if show_plots:
            plt.plot(log_L, log_kth_moments, "x")
            plt.plot(log_L, fit[1]+fit[0]*log_L)
            plt.show()

        k_exponents[k] = fit[0]

    ks = np.array(list(k_exponents.keys()))
    exponents = np.array(list(k_exponents.values()))

    # offset = fit[1] is equal to (1-tau)/(2-tau) as shown in paper
    #slope = fit[0] is D
    fit = np.polyfit(ks, exponents, 1)

    if show_plots:
        plt.plot(ks, exponents, "x")
        plt.plot(ks, linear(ks, fit[1], fit[0]))
        plt.show()

    return (2*fit[1] -1)/(fit[1] - 1), fit[0]

def estimate_correction(df):
    ''' Estimate Correction to scaling, gamma'''



#system_sizes = [4, 8, 16, 32, 64, 128]
system_sizes = [8, 16, 32, 64]
ks = [1, 2, 3, 4]
total_iterations = 50000
repetitions = 5

#avalanche_sizes_dict = gather_data(system_sizes, total_iterations)

L_k_moments = calculate_L_k_data(system_sizes, avalanche_sizes_dict)
estimate_crit_exponents(L_k_moments)
