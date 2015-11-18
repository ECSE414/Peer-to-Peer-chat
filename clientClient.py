import socket   #socket for Peer-to-Peer and Client-Server comms.
import time
import sys      #sys calls
import select   #import to poll keyboard for press
import datetime
from urllib2 import urlopen

SERVER_IP = '159.203.31.96'  #server IP
SERVER_PORT = 6000         #server port
check = False
def main():
    print socket.gethostbyname(socket.gethostname())
    my_ip = urlopen('http://ip.42.pl/raw').read()
    print my_ip
    try:
        while check == False:
            num = raw_input('Please enter your id: ')

            client = Client()
            client.ID = num
            print client.ID
            #sel_port = raw_input('Please enter a port number greater than 2000: ')
            client.host = socket.gethostbyname(socket.gethostname())
            client.port = 8000
            client.setupServerConn()
        while 1:
            command = raw_input("Please enter a command: (type /help for help)")
            if command == "/help":
                print "| req :: 'Request a Buddy' |\n| avail :: 'See available users' |\n| all :: 'See all users'|\n| exit :: 'Exit the application'|"
            elif command == "req":
                #TODO print list
                to = raw_input('Who would you like to contact?')
                conn = client.requestBuddy(to)
                client.setupChat(conn[0], int(conn[1]))
            elif command == "avail":
                pass
                #TODO print list
            elif command == "all":
                pass
                #TODO print list
            elif command == "exit":
                exit(0)
            else:
                print "Invalid command (type /help for help)"
    except KeyboardInterrupt:
        pass

class Client():
    def __init__(self):
        self.host = None
        self.port = None
        self.ID = None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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

        while 1:
            try:
                try:
                    out = self.s.recvfrom(1024)
                    data = out[0]
                    addr = out[1]
                    if data:
                        print "[" + dest + ":" + str(dest_port) + "] :: " + data
                except:
                    pass

                message = self.getLine()
                if (message != False):
                    self.s.sendto(message, (dest, dest_port))
            except KeyboardInterrupt:
                self.s.sendto("Buddy disconnected", (dest, dest_port))
                #self.s.sendto(str(self.ID) + ':-1', (SERVER_IP, SERVER_PORT))
                return

    def setupServerConn(self):
        global check
        print self.host
        print self.port
        self.s.bind((self.host, self.port))
        msg = str(self.ID) + ':' + self.host + ':' + str(self.port)
        print msg
        self.s.sendto(msg,(SERVER_IP, SERVER_PORT))

        out = self.s.recvfrom(1024)
        data = out[0]
        addr = out[1]

        if data == 'That numerical ID is taken, please try again':
            check = False
            print data
            return None
        check = True
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
