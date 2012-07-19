#!/usr/bin/env python

import wx
import socket
import logging
import sys
import cv
import struct

from simulator.panda3d.server.socket_packet import SocketPacket

#Message Types
VV_ACK_OK = 0
VV_CAM_LIST = 1
VV_IMG = 2
VV_REQ_SIGNATURE = 3
VV_TRACK_SIGNATURE = 4
VV_REQ_VIDEO_ANALYSIS = 5
VV_SYNC_ACK = 6
VV_READY = 7
VV_CAM_MESSAGE = 8
VV_VP_ACK_OK = 9
VV_VP_ACK_FAILED = 10

VP_SESSION = 100
VP_REQ_IMG = 101
VP_REQ_CAM_LIST = 102
VP_TRACKING_DATA = 103
VP_SIGNATURE = 104
VP_CAM_PAN = 105
VP_CAM_TILT = 106
VP_CAM_ZOOM = 107
VP_CAM_DEFAULT = 108
VP_CAM_IMAGE = 109
VP_CAM_RESOLUTION = 110
VP_CAM_CUSTOM_PAN = 111

SYNC_SESSION = 200
SYNC_REQ_CAM_LIST = 201
SYNC_REMOTE_CAM_LIST = 202
SYNC_STEP = 203
SYNC_CAM_MESSAGE = 204

STATIC_PIPELINE = 0
ACTIVE_PIPELINE = 1

SESSION_TYPE = 1

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title, ip_address, port):
        wx.Frame.__init__(self, parent, id, title, size=(1450, 800))
        self.panel = wx.Panel(self, -1)

        self.pipeline = [STATIC_PIPELINE, ACTIVE_PIPELINE, ACTIVE_PIPELINE, ACTIVE_PIPELINE, ACTIVE_PIPELINE, ACTIVE_PIPELINE]
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.step, self.timer)
        self.timer.Start(10, oneShot=False)
        
        self.camera_list = [1, 2, 3, 4, 5, 6];
        self.dictionary = {0: (1, 1), 1: (451, 1), 2: (901, 1), 3: (1, 401), 4: (451, 401), 5: (901, 401)}
        self.camera_dropdown1 = wx.Choice(parent = self.panel, pos = (166, 400))
        self.camera_dropdown2 = wx.Choice(parent = self.panel, pos = (499, 400))
        self.camera_dropdown3 = wx.Choice(parent = self.panel, pos = (832, 400))
        self.camera_numbers = ['1', '2', '3', '4', '5', '6']
        self.camera_dropdown1.AppendItems(strings=self.camera_numbers)
        self.camera_dropdown2.AppendItems(strings=self.camera_numbers)
        self.camera_dropdown3.AppendItems(strings=self.camera_numbers)
        self.camera_dropdown1.Select(n=0)
        self.camera_dropdown2.Select(n=1)
        self.camera_dropdown3.Select(n=2)
        wx.EVT_CHOICE(self, self.camera_dropdown1.GetId(), self.setCamera1)
        wx.EVT_CHOICE(self, self.camera_dropdown2.GetId(), self.setCamera2)
        wx.EVT_CHOICE(self, self.camera_dropdown3.GetId(), self.setCamera3)
        
        self.client_sockets = [None]*len(self.camera_numbers)
        self.read_buffers = [None]*len(self.camera_numbers)
        self.write_buffers = [None]*len(self.camera_numbers)
        self.read_states = [None]*len(self.camera_numbers)
        self.packets = [None]*len(self.camera_numbers)
        self.count = 0
        self.read_body_lengths = [None]*len(self.camera_numbers)
        self.client_ids = [None]*len(self.camera_numbers)
        
        try:
            for i in range(0, len(self.camera_numbers)):
		logging.debug("Connecting to server with IP: %s and PORT: %s" 
			      %(ip_address, port))
		self.read_buffers[(int)(self.camera_numbers[i]) - 1] = ''
		self.write_buffers[(int)(self.camera_numbers[i]) - 1] = ''
		self.read_states[(int)(self.camera_numbers[i]) - 1] = 0
		self.packets[(int)(self.camera_numbers[i]) - 1] = SocketPacket()
		self.client_sockets[(int)(self.camera_numbers[i]) - 1] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_sockets[(int)(self.camera_numbers[i]) - 1].connect((ip_address, port))
		self.client_sockets[(int)(self.camera_numbers[i]) - 1].setblocking(0)
	
	except Exception as e:
            print "Error connecting to server!"
            print e
            sys.exit(0)
            
	refresh_btn = wx.Button(self.panel, label="Refresh", pos=(1351, 1))
	refresh_btn.Bind(wx.EVT_KEY_DOWN, self.refresh)
    
    
    def refresh(self, event):
	print "Button has been pressed\n"
	keycode = event.GetKeyCode()
	if keycode == wx.WXK_SPACE:
	      self.getNewImages()
        event.Skip()
        
    def setCamera1(self, event):
	choice = event.GetString()
	self.camera_list[0] = int(choice)
	print("Value changed in list 1 to ", choice, "\n")

	
    def setCamera2(self, event):
	choice = event.GetString()
	self.camera_list[1] = int(choice)
	print("Value changed in list 2 to ", choice, "\n")
	
	
    def setCamera3(self, event):
	choice = event.GetString()
	self.camera_list[2] = int(choice)
	print("Value changed in list 3 to ", choice, "\n")
	
	
    def step(self, event):
        self.reader_polling()
        #self.getNewImages()
        self.write_polling()
        
    def write_packet(self, packet, camera_number):
        self.write_buffers[camera_number] = self.write_buffers[camera_number] + packet.get_header() + packet.get_body()
        
    def write_polling(self):
        for i in range(0, len(self.camera_list)):
	    if self.write_buffers[(int)(self.camera_list[i])-1] <> '':
		self.client_sockets[(int)(self.camera_list[i])-1].send(self.write_buffers[(int)(self.camera_list[i])-1])
	    self.write_buffers[(int)(self.camera_list[i])-1] = ''
	return
        
    def reader_polling(self):
        for i in range(0, len(self.camera_list)):
	    data=""
	    try:
		data = self.client_sockets[(int)(self.camera_list[i])-1].recv(1024)
	    except socket.error, ex:
		pass
	  
	    if data != '':
		self.read_buffers[(int)(self.camera_list[i])-1] = self.read_buffers[(int)(self.camera_list[i])-1] + data

	    while (True):
		if self.read_states[(int)(self.camera_list[i])-1] == 0:
		    if len(self.read_buffers[(int)(self.camera_list[i])-1]) >= self.packets[(int)(self.camera_list[i])-1].header_length:
			bytes_consumed = self.packets[(int)(self.camera_list[i])-1].header_length
			self.packets[(int)(self.camera_list[i])-1].header = self.read_buffers[(int)(self.camera_list[i])-1][:bytes_consumed]
			self.read_body_lengths[(int)(self.camera_list[i])-1] = self.packets[(int)(self.camera_list[i])-1].decode_header()  # consumes packet.data
			self.read_buffers[(int)(self.camera_list[i])-1] = self.read_buffers[(int)(self.camera_list[i])-1][bytes_consumed:]
			self.read_states[(int)(self.camera_list[i])-1] = 1

		    else:
			break
            
		if self.read_states[(int)(self.camera_list[i])-1] == 1:
		    if len(self.read_buffers[(int)(self.camera_list[i])-1]) >= self.read_body_lengths[(int)(self.camera_list[i])-1]:
			bytes_consumed = self.read_body_lengths[(int)(self.camera_list[i])-1]
			self.packets[(int)(self.camera_list[i])-1].data = self.read_buffers[(int)(self.camera_list[i])-1][:bytes_consumed]
			self.packets[(int)(self.camera_list[i])-1].offset = 0
			self.read_body_lengths[(int)(self.camera_list[i])-1] = 0
			self.read_buffers[(int)(self.camera_list[i])-1] = self.read_buffers[(int)(self.camera_list[i])-1][bytes_consumed:]
			self.read_states[(int)(self.camera_list[i])-1] = 0
			self.new_data_callback(self.packets[(int)(self.camera_list[i])-1])

		    else:
			break
	return
         
        
    def new_data_callback(self, packet):
        message_type = packet.get_int()
        if message_type == VV_ACK_OK:
	    server_ip = packet.get_string()
	    server_port = packet.get_int()
	    self.client_ids[self.count] = packet.get_int()
	    logging.info("Connection Established.")

	    w = SocketPacket()
	    w.add_int(VP_SESSION)
	    w.add_int(self.client_ids[self.count])
	    w.add_char(SESSION_TYPE)
	    w.add_char(self.pipeline[self.count])
	    w.add_int(self.count+1)
	    w.encode_header()
	    self.write_packet(w, self.count)
	      
	    self.count+=1

        elif message_type == VV_VP_ACK_OK:
          packet.get_string()
          packet.get_int()
          cam_id = packet.get_int()


        elif message_type == VV_REQ_VIDEO_ANALYSIS:
            logging.debug("VV_REQ_VIDEO_ANALYSIS")
            ip = packet.get_string()
            port = packet.get_int()
            camera_id = packet.get_int()


        elif message_type == VV_IMG:
            logging.debug("NEW IMAGE")
            server_ip = packet.get_string()
            server_port = packet.get_int()
            cam_id = packet.get_int()
            width = packet.get_int()
            height = packet.get_int()
            depth = packet.get_int()
            color_code = packet.get_char()
            jpeg =  packet.get_bool()
            time = packet.get_double()
            image = packet.get_string()
	   
	    cv_im = self.createImage(cam_id, image, width, height, depth, color_code, jpeg)
	    wxImage = wx.EmptyImage(width, height)
	    wxImage.SetData(cv_im.tostring())
            wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(wxImage), self.dictionary[self.camera_list.index(cam_id)], (wxImage.GetWidth(), wxImage.GetHeight()))
        
    def pan(self, direction, degrees, speed):
	print
	

    def getNewImages(self):
	for i in range(0, len(self.camera_list)):
	    w = SocketPacket()
	    w.add_int(VP_CAM_IMAGE)
	    temp = self.client_ids[(int)(self.camera_list[i])-1]
	    if temp is None:
		  return
	    w.add_int(self.client_ids[(int)(self.camera_list[i])-1])
	    w.add_int((int)(self.camera_list[i]))
	    w.encode_header()
	    self.write_packet(w, (int)(self.camera_list[i])-1)
	    
	
    def createImage(self, cam_id, image_data, width, height, depth, color_code, jpeg=False):
        if jpeg:
            length = len(image_data)
            image = cv.CreateMatHeader(1, length, cv.CV_8UC1)
            cv.SetData(image, image_data, length)
            return cv.DecodeImage(image)
        else:
            image = cv.CreateImageHeader((width, height), depth, 4)
            cv.SetData(image, image_data)
	
	
def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    app = wx.App()
    frame = MyFrame(None, -1, 'Main Controller', 'localhost', 9099)
    frame.Show(True)
    app.MainLoop()
  
if __name__ == "__main__":
    main()
