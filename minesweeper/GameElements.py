from abc import abstractmethod

"""
This file contains the elements of a minesweeper game: mines and counters and the abstract GameElement class.
"""


class GameElement(object):
    isRevealed: bool
    isFlagged: bool

    def __init__(self):
        self.isFlagged = False
        self.isRevealed = False
        super(object, self).__init__()

    @abstractmethod
    def __str__(self):
        """
        Returns a String representation of this class.
        This method is overwritten by sub classes.
        :rtype: String
        """
        if self.isFlagged:
            return "F"  # this element was flagged
        else:
            return "*"  # this element has neither been flagged nor revealed

    @abstractmethod
    def flag(self):
        """
        Marks a game element as flagged.
        This method is specified by sub classes
         :rtype Bool
        :return whether the caller has to do something
        """
        self.isFlagged = not self.isFlagged
        self.isRevealed = False

    @abstractmethod
    def reveal(self):
        """
        Marks a game element as revealed.
        This method is specified by sub classes
        :rtype Bool
        :return whether the caller has to do something
        """
        self.isRevealed = True


class Mine(GameElement):
    def __str__(self):
        if self.isRevealed:
            return "X"  # the bomb explodes
        else:
            return super().__str__()

    def flag(self):
        """
        If a mine is flagged the game has to check if the player has won.
        :rtype int
        :return: what has to be added to the flagged bombs counter
        """
        super().flag()
        if self.isFlagged:
            return 1
        else:
            return -1

    def reveal(self):
        """
        If a mine is revealed, it explodes and the game is over.
        :rtype Bool
        :return: Always True
        """
        super().reveal()
        return True


class Counter(GameElement):
    counter: int

    def __init__(self, counter):
        super().__init__()
        self.counter = counter

    def __str__(self):
        if self.isRevealed:
            return str(self.counter)  # show the bomb counter
        else:
            return super().__str__()

    def flag(self):
        """
        If a counter is flagged nothing happens
        :rtype int
        :return Always 0
        """
        super().flag()
        return 0

    def reveal(self):
        """
        If a counter is revealed it displays its count.
        If the counter is 0, the game has to reveal all adjacent counters.
        :rtype Bool
        :return whether the caller has to do something
        """
        super().reveal()
        if self.counter == 0:
            return True
        else:
            return False
