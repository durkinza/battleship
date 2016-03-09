class Ship1(object):

    def __init__(self):
        self.length = 3
        self.location = [[0, 0], [1, 0], [2, 0]]
        self.health = 3
        self.face = 'horizontal'
        self.chars_hor = ['<', '#', '>']
        self.chars_ver = ['^', '#', '>']

    def chars(self):
        # return the array up characters being used
        if self.face == 'horizontal':
            return self.chars_hor
        else:
            return self.chars_ver

    def turn(self):
        # turn the ship, using middle block as axis
        if self.face == 'horizontal':
            # if the ship is currently horizontal, turn it vertical
            # use the location of the middle block to set the rest of the blocks
            # move the left block ontop of the middle block
            #   set to same column
            self.location[0][0] = self.location[1][0]
            #   set to one row above
            self.location[0][1] = (self.location[1][1] - 1)
            # move the right block under the middle block
            #   set to same column
            self.location[2][0] = self.location[1][0]
            #   set to one row below
            self.location[2][1] = (self.location[1][1] + 1)
            # say that the ship is now vertical
            self.face = 'vertical'
        else:
            # if the ship is currently vertical, turn it horizontal
            # move the top block to the left of the middle block
            #   set to one column to the left
            self.location[0][0] = (self.location[1][0] - 1)
            #   set to same row
            self.location[0][1] = self.location[1][1]
            # move bottom block to the right
            #   set to one column to the right
            self.location[2][0] = (self.location[1][0] + 1)
            #   set to same row
            self.location[2][1] = self.location[1][1]
            # say that the ship is now horizontal
            self.face = 'horizontal'

    def down(self):
        # move the ship up a row(s)
        # move each block up on row from current row
        self.location[0][1] = (self.location[0][1] + 1)
        self.location[1][1] = (self.location[1][1] + 1)
        self.location[2][1] = (self.location[2][1] + 1)

    def up(self):
        # move the ship down a row(s)
        # move each block down a row from current row
        self.location[0][1] = (self.location[0][1] - 1)
        self.location[1][1] = (self.location[1][1] - 1)
        self.location[2][1] = (self.location[2][1] - 1)

    def left(self):
        # move the ship left one column
        self.location[0][0] = (self.location[0][0] - 1)
        self.location[1][0] = (self.location[1][0] - 1)
        self.location[2][0] = (self.location[2][0] - 1)

    def right(self):
        # move the ship right one column
        self.location[0][0] = (self.location[0][0] + 1)
        self.location[1][0] = (self.location[1][0] + 1)
        self.location[2][0] = (self.location[2][0] + 1)
