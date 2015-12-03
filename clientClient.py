import socket   #socket for Peer-to-Peer and Client-Server comms.
import time
import sys      #sys calls
import select   #import to poll keyboard for press
import datetime
from urllib2 import urlopen

SERVER_IP = '159.203.31.96'  #server IP
SERVER_PORT = 6000          #server port
check = 0                   #valid ID check
printed = False             #something to print check

client = None
NO_NAME = '%-1,'            #resevered character sequences
RESV1 = '-1'
RESV2 = '-2'
RESV3 = '-3'
RESV4 = '-4'
def main():
    global client
    global printed
    #print socket.gethostbyname(socket.gethostname())
    my_ip = urlopen('http://ip.42.pl/raw').read()
    print my_ip
    client = Client()
    while check == 0:
        ret = enter_ID(my_ip)  #get users input
        if ret == False:
            continue
    while 1:
        try:
            if not printed:
                print "Please enter a command: (type /help for help)"
                printed = True
            ret = to_recv()       #check to see if data is to be received
            ret = command_ready() #check to see if command is ready to be accepted
            if ret == False:
                continue
        except KeyboardInterrupt:
            printed = False
            print()
            pass

def enter_ID(my_ip):
    global client
    try:
        num = raw_input('Please enter your id: ')
        if num == '-1' or num == '-2' or num == '-3' or num == '-4' or num == NO_NAME:
            print "Invalid ID, try again"
            return False
        client.ID = num
        print client.ID
        client.host = my_ip
        client.port = 8000
        client.s.bind((client.host, client.port))
        client.setupServerConn()

    except KeyboardInterrupt:
        pass

def to_recv():
    global client
    global printed
    try:
        client.s.setblocking(False)
        out = client.s.recvfrom(1024)
        data = out[0]
        addr = out[1]
        print data
        received = data.split(':')
        if data:
            answer = raw_input("Request from " + str(data)+ " do you want to accept? (y/n)")
            print answer
            conn = client.requestBuddy(data)
            if answer == "y":
                print "answer was good"
                print "chat started"
                client.s.sendto("Chat request accepted", (conn[0], int(conn[1])))
                client.setupChat(conn[0], int(conn[1]))
                printed = False
            else:
                client.s.sendto("connection denied: returning to main menu", (conn[0], int(conn[1])))
                client.s.sendto(str(client.ID) + ':-2', (SERVER_IP, SERVER_PORT))
                printed = False
    except:
        client.s.setblocking(True)
        pass

def command_ready():
    global client
    global printed
    command = client.getLine()
    if (command != False):
        if command == "/help\n":
            print "| req\t::\t'Request a Buddy'\t|\n| avail\t::\t'See available users'\t|\n| all\t::\t'See all users'\t\t|\n| exit\t::\t'Exit the application'\t|"
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
            check = to.split('\n')
            if check[0] == client.ID:
                printed = False
                return False
            conn = client.requestBuddy(to)
            if conn == NO_NAME:
                printed = False
                return False
            client.s.sendto(client.ID, (conn[0], int(conn[1])))
            client.s.setblocking(True)
            data = client.s.recvfrom(1024)
            print(data[0])
            if data[0] == "connection denied: returning to main menu":
                dest = None
                client.s.sendto(str(client.ID) + ':-2', (SERVER_IP, SERVER_PORT))
                printed = False
                return False
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
            client.kill()
            exit(0)
        else:
            print "Invalid command (type /help for help)"
            printed = False

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
        chat = True
        while 1:
            try:
                try:
                    out = self.s.recvfrom(1024)
                    data = out[0]
                    addr = out[1]
                    if data:
                        print "[" + dest + ":" + str(dest_port) + "] :: " + data
                        if data == "Buddy disconnected: returning to main menu":
                            dest = None
                            self.s.sendto(str(self.ID) + ':-2', (SERVER_IP, SERVER_PORT))
                            return
                except:
                    pass

                message = self.getLine()
                if (message != False):
                    self.s.sendto(message, (dest, dest_port))
            except KeyboardInterrupt:
                if dest != None:
                    self.s.sendto("Buddy disconnected: returning to main menu", (dest, dest_port))
                self.s.sendto(str(self.ID) + ':-2', (SERVER_IP, SERVER_PORT))
                print()
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

        if data == NO_NAME:
            check = 0
            print 'That ID is taken, try again'
            self.s.close()
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return None
        else:
            check = 1
            print 'Your info: ' + data

    def requestBuddy(self, who):
       self.s.setblocking(True)
       msg = str(self.ID) + ':' + str(who)
       self.s.sendto(msg, (SERVER_IP, SERVER_PORT))

       out = self.s.recvfrom(1024)

       data = out[0]
       addr = out[1]

       print 'requested information: ' + data
       if data == NO_NAME:
           return data
       result = data.split(':', 1)
       print result
       return result
    def kill(self):
        self.active = False
        self.s.close()

if __name__ == "__main__":
    main()
