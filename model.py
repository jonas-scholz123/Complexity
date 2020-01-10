import numpy as np

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

        for i in range(self.size):
            self.gen_crit_slope(i)


    def drive(self):
        self.model[0] += 1
        self.time += 1

        if self.is_unstable(site = 0):
            self.relax(0)
        return

    def relax(self, site):
        #print("relaxing site ", site)

        self.model[site] -= 1
        if site != self.size - 1:
            self.model[site + 1] += 1
        else:
            self.dropped_grains += 1

        self.gen_crit_slope(site)

        if site != self.size - 1:
            if self.is_unstable(site + 1):
                self.relax(site + 1)

        #as the critical slope is changed, it can still be unstable after
        # first relaxation
        if self.is_unstable(site):
            self.relax(site)

    def gen_crit_slope(self, site):
        rand_val = np.random.uniform()
        # critical slopes may have values equal to 1 or 2
        if rand_val < self.critical_slope_prob:
            self.crit_slopes[site] = 2
        else:
            self.crit_slopes[site] = 1
        return

    def is_unstable(self, site):
        if site != self.size - 1:
            return self.model[site] - self.model[site + 1] > self.crit_slopes[site]
        else:
            return self.model[site] > self.crit_slopes[site]

    def run(self, total_iterations):
        for i in range(total_iterations):
            #print("model: ", self.model)
            #print("crit slopes: ", self.crit_slopes)
            self.drive()

    def system_is_relaxed(self):
        self.gen_slopes()
        differences = self.crit_slopes - self.slopes
        #print("differences", differences)
        return(all(differences >= 0))

    def gen_slopes(self):
        self.slopes = np.zeros(self.size, dtype = int)
        for i in range(self.size - 1):
            self.slopes[i] = self.model[i] - self.model[i+1]


OM = OsloModel(16)
OM.run(2000)
OM.gen_slopes()

print(OM.model)
print(OM.slopes)
print(OM.crit_slopes)
