Kalman Pendulum
====
## Overview
estimate double pendulum states with Unscented Kalman Filter(UKF)

<img width="911" alt="demo" src="https://user-images.githubusercontent.com/26299162/32402296-204d6d2a-c164-11e7-9a96-807bd864e8ed.png">

## Description
Just observing a part of double pendulum states, UKF can estimates whole states.

You can see the magic of modern control theory.

## Features
+ simple UI
+ many variable parameters

## Requirement
+ python3.6~
+ dygraphs(see package.json)

## Usage
0. Activate
    + Windows : click a `start.bat` and access to `http://localhost:8000/index.html`.
    + Others : `python server.py`. Then access to `http://localhost:8000/index.html`.

1. set parameters

<img width="366" alt="parameters" src="https://user-images.githubusercontent.com/26299162/32402668-c1334c66-c16c-11e7-8f96-6991582cc413.png">

2. click `generate`.

3. Please wait a minute whiel generating .csv files.<br>

4. click `view`.

+ If you want to change an observe variable, see cgi-bin/ukf.py/h(self, x)
+ You can change many hidden parameters(e.g simulation time, simulation step-time) directly. See cgi-bin/ukf.py.

Please Enjoy!
