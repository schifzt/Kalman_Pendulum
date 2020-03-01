# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
import urllib.request
import numpy as np
import dp
import solvent
import ukf

html_body = """
<!DOCTYPE html>
<html>
<head>
<title>show</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<a class="button" id="view" href="../index.html">view</a></div>

<p>g: %s [m/s^2]</p>
<p>l1: %s [m]</p>
<p>l2: %s [m]</p>
<p>mass1: %s [kg]</p>
<p>mass2: %s [kg]</p>
<p>omega1: %s [/s]</p>
<p>omega2: %s [/s]</p>
<p>phi1: %s [-]</p>
<p>phi2: %s [-]</p>
<p>lambda1: %s [Ns/m]</p>
<p>lambda2: %s [Ns/m]</p>

<meta http-equiv="refresh" content="0; URL = 'http://localhost:8000/index.html'" />

</body>
</html>
"""

# ----------------------
# Get data from fields
# ----------------------
form = cgi.FieldStorage()
generate = form.getvalue('generate', '')
filter = form.getvalue('filter', '')

g = form.getvalue('g', '')
l1 = form.getvalue('l1', '')
l2 = form.getvalue('l2', '')
m1 = form.getvalue('mass1', '')
m2 = form.getvalue('mass2', '')
omega1 = form.getvalue('omega1', '')
omega2 = form.getvalue('omega2', '')
phi1 = form.getvalue('phi1', '')
phi2 = form.getvalue('phi2', '')
lambda1 = form.getvalue('lambda1', '')
lambda2 = form.getvalue('lambda2', '')

print(html_body % (g, l1, l2, m1, m2, omega1,
                   omega2, phi1, phi2, lambda1, lambda2))
# f = urllib.request.urlopen("http://localhost:8000/index.html")
# print(f.read(100))

# ----------------------
# Get Parameters
# ----------------------
g = float(g)
l1 = float(l1)
l2 = float(l2)
m1 = float(m1)
m2 = float(m2)
omega1 = float(omega1)
omega2 = float(omega2)
phi1 = np.deg2rad(float(phi1))
phi2 = np.deg2rad(float(phi2))
lambda1 = float(lambda1)
lambda2 = float(lambda2)

# ----------------------
# Double Pendulum
# ----------------------
dp = dp.DoublePendulum(g, l1, l2, m1, m2, omega1,
                       omega2, phi1, phi2, lambda1, lambda2)
sol = solvent.Solvent(dp)
sol.solve()
sol.write("sim_pen.csv", sol.getPendulum)
sol.write("sim_raw.csv", sol.getState)

# ----------------------
# Kalman
# ----------------------
ukf = ukf.UnscentedKalmanFilter(dp)
x = np.loadtxt("sim_raw.csv", delimiter=",")
# x = x.T  # holizontal to vertical
ukf.putObeserve(x)
ukf.UKF()
ukf.write("kalman_pen.csv", ukf.getPendulum)
ukf.write("kalman_raw.csv", ukf.getState)
