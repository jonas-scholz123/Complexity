import numpy as np
import matplotlib.pyplot as plt
from model import OsloModel


class Analytics(OsloModel):
    
    def run(self, total_iterations):
        self.height_over_time = []
        for i in range(total_iterations):
            self.record_height()
            self.drive()
    
    def record_height(self):
        self.height_over_time.append(self.model[0])

system_sizes = [4, 8, 16, 32, 64, 128, 256]

total_iterations = 1000

for L in system_sizes:
    OM = Analytics(L)
    OM.run(total_iterations)

    t = np.array(range(total_iterations))

    plt.plot(t[0::10], OM.height_over_time[0::10],"x")
plt.show()

