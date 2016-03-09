# BattleShip (for terminal linux)
# Author: Tanner Purves, Zane Durkin
import os
import re
import sys
import time
import socket
import threading
import ships
# maybe use clint instead of configobh, also adds text color
from configobj import ConfigObj
from prettytable import PrettyTable

# settup getch() for both unix and windows
try:
    import tty, termios
except ImportError:
    # Probably Windows.
    try:
        import msvcrt
    except ImportError:
        # Just give up here.
        raise ImportError('getch not available')
    else:
        getch = msvcrt.getch
else:
    def getch():
        """getch() -> key character
         Read a single keypress from stdin and return the resulting character.
        Nothing is echoed to the console. This call will block if a keypress
        is not already available, but will not wait for Enter to be pressed.
         If the pressed key was a modifier key, nothing will be detected; if
        it were a special function key, it may return the first character of
        of an escape sequence, leaving additional characters in the buffer.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# function for clearing a ship's current spot on the board
def clear_ship(shp):
    for i in shp.location:
        board[i[0]][i[1]] = ''


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
                else:    # Canceling game
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
        IP = s.getsockname()[0]
    except:
        IP = Ip
    finally:
        s.close()
    return IP


# function to draw gameboard(s)
def game(typ):
    global board
    global ship1
    # create empty array for the board
    board = []
    # create all ship objects
    ship1 = ships.Ship1()
    # fill board array with empty strings
    for x in range(0, 10):
        board.append(['', '', '', '', '', '', '', '', '', ''])

    if typ == 'client':
        place_board()
    elif typ == 'server':
        place_board()

# draw game board with the ablitiy to move peices around
def draw_board():
#    clear()
    set_board = PrettyTable()
    set_board.horizontal_char ='~'
    set_board.vertical_char = '|'
    set_board.add_column("#",['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    set_board.add_column('A', board[0])
    set_board.add_column('B', board[1])
    set_board.add_column('C', board[2])
    set_board.add_column('D', board[3])
    set_board.add_column('E', board[4])
    set_board.add_column('F', board[5])
    set_board.add_column('G', board[6])
    set_board.add_column('H', board[7])
    set_board.add_column('I', board[8])
    set_board.add_column('J', board[9])
    print(set_board)


def place_board():
    board[ship1.location[0][0]][ship1.location[0][1]] = ship1.chars()[0]
    board[ship1.location[1][0]][ship1.location[1][1]] = ship1.chars()[1]
    board[ship1.location[2][0]][ship1.location[2][1]] = ship1.chars()[2]
    draw_board()
    print("Place Your Ship!")
    while True:
        char = getch()
        if char == 'q':
            print('quitting')
            break
        elif char =='qqq':
            print('qutting')
            break
        elif char =='\x1b':
            char2 = getch()
            if char2 != '[':
                break
            char3 = getch()
            if char3 == 'A':
                print('Up')
                clear_ship(ship1)
                ship1.up()
            elif char3 == 'B':
                print('Down')
                clear_ship(ship1)
                ship1.down()
            elif char3 == 'C':
                print('Right')
                clear_ship(ship1)
                ship1.right()
            elif char3 == 'D':
                print('Left')
                clear_ship(ship1)
                ship1.left()
            else:
                print('We don\'t accept those keys here')
        elif char == 'r':
            print('rotate')
            clear_ship(ship1)
            ship1.turn()
        else:
            print(char)

        if char != '':
            board[ship1.location[0][0]][ship1.location[0][1]] = ship1.chars()[0]
            board[ship1.location[1][0]][ship1.location[1][1]] = ship1.chars()[1]
            board[ship1.location[2][0]][ship1.location[2][1]] = ship1.chars()[2]
            clear()
            draw_board()
            print ("Place Your Ship!")

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
        board = ()
        main()

except KeyboardInterrupt:
    print("\nUntil next time")
    exit()
