import cv2
import numpy as np
import math

histogramSize = 100

src = cv2.imread("photo.jpg")
# src = cv2.GaussianBlur(src, (5, 5), cv2.BORDER_DEFAULT)
src = cv2.bilateralFilter(src, 25, 75, 75)
cv2.imwrite("blur.png", src)

dst = cv2.Canny(src, 180, 250, None, 5, True)
dst = cv2.dilate(dst, None)
dst = cv2.erode(dst, None)
cv2.imwrite("canny.png", dst)

print(dst.shape)
cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
cdst = np.zeros((dst.shape[0], dst.shape[1], 3), np.uint8)

linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 20, 10)

lxi = []
lri = []
for i in range(int((dst.shape[0] + dst.shape[1]) / histogramSize) + 30):
    lxi.append(0)
for i in range(91):
    lri.append(0)

if linesP is not None:
    for i in range(0, len(linesP)):
        l = linesP[i][0]
        if (l[2] - l[0]) == 0 or math.fabs(math.atan((l[3] - l[1]) / (l[2] - l[0])) / math.pi * 180) <= 80:
            cv2.line(cdst, (l[0], l[1]), (l[2], l[3]), (255, 255, 255), 1, cv2.LINE_AA)

    for i in range(0, len(linesP)):
        l = linesP[i][0]
        if (l[2] - l[0]) == 0 or math.fabs(math.atan((l[3] - l[1]) / (l[2] - l[0])) / math.pi * 180) > 80:
            lxi[int((l[0] - (l[2] - l[0]) / (l[3] - l[1]) * l[1]) / histogramSize) + 20] += math.sqrt(l[2] - l[0]) * (
                    l[2] - l[0]) + (l[3] - l[1]) * (l[3] - l[1])
            lri[int(math.fabs(math.atan((l[3] - l[1]) / (l[2] - l[0])) / math.pi * 180))] += math.sqrt(l[2] - l[0]) * (
                    l[2] - l[0]) + (l[3] - l[1]) * (l[3] - l[1])

    while lri[-1] == 0:
        del lri[-1]
    while lxi[-1] == 0:
        del lxi[-1]

    frl = lri
    frli = frl.index(max(frl))
    fxl = lxi[:int(len(lxi) / 2)]
    fxli = fxl.index(max(fxl)) - 20

    dotLi = []

    for i in range(0, len(linesP)):
        l = linesP[i][0]
        if (l[2] - l[0]) == 0 or math.fabs(math.atan((l[3] - l[1]) / (l[2] - l[0])) / math.pi * 180) > 80:
            if math.fabs((l[0] - (l[2] - l[0]) / (l[3] - l[1]) * l[
                1]) - fxli * histogramSize) < histogramSize * 2 and math.fabs(
                int(math.fabs(math.atan((l[3] - l[1]) / (l[2] - l[0])) / math.pi * 180)) - frli) < 5:
                dotLi.append((l[1], l[0]))
                dotLi.append((l[3], l[2]))

    dotLi.sort()
    cv2.line(cdst, (dotLi[0][1], dotLi[0][0]), (dotLi[-1][1], dotLi[-1][0]), (0, 255, 0), 3, cv2.LINE_AA)

    dotLi = []
    fxl = lxi[int(len(lxi) / 2):]
    fxli = fxl.index(max(fxl)) + int(len(lxi) / 2) - 20

    for i in range(0, len(linesP)):
        l = linesP[i][0]
        if (l[2] - l[0]) == 0 or math.fabs(math.atan((l[3] - l[1]) / (l[2] - l[0])) / math.pi * 180) > 80:
            print(math.fabs((l[0] - (l[2] - l[0]) / (l[3] - l[1]) * l[
                1])))
            if math.fabs((l[0] - (l[2] - l[0]) / (l[3] - l[1]) * l[
                1]) - fxli * histogramSize) < histogramSize * 2 and math.fabs(
                int(math.fabs(math.atan((l[3] - l[1]) / (l[2] - l[0])) / math.pi * 180)) - frli) < 5:
                dotLi.append((l[1], l[0]))
                dotLi.append((l[3], l[2]))
    dotLi.sort()
    cv2.line(cdst, (dotLi[0][1], dotLi[0][0]), (dotLi[-1][1], dotLi[-1][0]), (0, 0, 255), 3, cv2.LINE_AA)


cv2.imwrite("Probabilistic.png", cdst)

cv2.waitKey()
