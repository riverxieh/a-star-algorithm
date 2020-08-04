# main.py
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import a_star
import cv2
import point

#input
input_imgpath = r".\\Testcase\\astar_test.bmp"
input_mskpath = r".\\Testcase\\mask.bmp"
input_img0 = cv2.imread(input_imgpath)
input_img = input_img0[:, :, 1]
input_msk0 = cv2.imread(input_mskpath)
input_msk = input_msk0[:, :, 1]
start_point = point.Point(input_img.shape[0] - 5, 5)
end_point = point.Point(5, input_img.shape[1] - 5)

plt.figure(figsize=(5, 5))
ax = plt.gca()
ax.set_xlim([0, input_img.shape[0]])
ax.set_ylim([0, input_img.shape[1]])

for i in range(input_msk.shape[0]):
    for j in range(input_msk.shape[1]):
        if input_msk[i,j] == 0:
            rec = Rectangle((i, j), width=1, height=1, color='gray')
            ax.add_patch(rec)
        else:
            if input_img[i, j] == 0:
                rec = Rectangle((i, j), width=1, height=1, facecolor='g')
                ax.add_patch(rec)
            else:
                rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='w')
                ax.add_patch(rec)

#draw start point
rec = Rectangle((start_point.x, start_point.y), width = 1, height = 1, facecolor='b')
ax.add_patch(rec)
#draw end point
rec = Rectangle((end_point.x, end_point.y), width = 1, height = 1, facecolor='r')
ax.add_patch(rec)

plt.axis('equal')
# plt.axis('off')
# plt.tight_layout()
# plt.show()

a_star = a_star.AStar(input_img, start_point, end_point, input_msk, False)
a_star.RunAndSaveImage(ax, plt)

