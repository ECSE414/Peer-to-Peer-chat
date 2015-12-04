import socket   #socket for Peer-to-Peer and Client-Server comms.
import time
import sys      #sys calls
import select   #import to poll keyboard for press
import datetime
import re

SERVER_IP = '159.203.31.96'  #server IP
SERVER_PORT = 6000          #server port
NO_NAME = '%-1,'            #resevered character sequences
RESV1 = '-1'
RESV2 = '-2'
RESV3 = '-3'
RESV4 = '-4'
def main():
    #print socket.gethostbyname(socket.gethostname())
    #start server
    server = Server()
    server.start()

class Server():
    def __init__(self):
        self.addr = (SERVER_IP, SERVER_PORT)
        self.active = True
        self.for_table = {  };  #"forwarding Table" -- all users
        self.avail = {  };      #Available users
    def start(self):
        #bind to socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((SERVER_IP, SERVER_PORT))
        while 1:
            #set "should we send data" to TRUE
            send = True
            #Conditional check for adding entries or not
            add = 0
            #wait to recv data from clients
            out = s.recvfrom(1024)
            data = out[0]
            addr = out[1]
            answer = "\0"
            print addr
            #make sure data was received
            if not data:
                break;
            print data
            result = re.split(':|\n', data)
            print result

            #add information to available users if in menu
            #self.avail[result[0]] = str(addr[0]) + ':' + str(addr[1])

            #check to see who to send to
            if result[1] in self.for_table:
                #remove self from avail list
                del self.avail[result[0]]
                if result[1] in self.avail:
                    answer = self.avail[result[1]]
                else:
                    answer = self.for_table[result[1]]
                send = True
            #if RESV code 1 was sent...exit and delete entries
            elif result[1] == RESV1:
                del self.for_table[result[0]]
                del self.avail[result[0]]
                send = False
            #if RESV code 2 was sent, re-add entry to avail list
            elif result[1] == RESV2:
                self.avail[result[0]] = str(addr[0]) + ':' + str(addr[1])
                send = False
            #if RESV code 3 was sent, return available users
            elif result[1] == RESV3:
                answer = str(self.avail.keys())
            #if RESV code 4 was sent, return all online
            elif result[1] == RESV4:
                answer = str(self.for_table.keys())
            #else means its a new entry to the forwarding table, so update or reject if ID is taken
            else:
                answer = 'IP...' + result[1] + ' port...' + result[2]
                for i in self.for_table:
                    #if ID is taken return invalid seq
                    if i == result[0]:
                        answer = NO_NAME
                        add = 1
                        break
                if add == 0:
                    self.for_table[result[0]] = addr[0] + ":" + addr[1]
                    self.avail[result[0]] = addr[0] + ":" + addr[1]
            #if data to send, send.
            if send == True:
                s.sendto(answer, addr)
            print "[" + addr[0] + ":" + str(addr[1]) + "] :: " + data
            print self.for_table
    #used to close connection
    def kill(self):
        self.active = False
        s.close()

if __name__ == "__main__":
    main()
