import cv2 as cv
import numpy as np
import pandas as pd

if __name__ == '__main__':
    cap = cv.VideoCapture('./test.mp4')
    while True:
        success, image = cap.read()
        if image is None:
            break
        key = cv.waitKey(1) & 0xFF
        if (key == 27) or (key == ord('q')):
            break
        if success:
            dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
            parameters = cv.aruco.DetectorParameters_create()
            markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(image,
                                                                                  dictionary,
                                                                                  parameters=parameters)
            if markerIds is not None:
                coords = list(np.mean(markerCorners[0], axis=1)[0].astype('int'))
                image = cv.circle(image, coords, 20, (255, 0, 0), -1)
            cv.imshow("original", image)
        else:
            continue
