import numpy as np
from scipy.spatial import distance


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def offset(self, x_offset, y_offset):
        self.x += x_offset
        self.y += y_offset

    def as_numpy(self):
        return np.array([self.x, self.y])

    def distance(self, point, metric=distance.cityblock):
        p1_array = self.as_numpy()
        p2_array = point.as_numpy()

        return metric(p1_array, p2_array)
