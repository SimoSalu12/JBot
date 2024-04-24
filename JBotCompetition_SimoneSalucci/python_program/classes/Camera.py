from urllib.request import urlopen
import numpy as np
import cv2 as cv
import datetime

class Camera:
    def __init__(self, command) -> None:
        self.cmd = command

    def capture_image(self):
        self.cmd.N = 111
        try:
            cam = urlopen('http://192.168.4.1/capture')
            img = cam.read()
            img = np.asarray(bytearray(img), dtype = 'uint8')
            img = cv.imdecode(img, cv.IMREAD_UNCHANGED)
            # cv.imshow('Camera', img)
            cv.waitKey(1)
            print(self.cmd)
            return img
        except Exception as e:
            print('Error: ', e)

    def find_lines(self, image):
        line = cv.HoughLinesP(image, rho=1, theta=np.pi / 180, threshold=50, minLineLength=5, maxLineGap=10)
        return line is not None
    
    def are_black_parts_present(self, mask):
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        return len(contours) > 5

    def detect_red_light(self, jagerBOT):
        frame = jagerBOT.camera().capture_image()
        hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
        lower_red = np.array([255, 200, 225, 255])
        upper_red = np.array([255, 245, 255, 255])
        #lower_red = np.array([353, 36, 98])    upper_red = np.array([0, 0, 100])   hsv
        #lower_red = np.array([234, 153, 160])    upper_red = np.array([254, 254, 254])     rgb

        mask = cv.inRange(hsv_img, lower_red, upper_red)
        is_red_light_present = self.are_black_parts_present(mask)
        print("red line present:", is_red_light_present)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        cv.drawContours(frame, contours, -1, (0, 255, 0), 2)

        # cv.imshow("Image with Contours", frame)
        print(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        filename = f'D:\elonf\Documents\programming\projects\scuola\jagerBOT\code\program\data\images\photo_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg'
        print(filename)
        cv.imwrite(filename,frame)
        return is_red_light_present
    
    def detect_yellow_light(self, jagerBOT):
        frame = jagerBOT.camera().capture_image()
        hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
        lower_yellow = np.array([252, 222, 159, 255])
        upper_yellow = np.array([255, 254, 248, 255])
        #lower_red = np.array([70, 33, 93])     upper_red = np.array([0, 0, 100])   hsv
        #lower_yellow = np.array([195, 204, 161])   upper_yellow = np.array([254, 254, 254])  rgb

        mask = cv.inRange(hsv_img, lower_yellow, upper_yellow)
        yellow_parts_present = self.find_lines(mask)
        print("yellow line present:", yellow_parts_present)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        cv.drawContours(frame, contours, -1, (255, 255, 0), 2)

        cv.imshow("Image with Contours", frame)
        return yellow_parts_present