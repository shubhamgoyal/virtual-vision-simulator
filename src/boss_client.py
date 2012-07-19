#!/usr/bin/env python

import wx
import logging
import threading

from sample_client import MyFrame
from sample_client import panEVT_CUSTOM
from sample_client import tiltEVT_CUSTOM
from sample_client import zoomEVT_CUSTOM
from sample_client import getImageEVT_CUSTOM
from sample_client import DEFAULT_PAN_SPEED
from sample_client import DEFAULT_TILT_SPEED
from sample_client import DEFAULT_ZOOM_SPEED

STATIC_PIPELINE = 0
ACTIVE_PIPELINE = 1

clientList = []
e = threading.Event()

class PanCustomEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        degrees = 0
	speed = DEFAULT_PAN_SPEED

    def SetDegrees(self, val):
        self.degrees = val

    def GetDegrees(self):
        return self.degrees

    def SetSpeed(self, val):
	self.speed = val

    def GetSpeed(self):
	return self.speed
	
class TiltCustomEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        degrees = 0
	speed = DEFAULT_TILT_SPEED

    def SetDegrees(self, val):
        self.degrees = val

    def GetDegrees(self):
        return self.degrees

    def SetSpeed(self, val):
	self.speed = val

    def GetSpeed(self):
	return self.speed

class ZoomCustomEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        degrees = 0
	speed = DEFAULT_ZOOM_SPEED

    def SetDegrees(self, val):
        self.degrees = val

    def GetDegrees(self):
        return self.degrees

    def SetSpeed(self, val):
	self.speed = val

    def GetSpeed(self):
	return self.speed
	
class GetImageCustomEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
	wx.PyCommandEvent.__init__(self, evtType, id)

def pan (camera_number, degrees, speed):
    global clientList
    event = PanCustomEvent(panEVT_CUSTOM, 108)
    event.SetDegrees(degrees)
    event.SetSpeed(speed)
    wx.PostEvent(clientList[camera_number - 1], event)
	
def tilt (camera_number, degrees, speed):
    global clientList
    event = TiltCustomEvent(tiltEVT_CUSTOM, 109)
    event.SetDegrees(degrees)
    event.SetSpeed(speed)
    wx.PostEvent(clientList[camera_number - 1], event)

def zoom (camera_number, degrees, speed):
    global clientList
    event = ZoomCustomEvent(zoomEVT_CUSTOM, 111)
    event.SetDegrees(degrees)
    event.SetSpeed(speed)
    wx.PostEvent(clientList[camera_number - 1], event)
	
def getImage(camera_number):
    global clientList
    event = GetImageCustomEvent(getImageEVT_CUSTOM, 112)
    wx.PostEvent(clientList[camera_number - 1], event)
	
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
        app = wx.App()
	global clientList
	for x in range(0, 2):
		clientList.append(MyFrame(None, -1, 'Sample Client', 'localhost', 9099, STATIC_PIPELINE, x + 1, True))
		clientList[x].Show(True)
	for x in range(2, 6):
		clientList.append(MyFrame(None, -1, 'Sample Client', 'localhost', 9099, ACTIVE_PIPELINE, x + 1, True))
		clientList[x].Show(True)
        self.lock.release()
        app.MainLoop()

    def start_local(self):
        self.start_orig()
        self.lock.acquire()

def runMainLoopThread():
    mlt = mainLoopThread()
    global e
    e.wait(4)

def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    runMainLoopThread()

if __name__ == "__main__":
    main()
