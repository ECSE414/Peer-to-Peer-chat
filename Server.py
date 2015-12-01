import socket   #socket for Peer-to-Peer and Client-Server comms.
import time
import sys      #sys calls
import select   #import to poll keyboard for press
import datetime
import re

SERVER_IP = '159.203.31.96'  #server IP
SERVER_PORT = 6000         #server port
NO_NAME = '%-1,'
def main():
    print socket.gethostbyname(socket.gethostname())
    server = Server()
    server.start()

class Server():
    def __init__(self):
        self.addr = (SERVER_IP, SERVER_PORT)
        self.active = True
        self.for_table = {  };
        self.avail = {  };
    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((SERVER_IP, SERVER_PORT))
        while 1:
            send = True
            k = 0
            out = s.recvfrom(1024)
            data = out[0]
            addr = out[1]
            answer = "\0"
            print addr
            if not data:
                break;
            print data
            result = re.split(':|\n', data)
            print result
            self.avail[result[0]] = str(addr[0]) + ':' + str(addr[1])

            if result[1] in self.for_table:
                if result[1] in self.avail:
                    del self.avail[result[0]]
                    answer = self.avail[result[1]]
                else:
                    answer = NO_NAME
            elif result[1] == '-1':
                del self.for_table[result[0]]
                del self.avail[result[0]]
                send = False
            elif result[1] == '-2':
                self.avail[result[0]] = str(addr[0]) + ':' + str(addr[1])
                send = False
            elif result[1] == '-3':
                answer = str(self.avail.keys())
            elif result[1] == '-4':
                answer = str(self.for_table.keys())
            else:
                answer = 'IP...' + result[1] + ' port...' + result[2]
                for i in self.for_table:
                    if i == result[0] or result[0] == NO_NAME:
                        answer = NO_NAME
                        k = 1
                        break
                if k == 0:
                    self.for_table[result[0]] = result[1] + ":" + result[2]
                    self.avail[result[0]] = result[1] + ":" + result[2]

            #send_to = self.for_table[result[0]].split(':')
            #print send_to[0]
            #print send_to[1]
            #s.sendto(answer, (send_to[0], int(send_to[1])))
            if send == True:
                s.sendto(answer, addr)
            #print int(result[1])

            print "[" + addr[0] + ":" + str(addr[1]) + "] :: " + data
            print self.for_table
    def kill(self):
        self.active = False
        s.close()

if __name__ == "__main__":
    main()
