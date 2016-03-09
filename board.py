from prettytable import PrettyTable
import sys
import ships

board = []
ship1 = ships.Ship1()
for x in range(0, 10):
    board.append(['', '', '', '', '', '', '', '', '', ''])

def place_board():
#    clear()
    print("Place your ships!")
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


try:
    import tty, termios
except ImportError:
    # Probably Windows.
    try:
        import msvcrt
    except ImportError:
        # FIXME what to do on other platforms?
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

def clear_ship(shp):
    for i in shp.location:
        board[i[0]][i[1]]= ''
print ship1.chars
board[ship1.location[0][0]][ship1.location[0][1]] = ship1.chars()[0]
board[ship1.location[1][0]][ship1.location[1][1]] = ship1.chars()[1]
board[ship1.location[2][0]][ship1.location[2][1]] = ship1.chars()[2]
place_board()
print("Place Your Ship!")
while True:
    char = getch()
    if char == 'q':
        break
    elif char =='qqq':
        break
    elif char =='\x1b':
        char2 = getch()
        if char2 != '[':
            break
        char3 = getch()
        if char3 == 'A':
            print 'Up'
            clear_ship(ship1)
            ship1.up()
        elif char3 == 'B':
            print 'Down'
            clear_ship(ship1)
            ship1.down()
        elif char3 == 'C':
            print 'Right'
            clear_ship(ship1)
            ship1.right()
        elif char3 == 'D':
            print 'Left'
            clear_ship(ship1)
            ship1.left()
        else:
            print 'We don\'t accept those keys here'
    elif char == 'r':
        print('rotate')
        clear_ship(ship1)
        ship1.turn()

    if char != '':
        board[ship1.location[0][0]][ship1.location[0][1]] = ship1.chars()[0]
        board[ship1.location[1][0]][ship1.location[1][1]] = ship1.chars()[1]
        board[ship1.location[2][0]][ship1.location[2][1]] = ship1.chars()[2]
        # clear()
        place_board()
        print ("Place Your Ship!")

