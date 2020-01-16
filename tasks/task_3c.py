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

#system_sizes = [4, 8, 16, 32, 64, 128]
system_sizes = [8, 16]
ks = [1, 2, 3, 4]
total_iterations = 30000

avalanche_sizes_dict = gather_data(system_sizes, total_iterations)

L_k_moments = {}

for L in system_sizes:
    kth_moments = {}
    for k in ks:
        kth_moments[k] = get_kth_moment(avalanche_sizes_dict[L], k)
    L_k_moments[L] = kth_moments

pd.DataFrame.from_dict(L_k_moments)
