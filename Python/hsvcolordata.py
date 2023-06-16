import numpy as np

lower_ranges = {
    "yellow": np.array([20, 100, 100]),
    "green": np.array([60, 100, 50]),
    "blue": np.array([100, 100, 50]), 
    "red1": np.array([0, 100, 50]),
    "red2": np.array([170, 100, 50])
}

upper_ranges = {
    "yellow": np.array([40, 255, 255]),
    "green": np.array([100, 255, 255]),
    "blue": np.array([130, 255, 255]),
    "red1": np.array([10, 255, 255]),
    "red2": np.array([180, 255, 255])
}

colors = {
    "yellow": (0, 255, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "red1": (0, 0, 255),
    "red2": (0, 0, 255)
}