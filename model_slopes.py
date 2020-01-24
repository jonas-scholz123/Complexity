import numpy as np
import time

class OsloModel(object):
    """OsloModel as specified by the project guidelines.
        """

    def __init__(self, size, p = 0.5, total_iterations = 50):
        #initialise a system of specified size as np array
        super(OsloModel, self).__init__()
        self.time = 0
        self.size = size
        self.model = np.zeros(self.size, dtype = int)
        self.critical_slope_prob = p
        self.total_iterations = total_iterations
        self.crit_slopes = np.zeros(self.size, dtype = int)
        self.dropped_grains = 0
        self.first_drop_time = None
        self.height_over_time = []
        self.avalanche_sizes = []

        for i in range(self.size):
            self.gen_crit_slope(i)


    def drive(self):
        self.avalanche_size = 0
        self.model[0] += 1
        self.time += 1

        if self.is_unstable(site = 0):
            self.relax(0)

        self.avalanche_sizes.append(self.avalanche_size)
        return

    def relax(self, site):
        #every time the relax function is called, increment avalanche_size
        self.avalanche_size += 1

        if site == 0:
            self.model[site] -= 2
            self.model[site + 1] += 1
        elif site == self.size - 1:
            self.model[site] -= 1
            self.model[site - 1] += 1
            self.dropped_grains += 1
        else:
            self.model[site] -= 2
            self.model[site + 1] += 1
            self.model[site - 1] += 1

        self.gen_crit_slope(site)

        if site != self.size - 1:
            if self.is_unstable(site + 1):
                self.relax(site + 1)

        #as the critical slope is changed, it can still be unstable after
        # first relaxation
        if self.is_unstable(site):
            self.relax(site)
        return

    def gen_crit_slope(self, site):
        rand_val = np.random.uniform()
        # critical slopes may have values equal to 1 or 2
        if rand_val < self.critical_slope_prob:
            self.crit_slopes[site] = 2
        else:
            self.crit_slopes[site] = 1
        return

    def is_unstable(self, site):
        return self.model[site] > self.crit_slopes[site]

    def record_height(self):
        # TODO: FIX
        self.height_over_time.append(self.model[0])

    def run(self, total_iterations):

        for i in range(total_iterations):
            self.record_height()
            self.drive()

        return


if __name__ == "__main__":

    start = time.time()
    OM = OsloModel(64)
    OM.run(100000)
    end = time.time()
    print(end-start)
    #print(OM.slopes)
    #print(OM.crit_slopes)
