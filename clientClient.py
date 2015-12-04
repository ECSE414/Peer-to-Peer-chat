import socket   #socket for Peer-to-Peer and Client-Server comms.
import time
import sys      #sys calls
import select   #import to poll keyboard for press
import datetime
from urllib2 import urlopen #used to get your IP
import re

SERVER_IP = '159.203.31.96'  #server IP
SERVER_PORT = 6000          #server port

check = 0                   #valid ID check
printed = False             #something to print check

client = None               #globally accessible client
NO_NAME = '%-1,'            #resevered character sequences
RESV1 = '-1'                #Exit
RESV2 = '-2'
RESV3 = '-3'
RESV4 = '-4'
RESV5 = 't4cT'
def main():
    global client
    global printed
    my_ip = urlopen('http://ip.42.pl/raw').read()   #Get IP
    client = Client()                               #created client
    while check == 0:                               #while ID is not entered
        ret = enter_ID(my_ip)                       #get users ID
        if ret == False:                            #if invalid ID, try again
            continue
    while 1:
        try:
            if not printed:                         #print menu if valid
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

#!
# Function used to get user ID from client and update corresponding server information
#
def enter_ID(my_ip):
    global client
    try:
        #get users ID
        num = raw_input('Please enter your id: ')
        if num == RESV1 or num == RESV2 or num == RESV3 or num == RESV4 or num == NO_NAME:
            print "Invalid ID, try again"
            return False
        #update client ID
        client.ID = num
        #update IP and port number
        client.host = my_ip
        client.port = 8000
        #bind the socket to this port and IP
        client.s.bind((client.host, client.port))
        #setup and send information to server
        client.setupServerConn()

    except KeyboardInterrupt:
        pass
#!
#Function to recv a request that interrupts the menu
#
def to_recv():
    global client
    global printed
    try:
        #make sure that waiting to receive data is not blocking
        client.s.setblocking(False)
        #bytes to recv
        out = client.s.recvfrom(1024)
        #retreive data and senders information
        data = out[0]
        addr = out[1]
        if data ==  RESV5:
            data = client.s.recvfrom(1024)
        #if data recveived is valid then ask if user wants to accept connection
        if data:
            answer = raw_input("Request from " + str(data)+ " do you want to accept? (y/n)")
            conn = client.requestBuddy(data)
            if answer == "y":
                print "chat started"
                #Send accept message to user who sent request
                client.s.sendto(RESV5, (conn[5], int(conn[1])))
                client.s.sendto("Chat request accepted", (conn[0], int(conn[1])))
                #setup the chat
                client.setupChat(conn[0], int(conn[1]))
                printed = False
            else:
                #if user does not wish to accept. connection is denied.
                client.s.sendto(RESV5, (conn[5], int(conn[1])))
                client.s.sendto("connection denied: returning to main menu", (conn[0], int(conn[1])))
                #add user back to avail list on server.
                client.s.sendto(str(client.ID) + ':' + RESV2, (SERVER_IP, SERVER_PORT))
                printed = False
    except:
        client.s.setblocking(True)
        pass

def command_ready():
    global client
    global printed
    #grab line when avail
    command = client.getLine()
    #make sure line read is valid
    if (command != False):
        #if user requests help, display menu  options
        if command == "/help\n":
            print "| req\t::\t'Request a Buddy'\t|\n| avail\t::\t'See available users'\t|\n| all\t::\t'See all users'\t\t|\n| exit\t::\t'Exit the application'\t|"
            printed = False
        #if user wants to request a buddy
        elif command == "req\n":
            #request list of available users
            client.s.sendto(str(client.ID) + ":" + RESV3, (SERVER_IP, SERVER_PORT))
            client.s.setblocking(True)
            #wait to recv data from server
            out = client.s.recvfrom(1024)
            data = out[0]
            addr = out[1]
            #print list of available users
            print data
            listed = re.split('\[|\'|,|\]|\n', data)
            print(listed)
            #ask user who they want to request
            print 'Who would you like to contact?'
            to = False
            #keep trying to recv answer
            while not to:
                to = client.getLine()
            check = to.split('\n')
            #make sure that user did not request theirself
            avail = False
            for i in listed:
                if i == check[0]:
                    avail = True
                    break
            if check[0] == client.ID:
                printed = False
                return False
            if avail == False:
                printed = False
                return False
            #request information of user
            conn = client.requestBuddy(to)
            #if request is not valid, return back to menu
            if conn == NO_NAME:
                printed = False
                return False
            #send my ID to client who I wish to contact
            client.s.sendto(RESV5, (conn[5], int(conn[1])))
            client.s.sendto(client.ID, (conn[0], int(conn[1])))
            client.s.setblocking(True)
            #block and wait for recv
            data[0] = client.s.recvfrom(1024)
            if data[0] ==  RESV5:
                data = client.s.recvfrom(1024)

            print(data[0])
            #if connection was not accepted add back to avail list and return to menu
            if data[0] == "connection denied: returning to main menu":
                dest = None
                client.s.sendto(str(client.ID) + ':' +  RESV2, (SERVER_IP, SERVER_PORT))
                printed = False
                return False
            #setup the chat
            client.setupChat(conn[0], int(conn[1]))
            printed = False
        elif command == "avail\n":
            client.s.sendto(str(client.ID) + ':' + RESV3, (SERVER_IP, SERVER_PORT))
            loop = 1
            while loop == 1:
                out = client.s.recvfrom(1024)
                data = out[0]
                addr = out[1]
                print data
                loop = 0
            printed = False
        elif command == "all\n":
            client.s.sendto(str(client.ID) + ':' + RESV4, (SERVER_IP, SERVER_PORT))
            loop = 1
            while loop == 1:
                out = client.s.recvfrom(1024)
                data = out[0]
                addr = out[1]
                print data
                loop = 0
            printed = False
        elif command == "exit\n":
            client.s.sendto(str(client.ID) + ':' + RESV1, (SERVER_IP,SERVER_PORT))
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
        self.s.setblocking(False)
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
                            self.s.sendto(str(self.ID) + ':' + RESV2, (SERVER_IP, SERVER_PORT))
                            return
                except:
                    pass

                message = self.getLine()
                if (message != False):
                    self.s.sendto(message, (dest, dest_port))
            except KeyboardInterrupt:
                if dest != None:
                    self.s.sendto("Buddy disconnected: returning to main menu", (dest, dest_port))
                self.s.sendto(str(self.ID) + ':' + RESV2, (SERVER_IP, SERVER_PORT))
                print()
                return

    def setupServerConn(self):
        global check

        msg = str(self.ID) + ':' + self.host + ':' + str(self.port)
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


       if data == NO_NAME:
           return data

       print 'requested information: ' + data
       result = data.split(':', 1)
       #print result
       return result
    def kill(self):
        self.active = False
        self.s.close()

if __name__ == "__main__":
    main()
