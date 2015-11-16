import socket   #socket for Peer-to-Peer and Client-Server comms.
import time     
import sys      #sys calls
import select   #import to poll keyboard for press
import datetime

SERVER_IP = '159.203.31.96'  #server IP
SERVER_PORT = 6000         #server port

def main():
    print socket.gethostbyname(socket.gethostname())
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
            k = 0
            out = s.recvfrom(1024)
            data = out[0]
            self.addr = out[1]
            print self.addr
            if not data:
                break;
            result = data.split(':')
            if data == result[1]:
                answer = self.for_table[data]
            else:
                for i in self.for_table.keys():
                    if i == result[0]:
                        answer = 'That numerical ID is taken, please restart the messenger and try again'
                        k = 1
                        break
                    else:
                        answer = 'IP...' + result[1] + ' port...' + result[2]
                if k == 0:
                    self.for_table[result[0]] = result[1] + ":" + result[2]
                
                
            send_to = self.for_table[result[0]].split(':')
            print send_to[0]
            print send_to[1]
            #s.sendto(answer, (send_to[0], int(send_to[1])))
            s.sendto(answer, self.addr)
            #print int(result[1])
            
            print "[" + self.addr[0] + ":" + str(self.addr[1]) + "] :: " + data
            print self.for_table
    def kill(self):
        self.active = False
        s.close()

if __name__ == "__main__":
    main()
