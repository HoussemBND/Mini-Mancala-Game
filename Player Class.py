# P-2 MCS 275 Fri 3 Mar 2017 : player.py
"""
This script models the 2-player board game mancala.
"""

from random import randint
from board import Board

class Player(object):
    """
    A player makes successive moves in the game.
    """

    def __init__(self, brd, nbr, lvl):
        """
        A player gets access to the board
        and is identified with a number nbr,
        which is either zero or one,
        corresponding to the row on the board.
        """
        self.brd = brd # the game board
        self.idn = nbr # the row on the board identifies the player
        self.ply = lvl # level of difficulty

    def __str__(self):
        """
        Returns the string representation of the player.
        """
        result = 'Player ' + str(self.idn) \
               + ' plays at level ' + str(self.ply) \
               + ' at board:\n' + str(self.brd)
        return result

    def __repr__(self):
        """
        Returns the string representation.
        """
        return str(self)

    def prompt4hole(self):
        """
        Prints the board and prompts the player for the index
        of a hole.  If the move is valid, then returns the index.
        Otherwise the player is asked to retry.
        """
        while True:
            print(self.brd)
            try:
                hole = int(input('enter 1, 2, 3, 4, 5, 6 : '))
                if self.brd.valid(self.idn, hole):
                    return hole
                else:
                    print(hole, 'is an invalid choice, please retry.')
            except ValueError:
                print('Invalid input, please retry.')

    def randomhole(self, verbose=True):
        """
        Generates a random index of a hole, retries if not valid,
        and if verbose, prints the board and the index of the hole
        before returning the index.
        """
        while True:
            hole = randint(1, 6)
            if self.brd.valid(self.idn, hole):
                if verbose:
                    # print(self.brd)
                    print('Player', self.idn, 'chooses hole '+str(hole)+'.')
                return hole

    def play(self, verbose=True, seeExtra=True):
        """
        Selects a hole and goes through the moves.
        If verbose, then extra information about the moves is shown.
        if seeExtra, then we see the intermediate boards at the extra
        turns of the computer player.
        """
        while not self.brd.emptyside():
            if(self.ply == 0):
                hole = self.randomhole()
            elif(self.ply > 0):
                (hole, val) = self.bestmove(0, self.ply, verbose)
                if verbose:
                    print('-> the best move is hole', hole)
            else:
                hole = self.prompt4hole()
            stones = self.brd.pick(self.idn, hole-1)
            if verbose:
                print('Player', self.idn, 'picks up', stones, 'stone(s).')
            (row, idx) = self.brd.drop(self.idn, hole-1, stones, self.idn)
            #if verbose:
            #    print('Board after dropping stones :\n' + str(self.brd))
            if idx in range(6):
                self.brd.copy(row, idx, self.idn)
                if verbose:
                    if(self.idn == row) and (self.brd.holes[row][idx] == 1):
                        print('Player', self.idn, 'got stones from opponent.')
                        # print('Board after moving stones :\n' + str(self.brd))
                break
            else:
                if verbose:
                    print('Player', self.idn, 'gets an extra turn.')
                if self.ply != -1 or verbose:
                    if seeExtra:
                        print(self.brd)

    def bestmove(self, level, maxlvl, verbose=True):
        """
        Evaluates the six possible moves and returns the best choice
        as the first element in the tuple.  The second element in the
        tuple on return is the value of the best choice.
        """
        bestval = None
        for hole in range(1, 7):
            if self.brd.valid(self.idn, hole):
                backup = self.brd.deepcopy()
                if verbose:
                    print('evaluating choice', hole)
                stones = self.brd.pick(self.idn, hole-1)
                (row, idx) = self.brd.drop(self.idn, hole-1, stones, self.idn)
                if idx in range(6):
                    self.brd.copy(row, idx, self.idn)
                    oppidn = (self.idn + 1) % 2
                    val = self.brd.stores[self.idn] - self.brd.stores[oppidn]
                    if level < maxlvl and not self.brd.emptyside():
                        backupidn = self.idn # backup the idn of the player
                        self.idn = (self.idn + 1) % 2 # become the opponent
                        (validx, val) = self.bestmove(level+1,maxlvl,verbose)
                        val = -val # the value of the opponent is negative
                        self.idn = backupidn # restore the idn of the player
                else: # check if an extra turn is possible
                    if level < maxlvl and not self.brd.emptyside():
                        (validx, val) = self.bestmove(level+1,maxlvl,verbose)
                    else:
                        oppidn = (self.idn + 1) % 2
                        val = self.brd.stores[self.idn] \
                            - self.brd.stores[oppidn]
                        if level < maxlvl and not self.brd.emptyside():
                            backupidn = self.idn # backup the idn of the player
                            self.idn = (self.idn + 1) % 2 # become the opponent
                            (validx, val) \
                                 = self.bestmove(level+1,maxlvl,verbose)
                            val = -val # the value of the opponent is negative
                            self.idn = backupidn # restore the player's idn
                if bestval == None:
                    (besthole, bestval) = (hole, val)
                else:
                    if val > bestval:
                        (besthole, bestval) = (hole, val)
                if verbose:
                    print('value at hole', hole, 'is', val)
                    print('best value :', bestval, 'at hole', besthole)
                self.brd.holes = backup.holes   # restore the previous board
                self.brd.stores = backup.stores # but leave the outer brd
        return (besthole, bestval)

def final(brd):
    """
    Determines the winner of the game.
    """
    if brd.emptyside():
        brd.finish()
        print('The final board :\n' + str(brd))
        if brd.stores[0] > brd.stores[1]:
            print('Player 0 wins.')
        elif brd.stores[0] < brd.stores[1]:
            print('Player 1 wins.')
        else:
            print('The game ended in a draw.')

def randomplay(level, verbose=True):
    """
    Both players make random moves.
    A coin flip decides who begins.
    """
    brd = Board()
    print(brd)
    zero = Player(brd, 0, level)
    one = Player(brd, 1, level)
    cnt = randint(0, 1)
    while not brd.emptyside():
        if cnt == 0:
            zero.play(verbose)
            print(brd)
            if brd.emptyside():
                break
            one.play(verbose)
        else:
            one.play(verbose)
            print(brd)
            if brd.emptyside():
                break
            zero.play(verbose)
        print(brd)
        ans = input('Continue to the next round ? (y/n) ')
        if ans != 'y':
            break
    final(brd)

def interactiveplay(level, verbose=True):
    """
    The user plays agains player zero.
    A coin flip decides who begins.
    """
    brd = Board()
    zero = Player(brd, 0, level)
    one = Player(brd, 1, -1)
    cnt = randint(0, 1)
    if cnt == 0:
        print(brd)
    while not brd.emptyside():
        if cnt == 0:
            zero.play(verbose)
            if brd.emptyside():
                break
            one.play(verbose)
            print(brd)
        else:
            one.play(verbose)
            if brd.emptyside():
                break
            print(brd)
            zero.play(verbose)
        # print(brd)
        # ans = input('Continue to the next round ? (y/n) ')
        # if ans != 'y':
        #     break
    final(brd)

def main():
    """
    Runs through the mancala game.
    """
    print('Welcome to our mancala game!')
    ans = input('Run with two computer players ? (y/n) ')
    lvl = int(input('Give the level of difficulty (>= 0) : '))
    vrb = input('Verbose mode ? (y/n) ')
    verbose = (vrb == 'y')
    if ans == 'y':
        randomplay(lvl, verbose)
    else:
        interactiveplay(lvl, verbose)

if __name__ == "__main__":
    main()
