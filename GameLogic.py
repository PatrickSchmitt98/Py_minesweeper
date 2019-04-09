from random import randint
from typing import List

from numpy import zeros

import GameElements

"""
This file contains the logic of a minesweeper game.
"""


class GameRound(object):
    """
    This class manages a round of minesweeper.
    """
    width: int
    height: int
    bomb_count: int
    initialized: bool
    ended: bool
    won: bool
    flagged_bombs: int
    revealed_counters: int
    elements: []

    def __init__(self, width: int, height: int, bomb_count: int):
        """
        Create a new game round with a field from the specified dimensions and bomb count
        :param width:  width of field
        :param height: height of field
        :param bomb_count: number of bombs
        """
        self.bomb_count = bomb_count
        self.width = width
        self.height = height
        self.ended = False
        self.won = False
        self.initialized = False
        self.flagged_bombs = 0
        self.revealed_counters = 0
        self.elements = zeros((height, width), dtype=GameElements.GameElement)  # element matrix

    def get_adjacent_bomb_count(self, x, y):
        """
        This method determines how many bombs are adjacent to an element on (x,y)
        :param x: x position
        :param y: y position
        :rtype int
        :return: count of adjacent bombs
        """
        counter = 0
        for check_y in range(y - 1, y + 2):
            if 0 <= check_y < self.height:
                for check_x in range(x - 1, x + 2):
                    if 0 <= check_x < self.width:
                        element = self.elements[check_y, check_x]
                        if isinstance(element, GameElements.Bomb):
                            counter += 1
        return counter

    def place_elements(self, x, y):
        """
        This method places bombs in the elements matrix on random positions.
        No bomb is placed on (x,y).
        After the bombs are placed the matrix is filled with counters.
        :param x: x ignore
        :param y: y ignore
        """
        self.initialized = True
        positions = [(y, x)]
        for i in range(0, self.bomb_count):
            k = randint(0, self.width - 1)
            j = randint(0, self.height - 1)
            if positions.__contains__((j, k)):
                i -= 1
            else:
                positions.append((j, k))
                self.elements[j][k] = GameElements.Bomb()
        print(positions)
        self.elements[y][x] = GameElements.Counter(self.get_adjacent_bomb_count(x, y))
        for i in range(0, self.height):
            for j in range(0, self.width):
                if not positions.__contains__((i, j)):
                    counter = self.get_adjacent_bomb_count(j, i)
                    self.elements[i][j] = GameElements.Counter(counter)

    @property
    def __str__(self):
        """
        Returns a representation of the game as a string.
        Representation of elements is specified in GameElements.py
        :rtype str
        :return: String representation of the game
        """
        sb: List[str] = [""]
        result = ""
        if self.ended:
            if self.won:
                sb.append("You won:\n")
            else:
                sb.append("Game Over:\n")
        sb.append("  ")
        for x in range(0, self.width):
            sb.append(str(x))
            sb.append(" ")
        sb.append("\n")
        for y in range(0, self.height):
            sb.append(str(y) + " ")
            for x in range(0, self.width):
                element: GameElements.GameElement = self.elements[y][x]
                sb.append(element.__str__() + " ")
            sb.append("\n")
        result = result.join(sb)
        return result

    def flag(self, x, y):
        """
        Flags the element on (x,y).
        :param x: x coordinate
        :param y: y coordinate
        :rtype str
        :return self.__str__()
        """
        if not self.ended:
            if self.initialized:
                element: GameElements.GameElement = self.elements[y][x]  # the matrix is indexed differently, so the
                # coords differ
                self.flagged_bombs += element.flag()
                if self.flagged_bombs == self.bomb_count:
                    self.ended = True
                    self.won = True
                return self.__str__
            else:
                return "You have to reveal at least one field before you can use flag."

    def reveal(self, x, y, nop=False):
        """
        Reveals the element at (x,y).
        If the game has not been initialized, this will initialize it.
        :param nop: If nop is true no output is generated
        :param x: x coordinate
        :param y: y coordinate
        :rtype str
        :return: nop ? empty string : self.__str__()
        """
        if not self.ended:
            if not self.initialized:
                self.place_elements(x, y)
            element: GameElements.GameElement = self.elements[y][x]  # the matrix is indexed differently, so we have
            # to switch x and y
            if isinstance(element, GameElements.Bomb):
                if element.reveal():
                    self.ended = True
                    self.won = False
            else:
                if element.reveal():
                    self.reveal_adjacent_counters(x, y)
                self.revealed_counters += 1
                if self.revealed_counters == self.width * self.height - self.bomb_count:
                    self.ended = True
                    self.won = True
            if nop:
                return ""
            else:
                return self.__str__

    def reveal_adjacent_counters(self, x, y):
        """
        This method is called by reveal() if a revealed counter is 0.
        It reveals all adjacent fields.
        :param x: x coordinate
        :param y: y coordinate
        """
        for check_y in range(y - 1, y + 2):
            if 0 <= check_y < self.height:
                for check_x in range(x - 1, x + 2):
                    if 0 <= check_x < self.width:
                        element: GameElements.GameElement = self.elements[check_y][check_x]  # the matrix is indexed
                        # differently, so we have to switch x and y
                        if isinstance(element, GameElements.Counter) and not element.isRevealed:
                            self.reveal(check_x, check_y, True)

    def print_empty(self) -> str:
        """
        This method prints an empty matrix.
        :return: empty matrix
        """
        sb: List[str] = [""]
        result = ""
        sb.append("New Game: ")
        sb.append(str(self.width))
        sb.append(" x ")
        sb.append(str(self.height))
        sb.append(" Bombs: ")
        sb.append(str(self.bomb_count))
        sb.append("\n")
        for x in range(0, self.width):
            sb.append(str(x))
            sb.append(" ")
        sb.append("\n")
        for y in range(0, self.height):
            sb.append(str(y) + " ")
            for x in range(0, self.width):
                sb.append("* ")
        result = result.join(sb)
        return result


class Manager(object):
    """
    This class manages a game round.
    """
    game_round: GameRound
    initialized: bool

    def __init__(self):
        """
        Initializes the manager
        """
        self.initialized = False

    def parse_input(self, message: str) -> str:
        """
        Tries to parse a command from message and executes it on its saved game round.
        :param message: message to parse
        :return: result from game round or error
        """
        if self.initialized:
            if self.game_round.ended:
                self.initialized = False  # reset after the game is over
        if message[:6] == "reveal":
            if self.initialized:
                index = message.find(",", 6)
                try:
                    x = int(message[6:index])
                    y = int(message[index + 1])
                except ValueError:
                    return "Error: Could not parse value for x or y."
                try:
                    return self.game_round.reveal(x, y)
                except IndexError:
                    return "Error: Value for x or y is out of bounds."
            else:
                return "Please use 'new' to start a round of minesweeper first."
        elif message[:4] == "flag":
            if self.initialized:
                index = message.find(",", 4)
                try:
                    x = int(message[4:index])
                    y = int(message[index + 1])
                except ValueError:
                    return "Error: Could not parse value for x or y."
                try:
                    return self.game_round.flag(x, y)
                except IndexError:
                    return "Error: Value for x or y is out of bounds."
            else:
                return "Please use 'new' to start a round of minesweeper first."
        elif message[:3] == "new":
            if message[4:8] == "easy":
                self.game_round = GameRound(8, 8, 10)
                return self.game_round.print_empty()
            elif message[4:8] == "hard":
                self.game_round = GameRound(30, 16, 99)
                return self.game_round.print_empty()
            elif message[4:10] == "medium":
                self.game_round = GameRound(16, 16, 40)
                return self.game_round.print_empty()
        elif message[:4] == "help":
            return ""

        else:
            return "Unrecognized command. Use 'help' for a list of commands."
