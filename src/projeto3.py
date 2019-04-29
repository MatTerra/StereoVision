import numpy as np
import cv2
from matplotlib import pyplot as plt

tam = 20


def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global img1, img2
        # FLANN parameters
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()
        # find the keypoints and descriptors with SIFT
        img_sel = img2[y-tam:y+tam, x-tam:x+tam]
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img_sel, None)
        matches = flann.knnMatch(des1, des2, k=2)
        # Need to draw only good matches, so create a mask
        matchesMask = [[0, 0] for i in range(len(matches))]
        # ratio test as per Lowe's paper
        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7 * n.distance:

                matchesMask[i] = [1, 0]
        draw_params = dict(matchColor=(0, 255, 0),
                           singlePointColor=(255, 0, 0),
                           matchesMask=matchesMask,
                           flags=0)
        filtKp=[]
        for point in kp1:
            print(abs(point.pt[1] - y))
            if abs(point.pt[1] - y) < 10 and abs(point.pt[0] - x) < 50:
                filtKp.append(point)
        img1 = cv2.rectangle(img1, (int(filtKp[0].pt[0]-(tam/2)), int(filtKp[0].pt[1]-(tam/2))),
                      (int(filtKp[0].pt[0]+(tam/2)), int(filtKp[0].pt[1]+(tam/2))),
                      5)
        cv2.imshow("Match", img1)
        cv2.resizeWindow("Match", 600, 600)
        #img3 = cv2.drawMatchesKnn(img1, filtKp, img_sel, kp2, matches, None, **draw_params)

        #plt.imshow(img3, ), plt.show()


img1 = cv2.imread('JadePlant/im0.png', 0)  # queryImage
img2 = cv2.imread('JadePlant/im1.png', 0)  # trainImage

block_matcher = cv2.StereoBM_create(0, 5)
disp = block_matcher.compute(img2, img1)
norm_coeff = 255 / disp.max()
cv2.namedWindow("disparity", cv2.WINDOW_NORMAL)
cv2.imshow("disparity", disp * norm_coeff / 255)

cv2.resizeWindow("disparity", 600, 600)

img2_cor = cv2.imread('JadePlant/im1.png')  # trainImage
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.namedWindow("Match", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("image", click)
cv2.imshow("Match", img1)
cv2.imshow("image", img2_cor)
cv2.resizeWindow("image", 600, 600)
cv2.resizeWindow("Match", 600,600)

while not (cv2.waitKey(25) & 0xFF == ord('q') or cv2.getWindowProperty('image', 0)):
    cv2.imshow("image", img2_cor)
    cv2.waitKey(1)

