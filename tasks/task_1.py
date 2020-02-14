import sys
import numpy as np

sys.path.append("..") #allows import from parent level
import matplotlib.pyplot as plt
from model import OsloModel

class TestModel(OsloModel):
    ''' Verifies integrity of simulation'''

    def mass_conservation(self):
        return np.sum(self.model) + self.dropped_grains == self.time

    def run(self, total_iterations):
        for i in range(total_iterations):
            assert(self.mass_conservation())
            assert(self.system_is_relaxed())
            self.drive()
        assert(self.verify_avg_avalanche_size())

    def system_is_relaxed(self):
        self.gen_slopes()
        differences = self.crit_slopes - self.slopes
        #print("differences", differences)
        return(all(differences >= 0))

    def verify_avg_avalanche_size(self):
        """ Average avalanche size after t_c must be = L"""
        avg_avalanche_size = np.average(self.avalanche_sizes[self.first_drop_time:])
        # verify that avg_avalanche_size is approx equal to L by taking their ratio
        print("avg avalanche size = ", avg_avalanche_size, "L = ", self.size)
        return abs(avg_avalanche_size/self.size) < 1.02

TM = TestModel(16)
TM.run(3000)
print(TM.model)
