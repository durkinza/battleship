# BattleShip (for terminal linux)
# Author: Tanner Purves, Zane Durkin
import os
import sys
import re
import time
import socket
import threading
# import asyncore
# import getopt
# from docopt import docopt
from configobj import ConfigObj
from prettytable import PrettyTable


# function for connecting to a server
def get_server():
    # function to connect to a server
    while True:
        user_input = input("What IP are you connecting to?: ")
        try:
            socket.inet_aton(user_input)
        except socket.error:
            print('Thats not a valid IP')
            continue
        else:
            Ip = user_input
            while True:
                user_input = input("Are we using the default port?("+Port+") [Y/n]")
                if user_input not in ('Y', 'y', 'yes', 'Yes', 'N', 'n', 'no', 'No', None):
                    # if the user didn't use a valid anwser
                    print('Please use y or n')
                else:
                    if (user_input.lower()[0] == 'y') or (user_input is None):
                        # set default port to 2323 and exit
                        port = int(Port)
                        break
                    else:
                        # get specified port
                        print('You\'re a picky one...')
                        while True:
                            try:
                                # get optional port input
                                user_input = int(input("What port would you like to use? (must be >1024 without root permissions): "))
                            except ValueError:
                                # user must choose a number, show question again
                                print("Just a port number.\n")
                                continue
                            else:
                                port = int(user_input)
                                # break out of third loop
                                break
                        # break out of second loop
                        break
            # break out of first loop
            break
    try:
        global sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('dang... Couldn\'t connect ')
    else:
        print('Connecting to server at: '+str(Ip)+':'+str(port))
        sock.connect((Ip, port))
        # port_name = sock.getsockname()[1]
        data = "Joining "+Username+" "+Ip
        sock.send(data.encode())
        # conn, addr = sock.accept()
        # print('Connection address:'+addr)
        data = sock.recv(int(Buffer))
        if re.match('^([Jj]oined)', data.decode()):
            info = (data.decode()).split(' ')
            print('Joined '+info[1]+'\'s Game')
        print('Waiting for the game to start')
        while True:
            data = sock.recv(int(Buffer))
            if re.match('^[Ss]tart', data.decode()):
                print('Game is Starting!')
                start = True
                break
            elif re.match('^[Cc]ancle', data.decode()):
                print('Game is canceled...')
                start = False
                sock.close()
                break
            else:
                print(data.decode())
        if start:
            Serv = threading.Thread(target=client)
            Serv.daemon = True
            Serv.start()
            game('client')


# function to draw the main menu
def main_menu(user_input):
    if user_input == 1:
        network_table = PrettyTable(['BATTLESHIP Networking'])
        network_table.add_row(['1) Host a game'])
        network_table.add_row(['2) Join a game'])
        network_table.add_row(['3) Back'])
        network_table.align = 'l'
        os.system('clear')
        # ask for an option until a valid one is entered
        while True:
            print(network_table)
            try:
                # check that the user enterd an integer
                user_input = int(input("Whatchu want? [1-3]: "))
            except ValueError:
                # user must choose a number, show question again
                print("Yo, just pick a number.\n")
                continue
            else:
                # user entered a number, now make sure it is a valid one
                if int(user_input) not in (1, 2, 3):
                    # the user didn't enter a valid number
                    print("How about a valid number.\n")
                else:
                    # the number is valid, continue
                    if user_input == 1:
                        print('Setting up server')
                        set_server()
                        # os.system('clear')
                    elif user_input == 2:
                        print('Connecting to server')
                        get_server()
                        # os.system('clear')
                    elif user_input == 3:
                        # if the user wants to go back to main menu
                        print('going back')
                        main()
                    else:
                        # if something gets past the validation
                        print('How about no...')

    elif user_input == 2:
        # if the user wants to vs a computer
        print('Vs. Computer')
        print('How about no...')
    elif user_input == 3:
        # if the user wants to edit settings
        print('Settings')
        print('How about no...')
    elif user_input == 4:
        # if the user wants to quit
        print('You quitter...')
        exit()
    else:
        # if something gets past the validation
        print('How about no...')


# function to create server and get connections
def set_server():
    # global Buffer
    # global Ip
    # global Port
    # funtion to setup server
    while True:
        # see if user would like to specify a port
        user_input = input("Use default port ("+Port+")? [Y/n]: ")
        if user_input not in ('Y', 'y', 'yes', 'Yes', 'N', 'n', 'no', 'No', None):
            # if the user didn't use a valid anwser
            print('Please use y or n')
        else:
            if (user_input.lower()[0] == 'y') or (user_input is None):
                # set default port to 2323 and exit
                port = int(Port)
                break
            else:
                # get specified port
                print('You\'re a picky one...')
                while True:
                    try:
                        # get optional port input
                        user_input = int(input("What port would you like to use? (must be >1024 without root permissions):"))
                    except ValueError:
                        # user must choose a number, show question again
                        print("Just a port number.\n")
                        continue
                    else:
                        port = int(user_input)
                        # break out of second loop
                        break
                # break out of first loop
                break
    # print('start server')
    # server = Start_Server('localhost', port)
    # print('start loop')
    # asyncore.loop()
    # print('server started')
    try:
        global sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('dang... '+socket.error())
    else:
        print('Using port: '+str(port))
        sock.bind((Ip, port))
        # port_name = sock.getsockname()[1]
        sock.listen(1)
        global connected
        connected = []
        print('\nConnection address: '+str(Ip)+':'+str(port)+' \n')
        # print('Listening for connection...')
        # print('Connection address:', addr)
        # start server in new thread
        Serv = threading.Thread(target=server)
        Serv.daemon = True
        Serv.start()
        # don't start the game until at least one user is connected
        while True:
            os.system('clear')
            print('\nConnection address:' + str(Ip) + ':' + str(port) + ' \n' + 'Listening for connections...\n')
            if len(connected) > 0:
                print(str(connected[0][0])+' Connected')
                break
            time.sleep(3)
        while True:
            # see if user would like to specify a port
            user_input = input("Ready to Start? [Y/n]: ")
            if user_input not in ('Y', 'y', 'yes', 'Yes', 'N', 'n', 'no', 'No', None):
                # if the user didn't use a valid anwser
                print('Please use y or n')
            else:
                if (user_input.lower()[0] == 'y') or (user_input is None):
                    # tell everyone the game is starting
                    conn.send(('starting').encode())
                    game('server')
                    break
                else:
                    # Canceling game
                    print('Canceling Game...')
                    conn.send(('Canceled').encode())
                    break
        # while True:
        #     data = conn.recv(Buffer)
        #     if not data:
        #         break
        #     print("received data: ", data.decode())
        #     conn.send(data)  # echo data back
        conn.close()


# function to run in background for server
def server():
    global connected, conn
    conn, addr = sock.accept()
    while True:
        data = conn.recv(int(Buffer))
        if re.match('^([Jj]oining)', data.decode()):
            info = (data.decode()).split(' ')
            connected.append([info[1], info[2]])
            conn.send(('Joined '+Username).encode())
    # should be used when connection is closed
    conn.close()


# funtion to run in background for lient
def client():
    while True:
        data = sock.recv(int(Buffer))
        if re.match('^[Mm]ove', data.decode()):
            info = (data.decode()).split(' ')
            print('move made by '+info[1])
    conn.close()

# function to get current user's ip on network (defaults to 127.0.0.1 if no network)
def get_ip():
    # function to get the user's ip on network
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# function to draw gameboard(s)
def game(typ):
    if typ == 'client':
        while True:
            user_input = input('end of the line')
            if user_input is not None:
                sock.close()
                break
    if typ == 'server':
        while True:
            user_input = input('end of the line')
            if user_input is not None:
                conn.close()
                break

# class for starting a server and handling connections
# class Start_Server(asyncore.dispatcher):
#
#    def __init__(self, host, port):
#        asyncore.dispatcher.__init__(self)
#        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.set_reuse_addr()
#        self.bind((host, port))
#        self.listen(5)
#
#    def handle_connect(self):
#        pass
#
#    def handle_close(self):
#        self.close()
#
#    def handle_read(self):
#        print(self.recv(8192))
#
#    # def writable(self):
#    #    return (len(self.buffer) > 0)
#
#    def handle_accept(self):
#        pair = self.accept()
#        if pair is not None:
#            sock, addr = pair
#            print('New Connectin from %s' % repr(addr))
#            handler = sock.recv(Buffer)
#            if  handler:
#                self.send('recieved')
#
#    def handle_write(self):
#        sent = self.send(self.buffer)
#        self.buffer = self.buffer[sent:]


def main():
    # Build Welcome table
    welcome_table = PrettyTable(['WELCOME TO BATTLESHIP'])
    welcome_table.add_row(['1) Play on network'])
    welcome_table.add_row(['2) Vs. computer'])
    welcome_table.add_row(['3) Settings'])
    welcome_table.add_row(['4) Quit'])
    welcome_table.align = 'l'
    # get configuation file
    global config, Port, Ip, Buffer, Username
    config = ConfigObj('battleship.conf')
    Ip = config['TCP_IP']
    if Ip is None:
        Ip = '127.0.0.1'
    Port = config['TCP_PORT']
    if Port is None:
        Port = 2323
    Buffer = int(config['BUFFER_SIZE'])
    if Buffer is None:
        Buffer = 1024
    Username = config['USERNAME']
    if Username is None:
        Username = "Anonymous"
    # Ask user what they want
    os.system('clear')
    print(welcome_table)
    # ask for an option until a valid one is entered
    while True:
        try:
            # check that the user enterd an integer
            user_input = int(input("Whatchu want? [1-4]: "))
        except ValueError:
            # user must choose a number, show question again
            print("Yo, just pick a number.\n")
            continue
        else:
            # user entered a number, now make sure it is a valid one
            if int(user_input) not in (1, 2, 3, 4):
                # the user didn't enter a valid number
                print("How about a valid number.\n")
            else:
                # the number is valid, continue
                main_menu(user_input)
try:
    if __name__ == "__main__":
        main()

except KeyboardInterrupt:
    print("\nUntil next time")
    exit()
