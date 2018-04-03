#!/usr/bin/env python3
import cv2
import numpy as np
from convert3d import output_3d

def stylize_left(img):
    #color transform
    BGR = img.astype(np.float32) # uint8 may overflow when plus
    BGR = cv2.split(BGR)
    B = BGR[0] * 0.3
    G = BGR[1] * 0.47
    R = BGR[2] * 0.52
    BGR = np.clip(cv2.merge([B,G,R]),0,255)
    BGR = BGR.astype(np.uint8)

    #Brightness transform
    HSV = cv2.cvtColor(BGR, cv2.COLOR_BGR2HSV)
    HSV = HSV.astype(np.float32)
    HSV = cv2.split(HSV)
    H = HSV[0]
    S = HSV[1]
    V = HSV[2]
    V = V + 30

    decay = 30
    S[H < 25 / 2] = S[H < 25 / 2] - decay
    S[H < 21 / 2] = S[H < 21 / 2] - decay
    S[H < 17 / 2] = S[H < 17 / 2] - decay
    S[H < 14 / 2] = S[H < 14 / 2] - decay
    S[H > 315 / 2] = S[H > 315 / 2] - decay
    S[H > 325 / 2] = S[H > 325 / 2] - decay
    S[H > 335 / 2] = S[H > 335 / 2] - decay
    S[H > 345 / 2] = S[H > 345 / 2] - decay

    HSV = np.clip(cv2.merge([H,S,V]),0,255)
    HSV = HSV.astype(np.uint8)
    BGR = cv2.cvtColor(HSV, cv2.COLOR_HSV2BGR)
    cv2.GaussianBlur(BGR, (7,7), 0)
    cv2.imwrite("out7.jpg",BGR)

if __name__ == '__main__':
    imgL = cv2.imread("left.jpg")
    stylize_left(imgL)



