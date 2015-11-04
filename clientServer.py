import socket
import time
import sys
import select
from random import randint

SERVER_IP = 'localhost'  #server IP
SERVER_PORT = 6000         #server port

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
            client.host = 'localhost'
            client.port = 5000
            client.setupServerConn()
            #client.setupChatRecv('localhost', 8000)
        elif client.ID == '2':
            client.host = 'localhost'
            client.port = 8000
            client.setupServerConn()
            #client.setupChatSend('localhost', 5000)
            
    elif type == 'server':
        server = Server()
        server.start()
    
class Server():
    def __init__(self):
        self.addr = None
        self.active = True
        self.for_table = { '0' : SERVER_IP + ":" + str(SERVER_PORT) };
    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((SERVER_IP, SERVER_PORT))
        while 1:
            out = s.recvfrom(1024)
            data = out[0]
            self.addr = out[1]

            if not data:
                break;
            result = data.split(':', 2)
            #global for_table
            self.for_table[result[2]] = result[0] + ":" + result[1]
            answer = 'OK...' + result[0] + ' port...' + result[1]
            s.sendto(answer, self.addr)
            print "[" + self.addr[0] + ":" + str(self.addr[1]) + "] :: " + data
            print self.for_table
    def kill(self):
        self.active = False
        s.close()

class Client():
    def __init__(self):
        self.host = None
        self.port = None
        self.ID = None
        self.active = True

    def setupChatRecv(self, dest, dest_port):
        #self.kill()
        self.active = True
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, self.port))
        x = 1
        while 1:
            while (x == 1):
                out = s.recvfrom(1024)
                data = out[0]
                addr = out[1]

                if not data:
                    break;
                answer = "message received..."
                s.sendto(answer, (dest, dest_port))
                print "[" + dest + ":" + str(dest_port) + "] ::" + data
                x = 0
            while (x == 0):
                msg = raw_input('Enter message to send: ')

                s.sendto(msg, (dest, dest_port))

                out = s.recvfrom(1024)
                data = out[0]
                addr = out[1]

                print data
                x = 1
    def setupChatSend(self, dest, dest_port):
        #self.kill()
        self.active = True
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, self.port))
        x = 0
        while 1:
            while (x == 1):
                out = s.recvfrom(1024)
                data = out[0]
                addr = out[1]

                if not data:
                    break;
                answer = "message received..."
                s.sendto(answer, (dest, dest_port))
                print "[" + dest + ":" + str(dest_port) + "] ::" + data
                x = 0
            while (x == 0):
                msg = raw_input('Enter message to send: ')

                s.sendto(msg, (dest, dest_port))

                out = s.recvfrom(1024)
                data = out[0]
                addr = out[1]

                print data
                x = 1

    def setupServerConn(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while 1:
            msg = self.host + ':' + str(self.port) + ':' + str(self.ID)
            s.sendto(msg,(SERVER_IP, SERVER_PORT))
        
            out = s.recvfrom(1024)
            data = out[0]
            addr = out[1]

            print 'Your info: ' + data
    def kill(self):
        self.active = False
        s.close()

if __name__ == "__main__":
    main()