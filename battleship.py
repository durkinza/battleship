# BattleShip (for terminal linux)
# Author: Tanner Purves, Zane Durkin
import os
import sys
import socket
#import getopt
#from docopt import docopt
from prettytable import PrettyTable

# Build Welcome table
welcome_table = PrettyTable(['WELCOME TO BATTLESHIP'])
welcome_table.add_row(['1) Play on network'])
welcome_table.add_row(['2) Vs. computer'])
welcome_table.add_row(['3) Settings'])
welcome_table.add_row(['4) Quit'])
welcome_table.align = 'l'
try:
    def main_menu(user_input):
        if user_input == 1:
            # print('Network')
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
                    user_input = int(raw_input("Whatchu want? [1-3]: "))
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
  #                          os.system('clear')
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

    def set_server():
        # funtion to setup server
        while True:
            # see if user would like to specify a port
            user_input = raw_input("Use default port (2323)? [Y/n]: ")
            if user_input not in ('Y','y','yes','Yes','N','n','no','No',None):
                # if the user didn't use a valid anwser
                print('Please use y or n')
            else:
                if (user_input.lower()[0] == 'y') or (user_input == None):
                    # set default port to 2323 and exit
                    port = 2323
                    break
                else:
                    # get specified port
                    print('You\'re a picky one...')
                    while True:
                        try:
                            # get optional port input
                            user_input = int(raw_input("What port would you like to use? (must be >1024 without root permissions):"))
                        except ValueError:
                            # user must choose a number, show question again
                            print("Just a port number.\n")
                            continue
                        else:
                            port = user_input
                            # break out of second loop
                            break
                    # break out of first loop
                    break
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except KeyboardInterrupt:
            print('dang..')
        else:
            print('Using port: '+str(port))
            sock.bind(('',port))
            port_name = sock.getsockname()[1]
            print(port_name)
       #     s = socket.socket()
       # sock.bind(('', 0))
       # port = sock.getsockname()[1]

    def get_server():
        # function to connect to a server
        print('Connecting to server...')

    def main():
        # Ask user what they want
        os.system('clear')
        print(welcome_table)
        # ask for an option until a valid one is entered
        while True:
            try:
                # check that the user enterd an integer
                user_input = int(raw_input("Whatchu want? [1-4]: "))
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
    if __name__ ==  "__main__":
        main()

except KeyboardInterrupt:
    print("\nUntil next time")
    exit()

