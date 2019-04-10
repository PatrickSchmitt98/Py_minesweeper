from minesweeper.GameLogic import Manager

"""
This file is used to start a game of minesweeper
"""


def main():
    manager = Manager()
    prompt = "Enter command: "
    while True:
        message = input(prompt)
        if message == "quit":
            break
        else:
            print(manager.parse_input(message))


if __name__ == '__main__':
    main()
