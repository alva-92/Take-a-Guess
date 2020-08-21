import logging

class GuessGame:

    def __init__(self):
        self.__logger = logging.getLogger('ea-gGame')
        pass

    def configure_game(self) -> int:
        while True:         
            try:
                print("Select game difficulty")
                print("1. EASY")
                print("2. MEDIUM")
                print("3. HARD")
                difficulty = int(input("Selection: "))
            except ValueError:
                print("Must be an integer. Try again")
                continue
            else:
                return difficulty