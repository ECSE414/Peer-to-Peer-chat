import socket
import time
import sys
import select
import datetime

TIMEOUT = 1000
#common flags
READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT

SERVER_IP = '159.203.31.96'  #server IP
SERVER_PORT = 6000         #server port

def main():
    print socket.gethostbyname(socket.gethostname())
    type = raw_input('Please enter your type: ')
    type = type.lower()
    #print type
    if type == 'client':
        num = raw_input('Please enter your numerical id: ')
        client = Client()
        client.ID = num
        #print client.ID
        if client.ID == '1':
            client.host = socket.gethostbyname(socket.gethostname())
            client.port = 5000
            client.setupServerConn()
            to = raw_input('Who would you like to contact?')
            conn = client.requestBuddy(to)
            client.setupChat(conn[0], int(conn[1]))
        elif client.ID == '2':
            client.host = socket.gethostbyname(socket.gethostname())
            client.port = 8000
            client.setupServerConn()
            to = raw_input('Who would you like to contact?')
            conn = client.requestBuddy(to)
            client.setupChat(conn[0], int(conn[1]))
            
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
            print addr
            if not data:
                break;
            result = data.split(':', 2)
            if data == result[1]:
                answer = self.for_table[data]
            else:
                self.for_table[result[0]] = result[1] + ":" + result[2]
                answer = 'IP...' + result[1] + ' port...' + result[2]
                
            
            s.sendto(answer, (self.addr[0], int(self.addr[1])))
            #print int(result[1])
            
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
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.poller = select.poll()
        self.active = True

    def getLine(self):
        i,o,e = select.select([sys.stdin],[],[],0.0001)
        for s in i:
            if s == sys.stdin:
                input = sys.stdin.readline()
                return input
        return False
    def setupChat(self, dest, dest_port):
        self.kill()
        self.active = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.host, self.port))
        self.s.setblocking(False)

        #x = 1
        while 1:

            try:
                out = self.s.recvfrom(1024)
                data = out[0]
                addr = out[1]
                if data:
                    #answer = "message received..."
                    #self.s.sendto(answer, (dest, dest_port))
                    print "[" + dest + ":" + str(dest_port) + "] :: " + data
            except:
                pass
            
            message = self.getLine()
            if (message != False):
                self.s.sendto(message, (dest, dest_port))
       
    def setupServerConn(self):
        self.s.bind((self.host, self.port))
        msg = str(self.ID) + ':' + self.host + ':' + str(self.port)
        self.s.sendto(msg,(SERVER_IP, SERVER_PORT))
        
        out = self.s.recvfrom(1024)
        data = out[0]
        addr = out[1]

        print 'Your info: ' + data


    def requestBuddy(self, who):
       msg = str(self.ID) + ':' + str(who)

       self.s.sendto(msg, (SERVER_IP, SERVER_PORT))

       out = self.s.recvfrom(1024)

       data = out[0]
       addr = out[1]

       print 'requested information: ' + data
       result = data.split(':', 1)
       return result
    def kill(self):
        self.active = False
        self.s.close()

if __name__ == "__main__":
    main()