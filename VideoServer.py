#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer

class VideoServer():

   def __init__(self):
      self.server = None

   def initialize_on_port(self, port):
      handler = SimpleHTTPServer.SimpleHTTPRequestHandler
      self.server = SocketServer.TCPServer(("", port), handler)
      print "Serving at port", port
      print "Videos are served under <address>/video_chunks/<video_number>.mp4"
      print "Starting at 0.mp4"

   def handle_requests(self):
      self.server.handle_request()

   def close(self):
      return self.server.server_close()