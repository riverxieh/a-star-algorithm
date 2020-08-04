# a_star.py
import sys
import time
import numpy as np
from matplotlib.patches import Rectangle
import point3D


def euclidean_dis3d(p1, p2):
    vecp = []
    vecp.append[p1.x - p2.x]
    vecp.append[p1.y - p2.y]
    vecp.append[p1.z - p2.z]
    return np.sqrt(np.sum(np.square(vecp)))


class AStar3:
    def __init__(self, image, start_p, end_p, mask=None, displayflag=False):
        self.img = image
        self.msk = mask
        self.p_start = start_p      #tracing start
        self.p_end = end_p          #tracing end
        self.open_set = []
        self.close_set = []
        self.dispflag = displayflag     #display flag


    def BaseCost(self, p):
        # Distance to start point
        distance_cost = euclidean_dis3d(self.p_start, p)
        # Energy to start point
        p_temp = p
        energy_cost = 0
        while p_temp.parent is not None:
            energy_cost = energy_cost + self.img[p_temp.x, p_temp.y, p_temp.z]
            p_temp = p_temp.parent
        return energy_cost + distance_cost

    def HeuristicCost(self, p):
        # <=Min Distance to end point
        distance_cost = euclidean_dis3d(self.p_end, p)
        # <=Min Energy to end point
        energy_cost = distance_cost * 1
        return energy_cost + distance_cost

    def TotalCost(self, p):
        return self.BaseCost(p) + self.HeuristicCost(p)

    def IsObstacle(self, x, y, z):
        if self.msk is None:
            return False
        else:
            if self.msk[x, y, z] == 0:
                return True

    def IsValidPoint(self, x, y, z):
        if self.msk is None:
            return False
        if x < 0 or y < 0 or z < 0:
            return False
        if x >= self.msk.shape[0] or y >= self.msk.shape[1] or z >= self.msk.shape[2]:
            return False
        return not self.IsObstacle(x, y, z)

    def IsInPointList(self, p, point_list):
        for point in point_list:
            if point.x == p.x and point.y == p.y and point.z == p.z:
                return True
        return False

    def IsInOpenList(self, p):
        return self.IsInPointList(p, self.open_set)

    def IsInCloseList(self, p):
        return self.IsInPointList(p, self.close_set)

    def IsStartPoint(self, p):
        return p.x == self.p_start.x and p.y == self.p_start.y and p.z == self.p_start.z

    def IsEndPoint(self, p):
        return p.x == self.p_end.x and p.y == self.p_end.y and p.z == self.p_end.z

    def SaveImage(self, plt):
        millis = int(round(time.time() * 1000))
        filename = './' + str(millis) + '.png'
        plt.savefig(filename)

    def ProcessPoint3D(self, x, y, z, parent):
        if not self.IsValidPoint(x, y, z):
            return  # Do nothing for invalid point
        p = point3D.Point3D(x, y, z)
        if self.IsInCloseList(p):
            return  # Do nothing for visited point
        # print('Process Point [', p.x, ',', p.y, ']', ', cost: ', p.cost)
        if not self.IsInOpenList(p):
            p.parent = parent
            p.cost = self.TotalCost(p)
            self.open_set.append(p)

    def SelectPointInOpenList(self):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for p in self.open_set:
            cost = self.TotalCost(p)
            if cost < min_cost:
                min_cost = cost
                selected_index = index
            index += 1
        return selected_index

    def BuildPath(self, p, ax, plt, start_time):
        path = []
        while True:
            path.insert(0, p) # Insert first
            if self.IsStartPoint(p):
                break
            else:
                p = p.parent
        for p in path:
            rec = Rectangle((p.x, p.y), 1, 1, color='b')
            ax.add_patch(rec)
            plt.draw()
            # self.SaveImage(plt)
        plt.show()
        end_time = time.time()
        print('===== Algorithm finish in', int(end_time-start_time), ' seconds')

    def RunAndSaveImage(self, ax, plt):
        start_time = time.time()

        start_point = self.p_start
        start_point.cost = 0
        self.open_set.append(start_point)

        while True:
            index = self.SelectPointInOpenList()
            if index < 0:
                print('No path found, algorithm failed!!!')
                return
            p = self.open_set[index]
            rec = Rectangle((p.x, p.y), 1, 1, color='c')
            ax.add_patch(rec)
            print('SelectPoint [', p.x, ',', p.y, ', ', p.z, ']', ', cost: ', p.cost)
            # self.SaveImage(plt)

            if self.IsEndPoint(p):
                return self.BuildPath(p, ax, plt, start_time)

            del self.open_set[index]
            self.close_set.append(p)

            # Process all neighbors
            x = p.x
            y = p.y
            self.ProcessPoint3D(x-1, y+1, z, p)
            self.ProcessPoint3D(x-1, y, p)
            self.ProcessPoint(x-1, y-1, p)
            self.ProcessPoint(x, y-1, p)
            self.ProcessPoint(x+1, y-1, p)
            self.ProcessPoint(x+1, y, p)
            self.ProcessPoint(x+1, y+1, p)
            self.ProcessPoint(x, y+1, p)




