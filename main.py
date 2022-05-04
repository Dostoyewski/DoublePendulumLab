import cv2 as cv
import numpy as np
import pandas as pd


class ARUCODetector(object):
    def __init__(self, filename):
        self.cap = cv.VideoCapture(filename)
        self.res_df = pd.DataFrame(columns=['31x', '31y', '32x', '32y', '33x', '33y', 'timestamp'])
        self.fps = self.cap.get(cv.CAP_PROP_FPS)

    def run(self):
        n = 0
        while True:
            success, image = self.cap.read()
            if image is None:
                cv.destroyAllWindows()
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
                    out_d = {}
                    for i, idd in enumerate(markerIds):
                        coords = list(np.mean(markerCorners[i], axis=1)[0].astype('int'))
                        image = cv.circle(image, coords, 20, (255, 0, 0), -1)
                        out_d[str(idd[0]) + 'x'], out_d[str(idd[0]) + 'y'] = coords[0], coords[1]
                    out_d['timestamp'] = n / self.fps
                    self.res_df = self.res_df.append(out_d, ignore_index=True)
                cv.imshow("Detection result", image)
                n += 1
            else:
                continue
        self.res_df.to_excel('./out.xlsx')


if __name__ == '__main__':
    det = ARUCODetector('./IMG_3272.MOV')
    det.run()
