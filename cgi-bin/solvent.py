import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import dp
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import collections as mc

class Solvent:

    def __init__(self, system):  # {{{
        self.dp = system

        self.x0 = [self.dp.omega1, self.dp.omega2, self.dp.phi1, self.dp.phi2]

        self.step_time = self.dp.step_time
        self.stop_time = self.dp.stop_time

        self.x = []
        self.x1 = []
        self.y1 = []
        self.x2 = []
        self.y2 = []
        self.t = np.arange(0, self.stop_time, self.step_time)
# }}}

    def solve(self):  # {{{

        f = self.dp.system
        self.x = odeint(f, self.x0, self.t, args=(
            self.dp.m1, self.dp.m2, self.dp.l1, self.dp.l2))
# }}}

    def getState(self):  # {{{
        time = np.arange(0, len(self.x1)) * self.step_time
        time = np.reshape(time, (len(time), 1))
        return np.concatenate((time, self.x), 1)
# }}}

    def getPendulum(self):  # {{{
        self.x1 = self.dp.l1 * np.sin(self.x[:, 2])
        self.y1 = -self.dp.l1 * np.cos(self.x[:, 3])
        self.x2 = self.dp.l1 * \
            np.sin(self.x[:, 2]) + self.dp.l2 * np.sin(self.x[:, 3])
        self.y2 = -self.dp.l1 * \
            np.cos(self.x[:, 2]) - self.dp.l2 * np.cos(self.x[:, 3])

        time = np.arange(0, len(self.x1)) * self.step_time

        ret = [time, self.x1, self.y1, self.x2, self.y2]
        return np.array(ret).T
# }}}

    def write(self, filename, f):
        out = f()
        np.savetxt(filename, out, delimiter=",")

    def plot(self):  # {{{
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.axvline(x=0, color="black")
        plt.axhline(y=0, color="black")
        window_size = self.dp.l1 + self.dp.l2
        ax.set_xlim(-window_size, window_size)
        ax.set_ylim(-window_size, window_size)

        ax.plot(self.x1, self.y1, ".", color="orange")
        ax.plot(self.x2, self.y2, ".", color="skyblue")
        ax.plot(self.x2[0], self.y2[0], "rs")
        ax.plot(self.x2[len(self.x2) - 1], self.y2[len(self.y2) - 1], "bs")
        plt.show()
# }}}


if(__name__ == '__main__'):
    # g, l1, l2, m1, m2, omega1, omega2, phi1, phi2, lambda1, lambda2
    dp = dp.DoublePendulum(9.8, 1, 1, 1, 1, 0, 0, np.pi / 3, np.pi / 3, 1, 1)
    a = Solvent(dp)
    a.solve()
    # a.plot()
    a.write("sim_pen.csv", a.getPendulum)
    a.write("sim_raw.csv", a.getState)
