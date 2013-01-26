#!/usr/bin/env python

import wx
import socket
import logging
import sys
import cv

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
VP_CAM_CUSTOM_TILT = 112
VP_CAM_CUSTOM_ZOOM = 113

SYNC_SESSION = 200
SYNC_REQ_CAM_LIST = 201
SYNC_REMOTE_CAM_LIST = 202
SYNC_STEP = 203
SYNC_CAM_MESSAGE = 204

STATIC_PIPELINE = 0
ACTIVE_PIPELINE = 1

SESSION_TYPE = 1

DEFAULT_PAN_SPEED = 20.0 #degrees per second
DEFAULT_TILT_SPEED = 20.0 #degrees per second
DEFAULT_ZOOM_SPEED = 20.0 #degrees per second

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title, ip_address, port):
        wx.Frame.__init__(self, parent, id, title, size=(1350, 800))
        self.panel = wx.Panel(self, -1)
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.step, self.timer)
        self.timer.Start(10, oneShot=False)
        
        self.camera_list = [3, 2, 1, 4, 5, 6];
        self.top_left_corners = {0: (0, 0), 1: (450, 0), 2: (900, 0), 3: (0, 400), 4: (450, 400), 5: (900, 400)}
        self.camera_numbers = ['1', '2', '3', '4', '5', '6']
        self.pipeline = [STATIC_PIPELINE, STATIC_PIPELINE, ACTIVE_PIPELINE, ACTIVE_PIPELINE, ACTIVE_PIPELINE, ACTIVE_PIPELINE]
        
        self.client_sockets = [None]*len(self.camera_numbers)
        self.read_buffers = [None]*len(self.camera_numbers)
        self.write_buffers = [None]*len(self.camera_numbers)
        self.read_states = [None]*len(self.camera_numbers)
        self.packets = [None]*len(self.camera_numbers)
        self.read_body_lengths = [None]*len(self.camera_numbers)
        self.client_ids = [None]*len(self.camera_numbers)
        self.counts = [None] * len(self.camera_numbers)
        
        try:
            for i in range(0, len(self.camera_numbers)):
		logging.debug("Connecting to server with IP: %s and PORT: %s" 
			      %(ip_address, port))
		self.read_buffers[i] = ''
		self.write_buffers[i] = ''
		self.read_states[i] = 0
		self.packets[i] = SocketPacket()
		self.client_sockets[i] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_sockets[i].connect((ip_address, port))
		self.client_sockets[i].setblocking(0)
		self.counts[i] = 0
	
	
	except Exception as e:
            print "Error connecting to server!"
            print e
            sys.exit(0)
	
	self.pan_angle_values = [None] * 6
	self.pan_speed_values = [None] * 6
	self.tilt_angle_values = [None] * 6
	self.tilt_speed_values = [None] * 6
	self.zoom_angle_values = [None] * 6
	self.zoom_speed_values = [None] * 6
	self.pan_buttons = [None] * 6
	self.tilt_buttons = [None] * 6
	self.zoom_buttons = [None] * 6
	self.left_buttons = [None] * 6
	self.right_buttons = [None] * 6
	self.up_buttons = [None] * 6
	self.down_buttons = [None] * 6
	self.plus_buttons = [None] * 6
	self.minus_buttons = [None] * 6
	self.image_buttons = [None] * 6
	self.angle_texts = [None] * 18
	self.speed_texts = [None] * 18
	
	for i in range(0, 6):
	    self.pan_buttons[i] = wx.Button(self.panel, id = -1, label = 'Pan', name = 'Pan Camera ' + str(self.camera_list[i]) + ' Index ' + str(i), pos = ((self.top_left_corners[i])[0] + 10, (self.top_left_corners[i])[1] + 22), size=(50, 25))
	    self.tilt_buttons[i] = wx.Button(self.panel, id = -1, label = 'Tilt', name = 'Tilt Camera ' + str(self.camera_list[i]) + ' Index ' + str(i), pos = ((self.top_left_corners[i])[0] + 10, (self.top_left_corners[i])[1] + 57), size=(50, 25))
	    self.zoom_buttons[i] = wx.Button(self.panel, id = -1, label = 'Zoom', name = 'Zoom Camera ' + str(self.camera_list[i]) + ' Index ' + str(i), pos = ((self.top_left_corners[i])[0] + 10, (self.top_left_corners[i])[1] + 92), size=(50, 25))
	    self.image_buttons[i] = wx.Button(self.panel, id = -1, label = 'Get Image', name = 'Get Image from Camera ' + str(self.camera_list[i]) + ' Index ' + str(i), pos = ((self.top_left_corners[i])[0] + 10, (self.top_left_corners[i])[1] + 127))
	    self.left_buttons[i] = wx.Button(self.panel, id = -1, label = 'Left', name = 'Left Camera ' + str(self.camera_list[i]) + ' Index ' + str(i), pos = ((self.top_left_corners[i])[0] + 120, (self.top_left_corners[i])[1] + 200), size=(50, 25))
	    self.right_buttons[i] = wx.Button(self.panel, id = -1, label = 'Right', name = 'Right Camera ' + str(self.camera_list[i]) + ' Index ' + str(i), pos = ((self.top_left_corners[i])[0] + 180, (self.top_left_corners[i])[1] + 200), size=(50, 25))
	    self.up_buttons[i] = wx.Button(self.panel, id = -1, label = 'Up', name = 'Up Camera ' + str(self.camera_list[i]) + ' Index ' + str(i), pos = ((self.top_left_corners[i])[0] + 150, (self.top_left_corners[i])[1] + 170), size=(50, 25))
	    self.down_buttons[i] = wx.Button(self.panel, id = -1, label = 'Down', name = 'Down Camera ' + str(self.camera_list[i]) + ' Index ' + str(i), pos = ((self.top_left_corners[i])[0] + 150, (self.top_left_corners[i])[1] + 230), size=(50, 25))
	    self.plus_buttons[i] = wx.Button(self.panel, id = -1, label = '+', name = 'Down Camera ' + str(self.camera_list[i]) + ' Index ' + str(i), pos = ((self.top_left_corners[i])[0] + 140, (self.top_left_corners[i])[1] + 270), size=(25, 25))
	    self.minus_buttons[i] = wx.Button(self.panel, id = -1, label = '-', name = 'Down Camera ' + str(self.camera_list[i]) + ' Index ' + str(i), pos = ((self.top_left_corners[i])[0] + 185, (self.top_left_corners[i])[1] + 270), size=(25, 25))
	    (self.pan_buttons[i]).Bind(wx.EVT_BUTTON, self.pan)
	    (self.tilt_buttons[i]).Bind(wx.EVT_BUTTON, self.tilt)
	    (self.zoom_buttons[i]).Bind(wx.EVT_BUTTON, self.zoom)
	    (self.image_buttons[i]).Bind(wx.EVT_BUTTON, self.getImage)
	    (self.left_buttons[i]).Bind(wx.EVT_BUTTON, self.panLeft)
	    (self.right_buttons[i]).Bind(wx.EVT_BUTTON, self.panRight)
	    (self.up_buttons[i]).Bind(wx.EVT_BUTTON, self.tiltUp)
	    (self.down_buttons[i]).Bind(wx.EVT_BUTTON, self.tiltDown)
	    (self.plus_buttons[i]).Bind(wx.EVT_BUTTON, self.zoomIn)
	    (self.minus_buttons[i]).Bind(wx.EVT_BUTTON, self.zoomOut)
	    for j in range(3 * i, 3 * i + 3):
		self.angle_texts[j] = wx.StaticText(self.panel, -1, "Angle", ((self.top_left_corners[i])[0] + 80, (self.top_left_corners[i])[1] + 25 + 35 * (j - 3 * i)))
		self.speed_texts[j] = wx.StaticText(self.panel, -1, "Speed", ((self.top_left_corners[i])[0] + (self.angle_texts[j].GetSize())[0] + 210, (self.top_left_corners[i])[1] + 25 + 35 * (j - 3 * i)))
	    self.pan_angle_values[i] = wx.TextCtrl(self.panel, pos = ((self.top_left_corners[i])[0] + 80 + (self.angle_texts[i].GetSize())[0] + 10, (self.top_left_corners[i])[1] + 22), size = (100,25))
	    self.tilt_angle_values[i] = wx.TextCtrl(self.panel, pos = ((self.top_left_corners[i])[0] + 80 + (self.angle_texts[i].GetSize())[0] + 10, (self.top_left_corners[i])[1] + 57), size = (100, 25))
	    self.zoom_angle_values[i] = wx.TextCtrl(self.panel, pos = ((self.top_left_corners[i])[0] + 80 + (self.angle_texts[i].GetSize())[0] + 10, (self.top_left_corners[i])[1] + 92), size = (100, 25))
	    self.pan_speed_values[i] = wx.TextCtrl(self.panel, pos = ((self.top_left_corners[i])[0] + (self.angle_texts[0].GetSize())[0] + (self.speed_texts[0].GetSize())[0] + 220, (self.top_left_corners[i])[1] + 22), size = (100, 25))
	    self.tilt_speed_values[i] = wx.TextCtrl(self.panel, pos = ((self.top_left_corners[i])[0] + (self.angle_texts[0].GetSize())[0] + (self.speed_texts[0].GetSize())[0] + 220, (self.top_left_corners[i])[1] + 57), size = (100, 25))
	    self.zoom_speed_values[i] = wx.TextCtrl(self.panel, pos = ((self.top_left_corners[i])[0] + (self.angle_texts[0].GetSize())[0] + (self.speed_texts[0].GetSize())[0] + 220, (self.top_left_corners[i])[1] + 92), size = (100, 25))
	
	
    def panLeft(self, event):
	button = event.GetEventObject()
	name_words_list = (button.GetName()).split()
	camera_number = int(name_words_list[2])
	indexTextCtrl = int(name_words_list[4])
	w = SocketPacket()
	w.add_int(VP_CAM_PAN)
	index_camera_numbers = self.camera_numbers.index(str(camera_number))
	w.add_int(self.client_ids[index_camera_numbers])
	w.add_int(camera_number)
	w.add_float(-10.0)
	w.add_float(DEFAULT_PAN_SPEED)
	w.encode_header()
	self.write_packet(w, index_camera_numbers)
	
	
    def panRight(self, event):
	button = event.GetEventObject()
	name_words_list = (button.GetName()).split()
	camera_number = int(name_words_list[2])
	indexTextCtrl = int(name_words_list[4])
	w = SocketPacket()
	w.add_int(VP_CAM_PAN)
	index_camera_numbers = self.camera_numbers.index(str(camera_number))
	w.add_int(self.client_ids[index_camera_numbers])
	w.add_int(camera_number)
	w.add_float(10.0)
	w.add_float(DEFAULT_PAN_SPEED)
	w.encode_header()
	self.write_packet(w, index_camera_numbers)
	
	
    def tiltUp(self, event):
	button = event.GetEventObject()
	name_words_list = (button.GetName()).split()
	camera_number = int(name_words_list[2])
	indexTextCtrl = int(name_words_list[4])
	w = SocketPacket()
	w.add_int(VP_CAM_TILT)
	index_camera_numbers = self.camera_numbers.index(str(camera_number))
	w.add_int(self.client_ids[index_camera_numbers])
	w.add_int(camera_number)
	w.add_float(10.0)
	w.add_float(DEFAULT_TILT_SPEED)
	w.encode_header()
	self.write_packet(w, index_camera_numbers)
	
	
    def tiltDown(self, event):
	button = event.GetEventObject()
	name_words_list = (button.GetName()).split()
	camera_number = int(name_words_list[2])
	indexTextCtrl = int(name_words_list[4])
	w = SocketPacket()
	w.add_int(VP_CAM_TILT)
	index_camera_numbers = self.camera_numbers.index(str(camera_number))
	w.add_int(self.client_ids[index_camera_numbers])
	w.add_int(camera_number)
	w.add_float(-10.0)
	w.add_float(DEFAULT_TILT_SPEED)
	w.encode_header()
	self.write_packet(w, index_camera_numbers)
	
	
    def zoomIn(self, event):
	button = event.GetEventObject()
	name_words_list = (button.GetName()).split()
	camera_number = int(name_words_list[2])
	indexTextCtrl = int(name_words_list[4])
	w = SocketPacket()
	w.add_int(VP_CAM_ZOOM)
	index_camera_numbers = self.camera_numbers.index(str(camera_number))
	w.add_int(self.client_ids[index_camera_numbers])
	w.add_int(camera_number)
	w.add_float(-10.0)
	w.add_float(DEFAULT_ZOOM_SPEED)
	w.encode_header()
	self.write_packet(w, index_camera_numbers)
	
	
    def zoomOut(self, event):
	button = event.GetEventObject()
	name_words_list = (button.GetName()).split()
	camera_number = int(name_words_list[2])
	indexTextCtrl = int(name_words_list[4])
	w = SocketPacket()
	w.add_int(VP_CAM_ZOOM)
	index_camera_numbers = self.camera_numbers.index(str(camera_number))
	w.add_int(self.client_ids[index_camera_numbers])
	w.add_int(camera_number)
	w.add_float(10.0)
	w.add_float(DEFAULT_ZOOM_SPEED)
	w.encode_header()
	self.write_packet(w, index_camera_numbers)
	
	
    def pan(self, event):
	button = event.GetEventObject()
	name_words_list = (button.GetName()).split()
	camera_number = int(name_words_list[2])
	indexTextCtrl = int(name_words_list[4])
	angle_string = (self.pan_angle_values[indexTextCtrl]).GetValue()
	speed_string = (self.pan_speed_values[indexTextCtrl]).GetValue()
	angle = float(angle_string)
	speed = float(speed_string)
	w = SocketPacket()
	w.add_int(VP_CAM_CUSTOM_PAN)
	index_camera_numbers = self.camera_numbers.index(str(camera_number))
	w.add_int(self.client_ids[index_camera_numbers])
	w.add_int(camera_number)
	w.add_float(angle)
	w.add_float(speed)
	w.encode_header()
	self.write_packet(w, index_camera_numbers)


    def tilt(self, event):
	button = event.GetEventObject()
	name_words_list = (button.GetName()).split()
	camera_number = int(name_words_list[2])
	indexTextCtrl = int(name_words_list[4])
	angle_string = (self.tilt_angle_values[indexTextCtrl]).GetValue()
	speed_string = (self.tilt_speed_values[indexTextCtrl]).GetValue()
	angle = float(angle_string)
	speed = float(speed_string)
	w = SocketPacket()
	w.add_int(VP_CAM_CUSTOM_TILT)
	index_camera_numbers = self.camera_numbers.index(str(camera_number))
	w.add_int(self.client_ids[index_camera_numbers])
	w.add_int(camera_number)
	w.add_float(angle)
	w.add_float(speed)
	w.encode_header()
	self.write_packet(w, index_camera_numbers)
	
	
    def zoom(self, event):
	button = event.GetEventObject()
	name_words_list = (button.GetName()).split()
	camera_number = int(name_words_list[2])
	indexTextCtrl = int(name_words_list[4])
	angle_string = (self.zoom_angle_values[indexTextCtrl]).GetValue()
	speed_string = (self.zoom_speed_values[indexTextCtrl]).GetValue()
	angle = float(angle_string)
	speed = float(speed_string)
	w = SocketPacket()
	w.add_int(VP_CAM_CUSTOM_ZOOM)
	index_camera_numbers = self.camera_numbers.index(str(camera_number))
	w.add_int(self.client_ids[index_camera_numbers])
	w.add_int(camera_number)
	w.add_float(angle)
	w.add_float(speed)
	w.encode_header()
	self.write_packet(w, index_camera_numbers)
	
	
    def getImage(self, event):
	button = event.GetEventObject()
	name_words_list = (button.GetName()).split()
	camera_number = int(name_words_list[4])
	w = SocketPacket()
        w.add_int(VP_CAM_IMAGE)
        index_camera_numbers = self.camera_numbers.index(str(camera_number))
        w.add_int(self.client_ids[index_camera_numbers])
        w.add_int(camera_number)
        w.encode_header()
        self.write_packet(w, index_camera_numbers)
    
    
    def step(self, event):
        self.reader_polling()
        self.write_polling()
        
    def write_packet(self, packet, index):
        self.write_buffers[index] = self.write_buffers[index] + packet.get_header() + packet.get_body()
        
    def write_polling(self):
        for i in range(0, len(self.camera_numbers)):
	    if self.write_buffers[i] <> '':
		self.client_sockets[i].send(self.write_buffers[i])
	    self.write_buffers[i] = ''
	return
        
    def reader_polling(self):
        for i in range(0, len(self.camera_numbers)):
	    data=""
	    try:
		data = self.client_sockets[i].recv(1024)
	    except socket.error, ex:
		pass
	  
	    if data != '':
		self.read_buffers[i] = self.read_buffers[i] + data

	    while (True):
		if self.read_states[i] == 0:
		    if len(self.read_buffers[i]) >= self.packets[i].header_length:
			bytes_consumed = self.packets[i].header_length
			self.packets[i].header = self.read_buffers[i][:bytes_consumed]
			self.read_body_lengths[i] = self.packets[i].decode_header()  # consumes packet.data
			self.read_buffers[i] = self.read_buffers[i][bytes_consumed:]
			self.read_states[i] = 1

		    else:
			break
            
		if self.read_states[i] == 1:
		    if len(self.read_buffers[i]) >= self.read_body_lengths[i]:
			bytes_consumed = self.read_body_lengths[i]
			self.packets[i].data = self.read_buffers[i][:bytes_consumed]
			self.packets[i].offset = 0
			self.read_body_lengths[i] = 0
			self.read_buffers[i] = self.read_buffers[i][bytes_consumed:]
			self.read_states[i] = 0
			self.new_data_callback(self.packets[i], i)

		    else:
			break
	return
         
        
    def new_data_callback(self, packet, index):
        message_type = packet.get_int()
        if message_type == VV_ACK_OK:
	    server_ip = packet.get_string()
	    server_port = packet.get_int()
	    self.client_ids[index] = packet.get_int()
	    logging.info("Connection Established.")

	    w = SocketPacket()
	    w.add_int(VP_SESSION)
	    w.add_int(self.client_ids[index])
	    w.add_char(SESSION_TYPE)
	    w.add_char(self.pipeline[index])
	    w.add_int(int(self.camera_numbers[index]))
	    w.encode_header()
	    self.write_packet(w, index)

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
            cv_im = self.createImage(image, width, height, depth, color_code, jpeg)
            index_camera_numbers = self.camera_numbers.index(str(cam_id))
            cv.SaveImage("cam%s_%s.jpg" % (cam_id, self.counts[index_camera_numbers]), cv_im)
            self.counts[index_camera_numbers] += 1
	    cv.ShowImage("Image", cv_im)
            cv.WaitKey()
            
            
    def createImage(self, image_data, width, height, depth, color_code, jpeg=False):
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
    frame = MyFrame(None, -1, 'GUI Camera Controller', 'localhost', 9099)
    frame.Show(True)
    app.MainLoop()
  
if __name__ == "__main__":
    main()