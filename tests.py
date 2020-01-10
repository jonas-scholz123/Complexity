from model import OsloModel
import numpy as np

class TestModel(OsloModel):

    def mass_conservation(self):
        return np.sum(self.model) + self.dropped_grains == self.time

    def run(self, total_iterations):
        for i in range(total_iterations):
            assert(self.mass_conservation())
            assert(self.system_is_relaxed())
            self.drive()

    def system_is_relaxed(self):
        self.gen_slopes()
        differences = self.crit_slopes - self.slopes
        #print("differences", differences)
        return(all(differences >= 0))

TM = TestModel(32)
TM.run(3000)
print(TM.model)
