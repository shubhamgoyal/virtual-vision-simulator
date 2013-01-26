#!/usr/bin/env python

import wx
import logging
import threading

from client import MyFrame
from client import DEFAULT_PAN_SPEED
from client import DEFAULT_TILT_SPEED
from client import DEFAULT_ZOOM_SPEED

STATIC_PIPELINE = 0
ACTIVE_PIPELINE = 1

clientList = []
e = threading.Event()

def pan (camera_number, degrees, speed):
    clientList[camera_number - 1].pan(degrees, speed)
	
def tilt (camera_number, degrees, speed):
    clientList[camera_number - 1].tilt(degrees, speed)

def zoom (camera_number, degrees, speed):
    clientList[camera_number - 1].zoom(degrees, speed)
	
def getImage(camera_number):
    clientList[camera_number - 1].getImage()
	
class mainLoopThread(threading.Thread):
    def __init__(self, autoStart=True):
        threading.Thread.__init__(self)
        self.setDaemon(0)
        self.start_orig = self.start
        self.start = self.start_local
        self.lock = threading.Lock()
        self.lock.acquire()
        if autoStart:
            self.start()

    def run(self):
	global clientList
	for x in range(0, 2):
		clientList.append(MyFrame(None, -1, 'Sample Client', 'localhost', 9099, STATIC_PIPELINE, x + 1, True))
	for x in range(2, 6):
		clientList.append(MyFrame(None, -1, 'Sample Client', 'localhost', 9099, ACTIVE_PIPELINE, x + 1, True))
        self.lock.release()

    def start_local(self):
        self.start_orig()
        self.lock.acquire()

def runMainLoopThread():
    mlt = mainLoopThread()
    global e
    e.wait(1)
    
def wait():
    for y in range(0, 6):
	clientList[y].step(None)

def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    runMainLoopThread()
    
if __name__ == "__main__":
    main()