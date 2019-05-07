import cv2
import numpy as np

w=50
A = 2*w
A = A**2
img1 = cv2.imread('Motorcycle/im0.png')  # queryImage
img2 = cv2.imread('Motorcycle/im1.png')  # trainImage

cv2.namedWindow('imagem base', cv2.WINDOW_NORMAL)
cv2.resizeWindow("imagem base", 600, 600)
cv2.namedWindow("matches", cv2.WINDOW_NORMAL)
cv2.resizeWindow("matches", 600, 600)



def click(event, x, y, flags, param):
    global imgR
    global img1
    if event == cv2.EVENT_LBUTTONDOWN:
        if x < w:
            x=w
        if y < w:
            y=w
        window = img1[y-w:y+w, x-w:x+w, :]
        window = window.ravel()
        SAD_array=dict()
        for x_perr in range(min(w, x-300), min(img2.shape[1]-w, x+300)):
            window2 = img2[y-w:y+w, x_perr-w:x_perr+w, :]
            window2 = window2.ravel()
            SAD=0
            SAD = window-window2
            SAD = np.sum(SAD)
            SAD_array[x_perr] = SAD
        match = sorted(SAD_array.items(), key=lambda z: z[1])
        imgR = cv2.imread('Motorcycle/im1.png')
        # xnova = x-300
        # imgR = cv2.circle(imgR, (xnova, y), 2, (255, 255, 255), 4)
        # for j in range(0, len(match)):
        #     if abs(match[j][0]-xnova) > 100:
        #         j+=1
        #     else:
        #         x_novo = match[j][0]
        #         imgR = cv2.circle(imgR, (x_novo, y), w, (0, 255, 0), 4)
        #         break
        imgR = cv2.circle(imgR, (match[0][0], y), w, (255, 0, 0), 4)
        imgR = cv2.circle(imgR, (match[1][0], y), w, (0, 0, 255), 4)
        img1 = cv2.circle(img1, (x,y), w, (0,0,255), 4)
        cv2.resizeWindow("matches", 600, 600)
        cv2.imshow("matches", imgR)
        print("feito")



cv2.setMouseCallback("imagem base", click)


while not cv2.waitKey(25) & 0xFF == ord('q'):
    cv2.imshow("imagem base", img1)
