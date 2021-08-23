import pyautogui
import random
import numpy as np
import time
from scipy import interpolate
import math


def moveTo(x2, y2):
    # Moves the mouse from current position to the destination (x2, y2)
    # along a path defined by Bezier curve
    disable_pauses()
    # Start (current) position
    x1, y1 = pyautogui.position()
    # Select a random number of control points
    cp = random.randint(3, 7)

    # Distribute control points between start and destination evenly.
    x = np.linspace(x1, x2, num=cp, dtype='int')
    y = np.linspace(y1, y2, num=cp, dtype='int')

    # Randomize inner points a bit (+-RAND at most).
    RAND = 75
    xr = [random.randint(-RAND, RAND) for k in range(cp)]
    yr = [random.randint(-RAND, RAND) for k in range(cp)]
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    x += xr
    y += yr

    # Approximate using Bezier spline.
    degree = 3 if cp > 3 else cp - 1  # Degree of B-spline
    # Finds the B-spline representation of the curve represented by [x,y], degree k
    tck, u = interpolate.splprep([x, y], k=degree)
    # Move up to a certain number of points
    u = np.linspace(0, 1, num=2 + int(point_dist(x1, y1, x2, y2) / 50.0))
    points = interpolate.splev(u, tck)

    # Move mouse. Choose random duration for the mouse movement
    duration = random.uniform(0.2, 0.6)
    timeout = duration / len(points[0])
    point_list = zip(*(i.astype(int) for i in points))

    for i, point in enumerate(point_list):
        pyautogui.moveTo(*point)
        time.sleep(timeout)

    reset_pauses()


def point_dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def disable_pauses():
    pyautogui.MINIMUM_DURATION = 0
    pyautogui.MINIMUM_SLEEP = 0
    pyautogui.PAUSE = 0


def reset_pauses():
    pyautogui.MINIMUM_DURATION = 0.1
    pyautogui.MINIMUM_SLEEP = 0.05
    pyautogui.PAUSE = 0.1