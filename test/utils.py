import cv2
import numpy as np



def getColorRange(color):
    hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
    return hsv



if __name__ == "__main__":
    blue = np.uint8([[[255,0,0]]])
    blue_hsv = getColorRange(blue)
    print(blue_hsv)
