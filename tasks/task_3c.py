import sys
import numpy as np
import pandas as  pd
import pickle
from scipy.optimize  import curve_fit

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

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

def get_kth_moment(avalanche_sizes, k):
    avalanche_sizes = np.array(avalanche_sizes, dtype = np.float64)
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
        k_exponents[k] = fit[0]

        if show_plots:
            #plt.plot(log_L, log_kth_moments, "x")
            #plt.plot(log_L, fit[1]+fit[0]*log_L)
            #plt.show()
            #colour = "C"+str(k-1)
            #plt.loglog(L, kth_moments, colour+"x", label = "k = " + str(k))
            #plt.loglog(L, 10**fit[1]* L**fit[0], colour, label = "Fit for k = " + str(k))

            colour = "C"+str(k - 1)
            fit_data = linear(log_L, fit[1], fit[0])
            deltas = log_kth_moments - fit_data
            plt.plot(log_L, deltas , "x", label = "k = " + str(k))
            plt.plot(log_L, deltas, ":"+colour)
    plt.grid()
    plt.title(r"Deviation of measured $\log_{10} \langle s^k \rangle$ from fit vs $\log_{10}L$")
    plt.xlabel(r"$\log_{10}L$")
    plt.ylabel(r"$\log_{10}\langle s^k \rangle - \log{10}\langle s^k_{fit} \rangle$")
    plt.show()

    if show_plots:
        plt.grid()
        plt.legend()
        plt.title("Kth moment vs system size")
        plt.xlabel(r"$L$")
        plt.ylabel(r"$\langle s^k \rangle $")
        plt.show()

    ks = np.array(list(k_exponents.keys()))
    exponents = np.array(list(k_exponents.values()))

    # offset = fit[1] is equal to (1-tau)/(2-tau) as shown in paper
    #slope = fit[0] is D
    fit = np.polyfit(ks, exponents, 1)

    if show_plots:
        plt.plot(ks, exponents, "x", label = r"Measured $\gamma$")
        plt.plot(ks, linear(ks, fit[1], fit[0]), "r:", label = "Fit")
        plt.grid()
        plt.xlabel(r"$k$")
        plt.legend()
        plt.ylabel(r"$\gamma(k)$")
        plt.title(r"Critical exponent $\gamma$ vs. $k$")
        plt.show()

    return (2*fit[1] -1)/(fit[1] - 1), fit[0]

def estimate_crit_exponents_through_ratios(df):
    #ratio of kth+1/kth moment should equal L^D
    ratios = {}
    omega = 1
    for k in df.index[0:-1]:
        kth_moments = df.loc[k, 0:].values
        k_plus_1th_moments = df.loc[k+1, 0:].values

        L = df.columns
        ratios = k_plus_1th_moments/kth_moments

        logL = np.log10(L)
        log_ratios = np.log10(ratios)

        D, a = np.polyfit(logL, log_ratios, 1)
        print("k = ", k, " implies D = ", D)

        y = ratios/(L**D)
        x = 1/(logL ** omega)

        plt.plot(x, y, "x")


        #plt.plot(logL, log_ratios, "x")
        #plt.plot(logL, a + D*logL, "")
    plt.show()
    return

def power_law(L, a, gamma):
    return a * L ** gamma

def display_kth_moment_scaling(L_k_moments):
    for k in L_k_moments.index:
        L = L_k_moments.columns
        kth_moments = L_k_moments.loc[k, 0:].values

        fit, cov = curve_fit(power_law, L, kth_moments)

        plt.loglog(L, kth_moments, "x", label = "k = " + str(k))
        plt.loglog(L, fit[1]*L**fit[0])
    plt.grid()
    plt.legend()
    plt.show()

def estimate_correction(df, tau, D):
    ''' Estimate Correction to scaling, gamma'''
    tau = 1.55
    D = 9/4
    for gamma in [-0.1, 0.0, 0.05, 0.1, 0.7]:
        #for k in df.index:
        k = 1
        Ls = df.columns
        xs = (1/Ls)**gamma
        kth_moments = df.loc[k, 0:].values

        ys = kth_moments/(Ls**((k + 1 - tau)*D))
        plt.plot(xs, ys, "x", label = "k = " + str(k))
        plt.suptitle(str(gamma))
        plt.legend()
        plt.show()

#def estimate_correction(df, tau, D):
    #''' Estimate Correction to scaling'''
    #tau = 1.55
    #D = 9/4
    #for k in df.index:
        #Ls = df.columns
        ##xs = (1/Ls)**gamma
        #kth_moments = df.loc[k, 0:].values
#
        #ys = kth_moments/(Ls**((k + 1 - tau)*D))
        #plt.loglog(Ls, kth_moments, "x", label = "k = " + str(k))
    #plt.legend()
    #plt.show()

def corrected_log_power_law(L, k, A, tau, c_1, gamma):
    return np.log10(A) + ((k + 1 - tau)/(2 - tau)) * np.log10(L) + np.log10(1 + c_1/(L**gamma))

def show_corrections(system_sizes, all_tau, all_D):
    nr_included = 3
    beginning_index_range = range(0, len(system_sizes) - nr_included + 1)

    taus = []
    Ds   = []
    Ls   = []

    for i in beginning_index_range:
        partial_system_sizes = system_sizes[i:i+nr_included]
        avalanche_sizes_dict = gather_data(partial_system_sizes, total_iterations)
        L_k_moments = calculate_L_k_data(partial_system_sizes, avalanche_sizes_dict)
        tau, D = estimate_crit_exponents(L_k_moments, show_plots = False)
        taus.append(tau)
        Ds.append(D)
        Ls.append(partial_system_sizes)
        #estimate_correction(L_k_moments, tau, D)
        print(tau, D)

    max_Ls = [max(L) for L in Ls]
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True)
    ax1.plot(max_Ls, taus, "x", label = r"$\tau_s$ for different L ranges")
    ax1.hlines(all_tau, min(max_Ls), max(max_Ls), colors = ["C0"], label = r"$\tau_s$ including all L" )
    ax2.plot(max_Ls, Ds, "C1x", label = r"D for different L ranges")
    ax2.hlines(all_D, min(max_Ls), max(max_Ls), colors = ["C1"], label = r"D including all L" )
    ax2.grid()
    ax1.grid()
    ax2.set_xlabel(r"max. $L$ in range")
    ax1.set_ylabel(r"$\tau_s$")
    ax2.set_ylabel(r"D")
    ax1.legend()
    ax2.legend()
    fig.suptitle(r"$\tau_s$ and D over different ranges of L")
    plt.show()

#def estimate_correction(df, tau, D):
    #''' Estimate Correction to scaling, gamma'''
    #tau = 1.55
    #D = 9/4
    #for k in df.index:
        #Ls = np.array(df.columns.to_list())
        #ks = np.array([k for i in Ls])
        #kth_moments = df.loc[k, 0:].values
        #log_kth_moments = np.log10(kth_moments)
        #plt.plot(Ls, log_kth_moments)
        #plt.plot(Ls, corrected_log_power_law(Ls, ks, A = 1, tau = 1.55, c_1 = 0.0, gamma = 0.4))
        #plt.show()

        #fit, cov = curve_fit(corrected_log_power_law, (Ls, ks), log_kth_moments, p0 = [1, 1.55, 0.1, 0.4])
        #print(fit)

system_sizes = [4, 8, 16, 32, 64, 128, 256, 512]
ks = [1, 2, 3, 4]
total_iterations = 50000
repetitions = 5

#display_kth_moment_scaling(L_k_moments)

avalanche_sizes_dict = gather_data(system_sizes, total_iterations)
L_k_moments = calculate_L_k_data(system_sizes, avalanche_sizes_dict)
tau, D = estimate_crit_exponents(L_k_moments, show_plots = True)
#estimate_crit_exponents_through_ratios(L_k_moments)
#print(tau, D)
show_corrections(system_sizes, tau, D)
#estimate_correction(L_k_moments, tau, D)
