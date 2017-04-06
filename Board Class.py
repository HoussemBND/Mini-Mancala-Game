# P-2 MCS 275 Fri 3 Mar 2017 : board.py
"""
In the game of mancala stones are picked up and dropped
in successive holes, in counter clock wise fashion.
"""
class Board(object):
    """
    Models the board used for the mancala game.
    The board has two rows and two stores.  Each row has six holes.
    To each row corresponds a store.
    The holes are indexed from 0 to 5,
    while the corresponding moves are labeled from 1 to 6.
    """
    def __init__(self, **parameters):
        """
        Initializes the board and the stores.
        Without parameters, every hole in the board gets 4 stones
        and the stores of the player one and two are set to zero.
        The user can specify the number of stones in rowone
        and rowtwo by giving a list of numbers following the
        keywords rowone and rowtwo.  The values of the stores
        can be set with the keywords storeone and storetwo.   
        """
        self.holes = []
        if 'rowone' in parameters:
            self.holes.append(parameters['rowone'])
        else:
            self.holes.append([4 for _ in range(6)])
        if 'rowtwo' in parameters:
            self.holes.append(parameters['rowtwo'])
        else:
            self.holes.append([4 for _ in range(6)])
        self.stores = []
        if 'storeone' in parameters:
           self.stores.append(parameters['storeone'])
        else:
           self.stores.append(0)
        if 'storetwo' in parameters:
           self.stores.append(parameters['storetwo'])
        else:
           self.stores.append(0)

    def __str__(self):
        """
        Returns the string representation of the board.
        """
        result = '  %2d' % self.stores[0]
        for item in self.holes[0]:
            result = result + ' %2d' % item
        result = result + '\n    '
        for item in self.holes[1]:
            result = result + ' %2d' % item
        result = result + ' %2d' % self.stores[1]
        # result = result + '\n    '
        # for k in range(1, 7):
        #     result = result + ' %2d' % k
        return result

    def __repr__(self):
        """
        Returns the string representation.
        """
        return str(self)

    def deepcopy(self):
        """
        Returns a new object which is a deep copy.
        """
        from copy import deepcopy
        copyone = deepcopy(self.holes[0])
        copytwo = deepcopy(self.holes[1])
        return Board(rowone=copyone, storeone=self.stores[0], \
                     rowtwo=copytwo, storetwo=self.stores[1])

    def valid(self, row, move):
        """
        A move on a row is valid if move is an integer in range(1, 7)
        and if there is a stone in the corresponding hole.
        Returns True if move is valid, returns False otherwise.
        """
        if row not in [0, 1]:
            return False
        else:
            if move not in range(1, 7):
                return False
            else:
                return (self.holes[row][move-1] > 0)

    def pick(self, row, hole):
        """
        Returns all stones out of the hole with index hole
        from the row with index row.
        The number of stones afterwards at the hole of the row
        will be zero.
        """
        result = self.holes[row][hole]
        self.holes[row][hole] = 0
        return result

    def instore(self, player, idx):
        """
        Drops a stone in the store if idx < 0 and player == 0
        or if idx > 5 and player == 1.
        The index on return is not in range(6) if a stone was
        dropped in a store, otherwise the index on return is
        the index of the hole where a stone was dropped.
        """
        if(idx < 0):
            if(player == 0):
                self.stores[0] += 1
                return -1
            else:
                self.holes[1][0] += 1 
                return 0
        else:
            if(player == 1):
                self.stores[1] += 1
                return 6
            else:
                self.holes[0][5] += 1
                return 5

    def drop(self, row, hole, stones, player):
        """
        Drops a sequence of stones lifted from the hole at the row.
        Returns the row and the hole where the last stone was dropped.
        """
        idx = hole
        for cnt in range(stones):
            idx = (idx+1 if row == 1 else idx-1)
            if idx in range(6):
                self.holes[row][idx] += 1
            else:
                idx = self.instore(player, idx)
                if cnt < stones-1:       # if not at last stone
                    row = (row + 1) % 2  # then change the row
        return (row, idx)

    def copy(self, row, hole, player):
        """
        Given in row and hole the position of the last dropped stone,
        which is not a store, checks if the stones on the opposite
        row can be moved to the store.
        """
        if player == row:
            if self.holes[row][hole] == 1:
                opprow = (row + 1) % 2
                self.stores[row] += self.holes[opprow][hole]
                self.holes[opprow][hole] = 0

    def emptyside(self):
        """
        Returns True if all holes on one side are empty.
        """
        if(sum(self.holes[0]) == 0 or sum(self.holes[1]) == 0):
            return True
        else:
            return False

    def finish(self):
        """
        Moves all stones to the store on the right.
        """
        self.stores[0] += sum(self.holes[0])
        self.stores[1] += sum(self.holes[1])
        for k in range(6):
            self.holes[0][k] = 0
            self.holes[1][k] = 0

def test(brd):
    """
    Prompts the user for an index and executes the move
    on the board.
    """
    move = int(input('Enter 1, 2, 3, 4, 5, 6 : '))
    player = int(input('Give a row, either 0 or 1 : '))
    if not brd.valid(player, move):
        print('The move is not valid.')
    else:
        print('The move is valid.')
        stones = brd.pick(player, move-1)
        (row, idx) = brd.drop(player, move-1, stones, player)
        print('Last stone in row', row, 'and hole', idx+1)
        if idx in range(6):
            if(player == row) and (brd.holes[row][idx] == 1):
                print('The player gets stones from opposite row.')
                brd.copy(row, idx, player)
        else:
            print('The player gets an extra turn.')
        print('The board after the move :')
        print(brd)

def main():
    """
    Runs some tests on the board.
    There are three tests:
    (1) Check if the counterclock wise drops are correct,
        with the skipping of the store of the opponent.
    (2) Check if the player will get an extra turn if the
        last stone lands in the store of the player.
    (3) Check if the player gets the stones from the opposite row
        if the last stone lands in an empty hole.
    """
    print('The initial board :')
    brd = Board()
    print(brd)
    test(brd)
    print('A test board :')
    brd = Board(rowone = [5, 0, 3, 2, 6, 7], storeone = 2, \
                rowtwo = [0, 8, 2, 3, 0, 5], storetwo = 3)
    print(brd)
    test(brd)

if __name__ == "__main__":
    main()
