import sys
import numpy as np

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel
#standardise plots
from plot import set_plot_defaults
set_plot_defaults()

system_sizes = [4, 8, 16, 32, 64, 128, 256]

total_iterations = 90000

for L in system_sizes:
    OM = OsloModel(L)
    OM.run(total_iterations)

    #t = np.array(range(total_iterations - averaging_range + 1)) #for linear plot
    t = np.logspace(0, np.log10(total_iterations - 1), 50, dtype = int) #ensures even spacing of datapoints in log log plot

    height = OM.height_over_time
    height = [height[time] for time in t]

    plt.loglog(t, height, "", label = "L = " + str(L))


plt.title("Height of Pile over time $h(t;L)$")
plt.xlabel("$t$")
plt.ylabel("$h(t;L)$")
plt.legend()
plt.grid()
plt.show()
