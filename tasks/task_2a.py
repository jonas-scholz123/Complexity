import sys
import numpy as np

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

def moving_average(data, range = 10) :
    ret = np.cumsum(data, dtype=float)
    ret[range:] = ret[range:] - ret[:-range]
    return ret[range - 1:] / range

system_sizes = [4, 8, 16, 32, 64, 128, 256]

total_iterations = 3000
averaging_range = 1 #set to 1 for no smoothing

for L in system_sizes:
    OM = OsloModel(L)
    OM.run(total_iterations)

    #t = np.array(range(total_iterations - averaging_range + 1)) #for linear plot
    t = np.logspace(0, np.log10(total_iterations- averaging_range), 50, dtype = int) #ensures even spacing of datapoints in log log plot

    height = OM.height_over_time
    height = moving_average(height, averaging_range)
    height = [height[time] for time in t]

    plt.loglog(t, height, "x")
plt.show()
