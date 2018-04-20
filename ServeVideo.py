import SimpleHTTPServer
import SocketServer
import sys
import os

def main(path_to_serve, port):
    os.chdir(path_to_serve)
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), handler)
    print "Serving on port: ", port
    httpd.serve_forever()

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))