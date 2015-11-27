import socket   #socket for Peer-to-Peer and Client-Server comms.
import time
import sys      #sys calls
import select   #import to poll keyboard for press
import datetime
from urllib2 import urlopen

SERVER_IP = '159.203.31.96'  #server IP
SERVER_PORT = 6000         #server port
check = 0
def main():
    print socket.gethostbyname(socket.gethostname())
    my_ip = urlopen('http://ip.42.pl/raw').read()
    print my_ip
    while check == 0:
        try:
            num = raw_input('Please enter your id: ')
            if num == '-1' or num == '-2' or num == '-3' or num == '-4':
                print "Invalid ID, try again"
                continue
            client = Client()
            client.ID = num
            print client.ID
            #sel_port = raw_input('Please enter a port number greater than 2000: ')
            client.host = my_ip
            client.port = 8000
            client.s.bind((client.host, client.port))
            client.setupServerConn()
        except KeyboardInterrupt:
            pass
    printed = False
    while 1:
        #try:
        if not printed:
            print "Please enter a command: (type /help for help)"
            printed = True
        try:
            out = self.s.recvfrom(1024)
            data = out[0]
            addr = out[1]
            received = data.split(':')
            if data:
                answer = raw_input("Request from " + str(data+ " do you want to accept? (y/n)"))
                conn = client.requestBuddy(data)
                if answer == "y":
                    client.setupChat(conn[0], int(conn[1]))
                else:
                    client.s.sendto("connection denied: ctrl+C to exit to menu")
        except:
            pass

        command = client.getLine()
        if (command != False):
            print command
            if command == "/help\n":
                print "| req\t::\t'Request a Buddy'\t|\n| avail\t::\t'See available users'\t|\n| all\t::\t'See all users'\t|\n| exit\t::\t'Exit the application'\t|"
                printed = False
            elif command == "req\n":
                client.s.sendto(str(client.ID) + ':-3', (SERVER_IP, SERVER_PORT))
                loop = 1
                while loop == 1:
                    out = client.s.recvfrom(1024)
                    data = out[0]
                    addr = out[1]
                    print data
                    loop = 0
                print 'Who would you like to contact?'
                to = False
                while not to:
                    to = client.getLine()
                conn = client.requestBuddy(to)
                client.setupChat(conn[0], int(conn[1]))
                printed = False
            elif command == "avail\n":
                client.s.sendto(str(client.ID) + ':-3', (SERVER_IP, SERVER_PORT))
                loop = 1
                while loop == 1:
                    out = client.s.recvfrom(1024)
                    data = out[0]
                    addr = out[1]
                    print data
                    loop = 0
                printed = False
            elif command == "all\n":
                client.s.sendto(str(client.ID) + ':-4', (SERVER_IP, SERVER_PORT))
                loop = 1
                while loop == 1:
                    out = client.s.recvfrom(1024)
                    data = out[0]
                    addr = out[1]
                    print data
                    loop = 0
                printed = False
            elif command == "exit\n":
                client.s.sendto(str(client.ID) + ":-1", (SERVER_IP,SERVER_PORT))
                printed = False
                client.s.kill()
                exit(0)
            else:
                print "Invalid command (type /help for help)"
                printed = False
            #except KeyboardInterrupt:
            #    pass

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
        #self.kill()
        self.active = True
        #self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.s.bind((self.host, self.port))
        self.s.setblocking(False)
        print dest
        print dest_port
        while 1:
            try:
                try:
                    out = self.s.recvfrom(1024)
                    data = out[0]
                    addr = out[1]
                    if data:
                        print "[" + dest + ":" + str(dest_port) + "] :: " + data
                        if data == "connection denied: ctrl+C to exit to menu":
                            dest = None
                except KeyboardInterrupt:
                    if dest != None:
                        self.s.sendto("Buddy disconnected", (dest, dest_port))
                    self.s.sendto(str(self.ID) + ':-2', (SERVER_IP, SERVER_PORT))
                    return

                message = self.getLine()
                if (message != False):
                    self.s.sendto(message, (dest, dest_port))
            except KeyboardInterrupt:
                if dest != None:
                    self.s.sendto("Buddy disconnected", (dest, dest_port))
                self.s.sendto(str(self.ID) + ':-2', (SERVER_IP, SERVER_PORT))
                return

    def setupServerConn(self):
        global check
        print self.host
        print self.port
        #self.s.bind((self.host, self.port))
        msg = str(self.ID) + ':' + self.host + ':' + str(self.port)
        print msg
        self.s.sendto(msg,(SERVER_IP, SERVER_PORT))

        out = self.s.recvfrom(1024)
        data = out[0]
        addr = out[1]

        if data == 'That ID is taken, please try again':
            check = 0
            print data
            return None
        else:
            check = 1
            print 'Your info: ' + data

    def requestBuddy(self, who):
       msg = str(self.ID) + ':' + str(who)

       self.s.sendto(msg, (SERVER_IP, SERVER_PORT))

       out = self.s.recvfrom(1024)

       data = out[0]
       addr = out[1]

       print 'requested information: ' + data
       result = data.split(':', 1)
       print result
       return result
    def kill(self):
        self.active = False
        self.s.close()

if __name__ == "__main__":
    main()
