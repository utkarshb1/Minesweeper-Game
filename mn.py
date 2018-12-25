#CODE:

import random                               #Importing libraries
import re
import time
from string import ascii_lowercase



class Minesweeper:                          #Creating Class named Minesweeper
    
    def play(self,t_gridsize,t_numberof_mines):
        gridsize = t_gridsize
        numberofmines = t_numberof_mines

        currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]

        grid = []
        flags = []
        starttime = 0

        helpmessage = ("Type the column followed by the row (eg. a5). "
                       "To put or remove a flag, add 'f' to the cell (eg. a5f).")

        self.game_play_area(currgrid)
        print(helpmessage + " Type 'help' to show this message again.\n")

        while True:
            minesleft = numberofmines - len(flags)
            prompt = input('Enter the cell ({} mines left): '.format(minesleft))
            result = self.parseinput(prompt, gridsize, helpmessage + '\n')

            message = result['message']
            cell = result['cell']

            if cell:
                print('\n\n')
                rowno, colno = cell
                currcell = currgrid[rowno][colno]
                flag = result['flag']

                if not grid:
                    grid, mines = self.setup_the_grid(gridsize, cell, numberofmines)
                if not starttime:
                    starttime = time.time()

                if flag:
                    # Add a flag if the cell is empty
                    if currcell == ' ':
                        currgrid[rowno][colno] = 'F'
                        flags.append(cell)
                    # Remove the flag if there is one
                    elif currcell == 'F':
                        currgrid[rowno][colno] = ' '
                        flags.remove(cell)
                    else:
                        message = 'Cannot put flag there invalid position'

                # If there is a flag there, show a message
                elif cell in flags:
                    message = 'Flag is already present'

                elif grid[rowno][colno] == 'X':
                    print('Game Over\nYou have lost the game!\n')
                    self.game_play_area(grid)
                    if self.play_again():
                        self.play_game()
                    return

                elif currcell == ' ':
                    self.display_cells(grid, currgrid, rowno, colno)

                else:
                    message = "That cell is already shown"

                if set(flags) == set(mines):
                    minutes, seconds = divmod(int(time.time() - starttime), 60)
                    print(
                        'You Win. '
                        'It took you {} minutes and {} seconds.\n'.format(minutes, seconds))
                    self.game_play_area(grid)
                    if self.play_again():
                        self.play_game()
                    return

            self.game_play_area(currgrid)
            print(message)


    
    def setup_the_grid(self,gridsize, start, numberofmines):
        emptygrid = [['0' for i in range(gridsize)] for i in range(gridsize)]

        mines = self.get_the_mines(emptygrid, start, numberofmines)

        for i, j in mines:
            emptygrid[i][j] = 'X'

        grid = self.get_the_number(emptygrid)

        return (grid, mines)


    def game_play_area(self, grid):
        gridsize = len(grid)

        horizontal = '   ' + (4 * gridsize * '-') + '-'

        # Print top column letters
        toplabel = '     '

        for i in ascii_lowercase[:gridsize]:
            toplabel = toplabel + i + '   '

        print(toplabel + '\n' + horizontal)

        # Print left row numbers
        for idx, i in enumerate(grid):
            row = '{0:2} |'.format(idx + 1)

            for j in i:
                row = row + ' ' + j + ' |'

            print(row + '\n' + horizontal)

        print('')


    def get_the_random_cell(self,grid):
        gridsize = len(grid)

        a = random.randint(0, gridsize - 1)
        b = random.randint(0, gridsize - 1)

        return (a, b)


    def get_the_neighbours(self,grid, rowno, colno):
        gridsize = len(grid)
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                    neighbors.append((rowno + i, colno + j))

        return neighbors


    def get_the_mines(self,grid, start, numberofmines):
        mines = []
        neighbors = self.get_the_neighbours(grid, *start)

        for i in range(numberofmines):
            cell = self.get_the_random_cell(grid)
            while cell == start or cell in mines or cell in neighbors:
                cell = self.get_the_random_cell(grid)
            mines.append(cell)

        return mines


    def get_the_number(self,grid):
        for rowno, row in enumerate(grid):
            for colno, cell in enumerate(row):
                if cell != 'X':
                    # Gets the values of the neighbors
                    values = [grid[r][c] for r, c in self.get_the_neighbours(grid,rowno, colno)]
                    # Counts how many are mines
                    grid[rowno][colno] = str(values.count('X'))

        return grid


    def display_cells(self,grid, currgrid, rowno, colno):
        # Exit function if the cell was already shown
        if currgrid[rowno][colno] != ' ':
            return

        # Show current cell
        currgrid[rowno][colno] = grid[rowno][colno]

        # Get the neighbors if the cell is empty
        if grid[rowno][colno] == '0':
            for r, c in self.get_the_neighbours(grid, rowno, colno):
                # Repeat function for each neighbor that doesn't have a flag
                if currgrid[r][c] != 'F':
                    self.display_cells(grid, currgrid, r, c)


    def play_again(self):
        choice = input('Do you want to Play again? (y/n): ')

        return choice.lower() == 'y'


    def parseinput(self,inputstring, gridsize, helpmessage):
        cell = ()
        flag = False
        message = "Invalid cell. " + helpmessage

        pattern = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[gridsize - 1])
        validinput = re.match(pattern, inputstring)

        if inputstring == 'help':
            message = helpmessage

        elif validinput:
            rowno = int(validinput.group(2)) - 1
            colno = ascii_lowercase.index(validinput.group(1))
            flag = bool(validinput.group(3))

            if -1 < rowno < gridsize:
                cell = (rowno, colno)
                message = ''

        return {'cell': cell, 'flag': flag, 'message': message}

    def play_game(self):
        while True:
            level = int(input("Choose Level \n1.Easy\n2.Medium\n3.Hard\n=> "))
            if level == 1:
                game.play(9,12)
                break
            elif level == 2:
                game.play(12,17)
                break
            elif level == 3:
                game.play(15,30)
                break
            else:
                continue
game = Minesweeper()
game.play_game();

     
