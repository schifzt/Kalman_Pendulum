import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import dp


class UnscentedKalmanFilter:
    def __init__(self, system):
        self.dp = system

        self.step_time = self.dp.step_time
        self.stop_time = self.dp.stop_time
        self.out = []

        # Target State
        self.x0 = np.array([[self.dp.omega1], [self.dp.omega2], [
                           self.dp.phi1], [self.dp.phi2]])

        # observe State(x projection)
        self.z = []

        self.n = len(self.x0)
        self.m = 1

        # Weights
        self.wm = np.zeros(2 * self.n + 1)
        self.wc = np.zeros(2 * self.n + 1)

        # Sigma Point
        k = 0  # 0
        a = 0.01  # 0 < a << 1
        b = 2  # 0
        self.lmd = np.square(a) * (self.n + k) - self.n
        self.prm = 1.0 - np.square(a) + b

        # sigma_point = #array([
        # [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        # [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        # [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        # [0., 0., 0., 0., 0., 0., 0., 0., 0.]
        # ])

        #------------------------------------------
        # Almost Stable
        #-----------------------------------------
        # self.P = np.eye(4) * 0.0001
        # self.sigma2_w = 0.0001  # move noise
        # self.sigma2_v = 0.0001  # obeserb noise
        #------------------------------------------
        self.P = np.eye(4) * 0.0001
        # self.P = np.ones((4,4)) * 0.001
        self.sigma2_w = 0.0001  # move noise
        self.sigma2_v = 0.0001  # obeserb noise #max 0.014

    def calcWeight(self):  # {{{
        self.wm[0] = self.lmd / (self.n + self.lmd)
        self.wc[0] = self.lmd / (self.n + self.lmd) + self.prm
        for i in range(1, 2 * self.n + 1):  # i = 1, .., 2 n
            self.wm[i] = self.wc[i] = 1 / (2 * (self.n + self.lmd))

# }}}

    def putObeserve(self, x):  # {{{
        x = x[:, 1:5]
        x = x.T
        obeserb = self.h(x)

        self.z = obeserb + \
            np.random.randn(len(obeserb[0]), self.m).T * self.sigma2_v

        time = np.arange(0, len(obeserb[0])) * self.step_time
        time = np.array([time])
        ret = np.concatenate((time, self.z), 0).T
        np.savetxt("observe.csv", ret, delimiter=",")

        return self.z
# }}}

    #------------------------------------------
    # Define What You CAN See
    #------------------------------------------
    def h(self, x):  # {{{
        # x=[dt1[0000000000000000],
        #    dt2[0000000000000000],
        #    t1[0000000000000000],
        #    t2[0000000000000000]]
        dt1 = x[0]
        dt2 = x[1]
        t1 = x[2]
        t2 = x[3]

        # vertical vector
        h = np.zeros((self.m, len(dt1)))
        # h[0] = -self.dp.l1 * np.cos(t1)
        # h[1] = self.dp.l1 * np.sin(t1)
        # h[1] = -self.dp.l1 * np.cos(t1) - self.dp.l2 * np.cos(t2)
        h[0] = self.dp.l1 * np.sin(t1) + self.dp.l2 * np.sin(t2)
        return h
# }}}

    def f(self, x):  # {{{
        dt1 = x[0]
        dt2 = x[1]
        t1 = x[2]
        t2 = x[3]

        g = self.dp.g
        m1 = self.dp.m1
        m2 = self.dp.m2
        l1 = self.dp.l1
        l2 = self.dp.l2
        lambda1 = self.dp.lambda1
        lambda2 = self.dp.lambda2

        A = (m1 + m2) * np.square(l1)
        B = m2 * l1 * l2 * np.cos(t1 - t2)

        C = -m2 * l1 * l2 * np.square(dt2) * np.sin(t1 - t2)
        C -= (m1 + m2) * g * l1 * np.sin(t1)
        C -= lambda1 * dt1

        D = m2 * l1 * l2 * np.cos(t1 - t2)
        E = m2 * np.square(l2)
        F = m2 * l1 * l2 * np.square(dt1) * np.sin(t1 - t2)
        F -= m2 * l2 * g * np.sin(t2)
        F -= lambda2 * dt2

        f1 = dt1 + self.step_time * (E * C - B * F) / (A * E - B * D)
        f2 = dt2 + self.step_time * (A * F - C * D) / (A * E - B * D)
        f3 = t1 + self.step_time * f1
        f4 = t2 + self.step_time * f2

        return np.array([f1, f2, f3, f4])  # vertical vector

        # f3 = t1 + self.step_time * dt1
        # f4 = t2 + self.step_time * dt2

# }}}

    def sigmaPoint(self, u, P):  # {{{
        rootP = np.linalg.cholesky(P)
        sigma_point = np.zeros((self.n, 2 * self.n + 1))

        sigma_point[:, 0: 1] = u  # col[0] = u
        for i in range(1, self.n + 1):  # i = 1, .., n
            sigma_point[:, i: i + 1] = u + \
                np.sqrt(self.n + self.lmd) * rootP[:, i - 1: i]
            sigma_point[:, self.n + i: self.n + i + 1] = u - \
                np.sqrt(self.n + self.lmd) * rootP[:, i - 1: i]

        return sigma_point
# }}}

    def E(self, X):  # {{{
        col = len(X[:, 0])
        u = np.zeros((col, 1))
        # print(u)
        # print("\n")
        # print("E")
        for i in range(2 * self.n + 1):  # i = 0, .., 2 n
            # print(X[:, i:i + 1])
            u += self.wm[i] * X[:, i: i + 1]
        return u
# }}}

    def Cov(self, u, X):  # {{{
        col = len(X[:, 0])
        # print("Cov\n")
        # print(P)
        P = np.zeros((col, col))
        for i in range(2 * self.n + 1):  # i = 0, .., 2 n
            diff = X[:, i: i + 1] - u
            P += self.wc[i] * np.dot(diff, diff.T)
        return P
# }}}

    def xCov(self, u, X, y, Y):  # {{{
        col1 = len(X[:, 0])
        col2 = len(Y[:, 0])
        P = np.zeros((col1, col2))
        for i in range(2 * self.n + 1):  # i = 0, .., 2 n
            diff1 = X[:, i: i + 1] - u
            diff2 = Y[:, i: i + 1] - y
            P += self.wc[i] * np.dot(diff1, diff2.T)
        return P
# }}}

    #------------------------------------------
    # zt: obeserb state
    # ut: mean of internal state
    # P: covariance of internal state
    #------------------------------------------

    def UKFcore(self, zt, ut1, Pt1):
        #------------------------------------------
        # PREDICT state
        #------------------------------------------
        Xt1 = self.sigmaPoint(ut1, Pt1)

        # print("Xt1\n", Xt1[: , 0: 5])
        # print("Xt1\n", Xt1[: , 5: 9])
        # print("\n")

        _Xast = np.zeros((self.n, 2 * self.n + 1))
        for i in range(2 * self.n + 1):
            _Xast[:, i: i + 1] = self.f(Xt1[:, i: i + 1])

        # print("_Xast\n", _Xast[: , 0: 5])
        # print("_Xast\n", _Xast[: , 5: 9])
        # print("\n")

        R = self.sigma2_v * np.eye(self.n)
        _ut = self.E(_Xast)
        _Pt = self.Cov(_ut, _Xast) + R

        # print("_ut\n", _ut)
        # print("\n")
        # print("_Pt\n", _Pt)
        # print("\n")
        # print(np.linalg.eigvals(_Pt))
        # print("\n")

        #------------------------------------------
        # PREDICT zt
        #------------------------------------------
        _X = self.sigmaPoint(_ut, _Pt)

        # print("_X\n", _X[: , 0: 5])
        # print("_X\n", _X[: , 5: 9])
        # print("\n")

        # _Z = [[0, ..., 0],[0, ..., 0], ..., [0]]
        _Z = np.zeros((self.m, 2 * self.n + 1))
        for i in range(2 * self.n + 1):  # i = 0, ..., 2 n
            _Z[:, i: i + 1] = self.h(_X[:, i: i + 1])
            # _Z[:, i: i + 1] = self.h(_X[:, i])

        _zt = self.E(_Z)

        # print("_Z\n", _Z)
        # print("\n")
        # print("_zt\n", _zt)
        # print("\n")

        #------------------------------------------
        # Fix ut with Mesurement
        #------------------------------------------
        Q = self.sigma2_w * np.eye(self.m)
        S = self.Cov(_zt, _Z) + Q
        _crossPt = self.xCov(_ut, _X, _zt, _Z)

        # print("Q\n", Q)# print("\n")
        # print("S\n", S)
        # print("\n")
        # print("_crossPt\n", _crossPt)
        # print("\n")

        K = np.dot(_crossPt, np.linalg.inv(S))
        ut = _ut + np.dot(K, (zt - _zt))
        Pt = _Pt - np.dot(K, np.dot(S, K.T))

        # print("\n")
        # print("K\n", K)
        # print("\n")
        # print("ut\n", ut)
        # print("\n")
        # print("Pt\n", Pt)
        # print("\n")

        return [ut, Pt]

    def UKF(self):  # {{{
        u = []
        P = []
        self.calcWeight()
        for t in range(0, len(self.z[0])):
            if (t == 0):
                u, P = self.UKFcore(self.z[:, t: t + 1], self.x0, self.P)
            else:
                u, P = self.UKFcore(self.z[:, t: t + 1], u, P)

            P_diag = np.diag(P)
            y = np.concatenate((u.T[0], P_diag))  # vertical to holizontal
            self.out.append(y)

        self.out = np.reshape(self.out, (len(self.out), 8))  # row to column

        #------------------------------------------
        # out =
        # [[omega1, omega2, phi1, phi2,
        #       diag1, diag2, diag3, diag4]]
        #------------------------------------------
# }}}

    def getState(self):  # {{{
        time = np.arange(0, len(self.out)) * self.step_time
        time = np.reshape(time, (len(time), 1))
        return np.concatenate((time, self.out), 1)
# }}}

    def getPendulum(self):  # {{{
        out = self.getState()  # note that out[0] is time

        l1 = self.dp.l1
        l2 = self.dp.l2
        t1 = out.T[3]  # row
        t2 = out.T[4]  # row
        x1_estm = l1 * np.sin(t1)
        y1_estm = -l1 * np.cos(t1)
        x2_estm = l1 * np.sin(t1) + l2 * np.sin(t2)
        y2_estm = -l1 * np.cos(t1) - l2 * np.cos(t2)

        time = np.arange(0, len(x1_estm)) * self.step_time
        ret = [time, x1_estm, y1_estm, x2_estm, y2_estm]
        return np.array(ret).T
# }}}

    def write(self, filename, f):  # {{{
        out = f()
        np.savetxt(filename, out, delimiter=",")
        # h = str(self.step_time) + ',' + str(self.stop_time)
        # np.savetxt(filename, out, delimiter=",", header=h, comments='')
# }}}


if (__name__ == '__main__'):
    dp = dp.DoublePendulum(9.8, 1.5, 1.5, 1, 1, 10, -9,
                           np.pi / 3, np.pi / 3, 0, 0)
    ukf = UnscentedKalmanFilter(dp)
    x = np.loadtxt("sim_raw.csv", delimiter=",")
    # x = x.T  # holizontal to vertical

    ukf.putObeserve(x)
    ukf.UKF()
    ukf.write("kalman_pen.csv", ukf.getPendulum)
    ukf.write("kalman_raw.csv", ukf.getState)
