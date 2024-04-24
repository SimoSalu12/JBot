"""
This is the main script.

This script will be executed during the contest.
Each function represent a stage of the circuit, each function has a small
description of its capabilities and limitations.
"""

# Import the required classes and libraries
from classes.JagerBOT import JagerBOT 
import time
import math
import sys
import numpy as np
import cv2 as cv

"""
During this phase jagerBOT will follow a black line.
"""
def section1_follow_black_line():
    while True:
        jagerBOT.mode().follow_black_line()

"""
During this phase jagerBOT will follow a black line and avoid an obstacle.
"""
def section2_avoid_obstacle():

    jagerBOT.rotate().horizzontally(90)
    obs = False
    while obs == False:
        jagerBOT.mode().follow_black_line()
        obs = jagerBOT.detect().obstacle(20)
    jagerBOT.move().right(speed=100)
    time.sleep(0.4)
    jagerBOT.stop()
    jagerBOT.rotate().horizzontally(180)
    obs=True
    while obs == True:
        jagerBOT.move().forward(100)
        obs = jagerBOT.detect().obstacle(20)
    time.sleep(0.8)
    jagerBOT.stop()
    jagerBOT.move().left(speed=100)
    time.sleep(0.3)
    jagerBOT.stop()
    obs=True
    while obs == True:
        jagerBOT.move().forward(100)
        obs = jagerBOT.detect().obstacle(20)
    time.sleep(0.5)
    jagerBOT.stop()
    jagerBOT.move().left(speed=100)
    time.sleep(0.3)
    jagerBOT.stop()
    while True:
        jagerBOT.move().forward(100)
        measured_light_refraction = jagerBOT.measure().light_refraction(sensor='M')
        if measured_light_refraction >= 250 and measured_light_refraction <= 850:
            break
    while True:
        jagerBOT.mode().follow_black_line()
        if jagerBOT.read_output() == 'END_OF_STAGE_MODE':
            print('END_OF_STAGE_MODE')
            break


def section3_traffic_light():
    """
    During this phase jagerBOT will stop at the red light and
    will start again broke.
    """

    
    def find_lines(imag):
        line = cv.HoughLinesP(imag, rho=1, theta=np.pi / 180, threshold=50, minLineLength=-1, maxLineGap=10)
        return line is not None

    def tgtl():
        frame = jagerBOT.camera().capture_image()
        hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
        lower_green = np.array([155,182,200,255])
        upper_green = np.array([237,255,246,255])

        mask = cv.inRange(hsv_img, lower_green, upper_green)
        red_parts_present = find_lines(mask)
        print("red line present:", red_parts_present)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        cv.drawContours(frame, contours, -1, (0, 255, 0), 2)

        cv.imshow("Image with Contours", frame)
        return red_parts_present
    

    jagerBOT.move().forward(100)
    time.sleep(1)
    jagerBOT.restart()
    gpp = tgtl()
    while gpp == True :
        gpp = tgtl()
    jagerBOT.move().forward(200)
    time.sleep(1)
    while True:
        jagerBOT.mode().follow_black_line()

def section4_follow_line_by_color():
    """
    During this phase jagerBOT will follow a line of the chosen color
    by the judges (red, green or blue).
    """

    # jagerBOT.mode().adjust_sensibility(500)
    jagerBOT.rotate().horizzontally(90)
    while True:
        jagerBOT.mode().follow_black_line()
        if jagerBOT.measure().light_refraction('M') < 250:
            jagerBOT.restart()
            break
    color = 'red'

    if color == 'blue':
        jagerBOT.move().right(speed=100)
        time.sleep(0.15)

    if color == 'red':
        pass
    
    if color == 'green':
        jagerBOT.move().right(speed=100)
        time.sleep(0.15)

    while True:
        jagerBOT.mode().follow_colored_line()
        if jagerBOT.read_output() == 'END_OF_STAGE_MODE':
            print('END_OF_STAGE_MODE')
            break

def section5_go_to_finish_line():
    """
    During this phase jagerBOT will identify the finish line and there
    will park in front.
    """
    lato1 = 4
    lato2 = 3
    def find_finish_line():
        camera = jagerBOT.camera().capture_image()
        # Converti frame in scala di grigi
        gray = cv.cvtColor(camera, cv.COLOR_BGR2GRAY)
        # Cerca i punti dei vertici della scacchiera
        ret, corners = cv.findChessboardCornersSB(gray, (lato1, lato2), None)
        cv.imshow('capture', camera)
        return ret

    res = False
    jagerBOT.move().left(100)
    time.sleep(0.5)
    rotation_degree = 0
    while True:
        if rotation_degree <= 180:
            jagerBOT.rotate().horizzontally(rotation_degree)
            time.sleep(0.2)
            res = find_finish_line()
            if res == True:
                res2 = False
                jagerBOT.rotate().horizzontally(90)
                x = 0
                if rotation_degree < 90:
                    jagerBOT.move().right(speed=50)
                    while res2 == False :
                        jagerBOT.move().right(speed=50)
                        time.sleep(0.2)
                        jagerBOT.stop()
                        time.sleep(0.5)
                        res2 = find_finish_line()
                        time.sleep(0.5)
                    jagerBOT.stop()
                elif rotation_degree > 90:
                    while res2 == False :
                        jagerBOT.move().left(speed=50)
                        time.sleep(0.2)
                        jagerBOT.stop()
                        time.sleep(0.5)
                        res2 = find_finish_line()
                        time.sleep(0.5)
                    jagerBOT.stop()

                res2 = find_finish_line()
                if res2 == True:
                    while res2 == True :
                        jagerBOT.move().forward(50)
                        time.sleep(1)
                        jagerBOT.stop()
                        time.sleep(0.5)
                        res2 = find_finish_line()
                        time.sleep(0.5)
                jagerBOT.stop()
        else:
            rotation_degree = -30
            jagerBOT.move().forward(50)
            time.sleep(2)
            jagerBOT.stop()

        rotation_degree += 30
    

jagerBOT = JagerBOT()
jagerBOT.rotate().horizzontally(90)


# section1_follow_black_line()

#section2_avoid_obstacle()

#section3_traffic_light()

#section4_follow_line_by_color()

#section5_go_to_finish_line()

