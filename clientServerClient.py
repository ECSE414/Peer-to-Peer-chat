import socket
import time
import sys
from random import randint

HOST = ''
PORT = 5000

def main():
    test_server = Server()
    test_server.start()


#class Client():
#    def __init__(self):
#        self.host = None
#        self.sock = None
#        self.active = True;
    
    
class Server():
    def __init__(self):
        self.addr = None
        self.Active = True

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((HOST, PORT))
        while 1:
            data, self.addr = s.recvfrom(1024)
            
            if not data:
                break;

            answer = 'OK...' + data
            s.sendto(answer, addr)
            print "[" + addr[0] + ":" + str(addr[1]) + "] :: " + data
    def kill(self):
        self.Active = False


if __name__ == "__main__":
    main();