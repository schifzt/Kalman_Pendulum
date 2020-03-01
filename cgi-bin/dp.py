import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import collections as mc
# import matplotlib.animation as animation


class DoublePendulum:
    def __init__(self, g, l1, l2, m1, m2, omega1, omega2, phi1, phi2, lambda1, lambda2):
        self.g = g
        self.l1 = l1
        self.l2 = l2
        self.m1 = m1
        self.m2 = m2
        self.omega1 = omega1
        self.omega2 = omega2
        self.phi1 = phi1
        self.phi2 = phi2
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.step_time = 0.0025
        self.stop_time = 30

    def system(self, x, t, m1, m2, l1, l2):
        A = (m1 + m2) * l1 * l1
        B = m2 * l1 * l2 * np.cos(x[2] - x[3])

        C = -m2 * l1 * l2 * x[1] * x[1] * np.sin(x[2] - x[3])
        C -= (m1 + m2) * self.g * l1 * np.sin(x[2])
        C -= self.lambda1 * x[0]

        D = m2 * l1 * l2 * np.cos(x[2] - x[3])
        E = m2 * l2 * l2
        F = m2 * l1 * l2 * x[0] * x[0] * np.sin(x[2] - x[3])
        F -= m2 * l2 * self.g * np.sin(x[3])
        F -= self.lambda2 * x[1]

        return [(E * C - B * F) / (A * E - B * D), (A * F - C * D) / (A * E - B * D), x[0], x[1]]
