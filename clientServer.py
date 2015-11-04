import socket
import time
import sys
import select
from random import randint


def main():
    type = raw_input('Please enter your type: ')
    type = type.lower()
    #print type
    if type == 'client':
        num = raw_input('Please enter your numerical id: ')
        client = Client()
        client.ID = num
        #print client.ID
        if client.ID == '1':
            client.setupChatRecv('localhost', 5000, 'localhost', 8000)
        elif client.ID == '2':
            client.setupChatSend('localhost', 8000, 'localhost', 5000)
            
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
        self.ID = None
        self.active = True

    def setupChatRecv(self, host, port, dest, dest_port):
        #self.kill()
        self.active = True
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        x = 1
        while 1:
            while (x == 1):
                out = s.recvfrom(1024)
                data = out[0]
                addr = input[1]

                if not data:
                    break;
                answer = "message received..."
                s.sendto(answer, (dest, dest_port))
                print "[" + dest + ":" + dest_port + "] ::" + data
                x = 0
            while (x == 0):
                msg = raw_input('Enter message to send: ')

                s.sendto(msg, (dest, dest_port))

                out = s.recvfrom(1024)
                data = out[0]
                addr = out[1]

                print "[" + addr[0] + ":" + str(addr[1]) + "] :: " + data
                x = 1
    def setupChatSend(self, host, port, dest, dest_port):
        #self.kill()
        self.active = True
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        x = 0
        while 1:
            while (x == 1):
                out = s.recvfrom(1024)
                data = out[0]
                addr = input[1]

                if not data:
                    break;
                answer = "message received..."
                s.sendto(answer, (dest, dest_port))
                print "[" + dest + ":" + dest_port + "] ::" + data
                x = 0
            while (x == 0):
                msg = raw_input('Enter message to send: ')

                s.sendto(msg, (dest, dest_port))

                out = s.recvfrom(1024)
                data = out[0]
                addr = out[1]

                print "[" + addr[0] + ":" + str(addr[1]) + "] :: " + data
                x = 1
    def setupServerConn(self):
        HOST = 'localhost'
        PORT = 5000
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while 1:
            msg = raw_input('Enter message: ')
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