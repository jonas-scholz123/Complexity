import sys
import numpy as np

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

tc_values = {}
nr_repetitions = 3
system_sizes = [4, 8, 16, 32]
total_iterations = 3000

for L in system_sizes:
    tc_values[L] = []

    for i in range(nr_repetitions):

        OM = OsloModel(L)
        OM.run(total_iterations)
        tc_values[L].append(OM.first_drop_time)

avg_tc_values = {k: np.average(v) for k,v in tc_values.items()}

system_sizes = []
avg_tc_list  = []

for L, avg_tc in avg_tc_values.items():
    system_sizes.append(L)
    avg_tc_list.append(avg_tc)

plt.loglog(system_sizes, avg_tc_list, "x")
plt.show()


print(avg_tc_values)


def theoretical_tc(L):
    return 3/4 *L*(L+1)

theoretical_values = {L : theoretical_tc(L) for L in system_sizes}
print(theoretical_values)

for L in system_sizes:
    print(theoretical_values[L]/avg_tc_values[L])
