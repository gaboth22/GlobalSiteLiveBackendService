import socket
import SimpleHTTPServer
import SocketServer
import sys
import os

class ReusableTCPServer(SocketServer.TCPServer):
   def server_bind(self):
      self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.socket.bind(self.server_address)

class VideoServer:
   def start(self, path_to_serve, port):
      while not os.path.isdir(path_to_serve):
         pass
      handler = SimpleHTTPServer.SimpleHTTPRequestHandler
      httpd = ReusableTCPServer(("", port), handler)
      print "Serving on port: ", port
      httpd.serve_forever()