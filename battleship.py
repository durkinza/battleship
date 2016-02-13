# BattleShip (for terminal linux)
# Author: Tanner Purves, Zane Durkin
import os
import sys
#import getopt
#from docopt import docopt
from prettytable import PrettyTable

# Ask user if they want to be client or server
welcome_table = PrettyTable(['WELCOME TO BATTLESHIP'])
welcome_table.add_row(['1) Play on network'])
welcome_table.add_row(['2) Vs. computer'])
welcome_table.add_row(['3) Settings'])
welcome_table.add_row(['4) Quit'])
welcome_table.align = 'l'
try:
    def menu(user_input):
        if user_input == 1:
            # print('Network')
            network_table = PrettyTable(['Network'])
            network_table.add_row(['1) Host a game'])
            network_table.add_row(['2) Join a game'])
            network_table.add_row(['3) Back'])
            network_table.align = 'l'
            os.system('clear')
            print(network_table)
            # ask for an option until a valid one is entered
            while True:
                try:
                    # check that the user enterd an integer
                    user_input = int(raw_input("Whatch you want? [1-3]: "))
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
                        elif user_input == 2:
                            print('Connecting to server')
                        elif user_input == 3:
                            print('going back')
                            main()
                        else:
                            print('How about no...')

        elif user_input == 2:
            print('Vs. Computer')
            print('How about no...')
        elif user_input == 3:
            print('Settings')
            print('How about no...')
        elif user_input == 4:
            print('You quitter...')
            exit()
        else:
            print('How about no...')

    def set_server():
        # function to setup server
        print('using port: ')

    def get_server():
        # function to connect to a server
        print('connecting to server...')

    def main():
        os.system('clear')
        print(welcome_table)
        # ask for an option until a valid one is entered
        while True:
            try:
                # check that the user enterd an integer
                user_input = int(raw_input("Whatch you want? [1-4]: "))
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
                    menu(user_input)
    if __name__ ==  "__main__":
        main()

except KeyboardInterrupt:
    print("\nUntil next time")
    exit()

