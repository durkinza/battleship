# BattleShip (for terminal linux)
# Author: Tanner Purves, Zane Durkin
import os
import sys
from prettytable import PrettyTable

# Ask user if they want to be client or server
table = PrettyTable(['WELCOME TO BATTLESHIP'])
table.add_row(['1) Play on network'])
table.add_row(['2) Vs computer'])
# table.align(0) = 'l'
print(table)
