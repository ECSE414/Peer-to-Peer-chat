import socket
import time
import sys
from random import randint


def main():
    type = raw_input('Please enter your type: ')
    type = type.lower()
    print type
    if type == 'client':
        client = Client()
        client.start()
    elif type == 'server':
        server = Server()
        server.start()

#class Client():
#    def __init__(self):
#        self.host = None
#        self.sock = None
#        self.active = True;
    
    
class Server():
    def __init__(self):
        self.addr = None
        self.active = True

    def start(self):
        HOST = ''
        PORT = 5000
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((HOST, PORT))
        while 1:
            out = s.recvfrom(1024)
            data = out[0]
            self.addr = out[1]

            if not data:
                break;

            answer = 'OK...' + data
            s.sendto(answer, self.addr)
            print "[" + self.addr[0] + ":" + str(self.addr[1]) + "] :: " + data
    def kill(self):
        self.active = False
        s.close()

class Client():
    def __init__(self):
        #self.host = None
        self.sock = None
        self.active = True
    def start(self):
        HOST = 'localhost'
        PORT = 5000
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while 1:
            msg = raw_input('Enter messgae: ')
            s.sendto(msg,(HOST, PORT))
        
            out = s.recvfrom(1024)
            data = out[0]
            addr = out[1]

            print 'Server: ' + data
    def kill(self):
        self.active = False
        s.close()

if __name__ == "__main__":
    main()