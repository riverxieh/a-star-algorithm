# point3D.py
import sys


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.cost = sys.maxsize
        self.parent = None
