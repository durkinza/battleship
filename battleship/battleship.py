# BattleShip (for terminal linux)
# Author: Tanner Purves, Zane Durkin
import os
import re
import time
import socket
import threading
# maybe use clint instead of configobh, also adds text color
from configobj import ConfigObj
from prettytable import PrettyTable

# function for clearing screen (for both windows and linux)
def clear():
    if (os.name == 'nt'):
        c = os.system('cls')
    else:
        c = os.system('clear')
    del c  # can also omit c totally

# function for connecting to a server
def get_server():
    # function to connect to a server
    while True:
        user_input = input("What IP are you connecting to?: ")
        try:
            # see if user entered a valid ip number
            socket.inet_aton(user_input)
        except socket.error:
            # the ip is not valid, let user know and ask again
            print('Thats not a valid IP')
            continue
        else:
            Ip = user_input
            while True:
                user_input = input("Are we using the default port today?("+Port+") [Y/n]")
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
        # connect to server
        sock.connect((Ip, port))
        # tell server that the user wants to join
        data = "Joining "+Username+" "+Ip
        # send request to server
        sock.send(data.encode())
        # listen for a response
        data = sock.recv(int(Buffer))
        # let user know if they can join
        if re.match('^([Jj]oined)', data.decode()):
            # if the server returns joined then continue
            # split the data up to get the server's username
            info = (data.decode()).split(' ')
            print('Joined '+info[1]+'\'s game')
            connect = True
        else:
            # if the server denied the connection
            print('Could not connect to game')
            connect = False
        if connect:
            # after joining game, wait for game to start
            print('Waiting for the game to start...')
            while True:
                # listen for new data from the server
                data = sock.recv(int(Buffer))
                # the server says the game is starting
                if re.match('^[Ss]tart', data.decode()):
                    print('\n\nGame is Starting!\n\n')
                    # start the game on client side
                    start = True
                    break
                elif re.match('^[Cc]ancle', data.decode()):
                    # if the server canceled the game close the connection
                    print('Game is canceled...')
                    start = False
                    sock.close()
                    break
                else:
                    # display any other info from the server, like any other new players
                    print(data.decode())
            # if the server said to start
            if start:
                # push connectino to the background
                Serv = threading.Thread(target=client)
                Serv.daemon = True
                Serv.start()
                # start game in client mode
                game('client')


# function to draw the main menu
def main_menu(user_input):
    if user_input == 1:
        # create networking menu
        network_table = PrettyTable(['BATTLESHIP Networking'])
        network_table.add_row(['1) Host a game'])
        network_table.add_row(['2) Join a game'])
        network_table.add_row(['3) Back'])
        network_table.align = 'l'
        # clear the screen
        clear()
        # os.system('clear')
        # ask for an option until a valid one is entered
        while True:
            # print the menu
            print(network_table)
            # wait for a valid option to be chosen
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
    try:
        # create a global connection
        global sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        # if socket could not be used
        print('dang... '+socket.error())
    else:
        # if the the socket can be used, bind to it
        print('Using port: '+str(port))
        sock.bind((Ip, port))
        # listen to the socket
        sock.listen(1)
        # create a global array of all that are connected
        global connected
        connected = []
        # print address for others to connect to
        print('\nConnection address: '+str(Ip)+':'+str(port)+' \n')
        # start server in new thread
        Serv = threading.Thread(target=server)
        Serv.daemon = True
        Serv.start()
        # don't start the game until at least one user is connected
        while True:
            # os.system('clear')
            clear()
            print('\nConnection address:' + str(Ip) + ':' + str(port) + ' \n' + 'Listening for connections...\n')
            if len(connected) > 0:
                print(str(connected[0][0])+' Connected')
                break
            time.sleep(1)
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
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


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


def main():
    # Build Welcome table
    welcome_table = PrettyTable(['WELCOME TO BATTLESHIP'])
    welcome_table.add_row(['1) Play on network'])
    welcome_table.add_row(['2) Vs. computer'])
    welcome_table.add_row(['3) Settings'])
    welcome_table.add_row(['4) Quit'])
    welcome_table.align = 'l'
    # get configuation file
    import pdb
    pdb.set_trace()
    global config, Port, Ip, Buffer, Username
    config = ConfigObj('battleship.conf')
    Ip_conf = config['TCP_IP']
    Ip = get_ip()
    if Ip == '127.0.0.1':
        Ip = Ip_conf
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
    clear()
    # os.system('clear')
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
