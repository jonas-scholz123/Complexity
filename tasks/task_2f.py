import sys
import numpy as np
from task_2e import get_mean_height

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

def gather_data(system_sizes, total_iterations):
    height_std_devs      = {}

    for L in system_sizes:
        OM = OsloModel(L)
        OM.run(total_iterations)

        height_std_devs[L] = get_height_std_dev(OM)
    return height_std_devs

def get_height_std_dev(OM):
    ''' Gets average height after first dropped grain'''

    sq_heights_over_time = [h*h for h in OM.height_over_time[OM.first_drop_time:]]
    mean_squared_height = get_mean_squared_height(OM)
    mean_height_squared = get_mean_height(OM)**2

    return np.sqrt(mean_squared_height - mean_height_squared)

def get_mean_squared_height(OM):
    sq_heights_over_time = [h*h for h in OM.height_over_time[OM.first_drop_time:]]
    return np.average(sq_heights_over_time)

if __name__ == "__main__":
    system_sizes = [4, 8, 16, 32, 64, 128, 256]
    total_iterations = 100000
    height_std_devs = gather_data(system_sizes, total_iterations)

#%%
    plt.loglog(system_sizes, list(height_std_devs.values()), "x")
    plt.show()
