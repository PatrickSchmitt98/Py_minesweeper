from GameLogic import Manager

"""
This file is used to start a game of minesweeper
"""


def main():
    manager = Manager()
    message = ""
    prompt = "Enter command: "
    while message != "quit":
        message = input(prompt)
        print(manager.parse_input(message))


if __name__ == '__main__':
    main()
