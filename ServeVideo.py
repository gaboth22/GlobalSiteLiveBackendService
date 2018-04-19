import SimpleHTTPServer
import SocketServer
import sys

def main(port):
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), handler)
    print "Serving on port: ", port
    httpd.serve_forever()

if __name__ == '__main__':
    main(int(sys.argv[1]))
