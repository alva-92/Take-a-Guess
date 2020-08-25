import logging
import sys
import os
import random
import GameSettings as gameSettings

class GuessGame:

    def __init__(self):
        self.__logger     = logging.getLogger('ea-gGame')
        self.__winningNum = "Not Set"
        self.__guessedNum = "Not Set"
        self.__dificulty  = 0

        pass

    def show_game_header(self):
        if (sys.platform == 'win32'):
            os.system('cls')
        else:
            os.system('clear')

        print("|------------------------------|")
        print("\tGuess that number\t")
        print("|------------------------------|")

    def show_game_instructions(self):
        print("The game is simple, you must guess the number the computer is thinking.")
        proceed = input("\nWant to play (y/n): ")
        if (proceed != 'y'):
            print("Bye...")
            exit(0)

    def configure_game(self) -> int:    
        try:
            print("Select game difficulty")
            print("1. EASY")
            print("2. MEDIUM")
            print("3. HARD")
            difficulty = int(input("Selection: "))
            if difficulty < 1 or difficulty > 3:
                raise ValueError
        except ValueError:
            print("Must be an integer with a value of 1 to 3. Try again")
            return gameSettings.INVALID_DIFFICULTY
        else:
            self.set_game_difficulty(difficulty)
            return gameSettings.SUCCESS

    def set_game_difficulty(self, difficulty):
        self.__dificulty = difficulty
        if (difficulty == 1):
            self.set_winning_num(random.choice(gameSettings.NUMBERS_1))
            print("I am thinking of a number in the given range:")
            range = ("\t{words}").format(words=', '.join(gameSettings.NUMBERS_1))
            print(range)
        elif (difficulty == 2):
            self.set_winning_num(random.choice(gameSettings.NUMBERS_2))
            print("I am thinking of a number in the given range:")
            range = ("\t{words}").format(words=', '.join(gameSettings.NUMBERS_2))
            print(range)
        elif (difficulty == 3):
            self.set_winning_num(random.choice(gameSettings.NUMBERS_3))
            print("I am thinking of a number in the given range:")
            range = ("\t{words}").format(words=', '.join(gameSettings.NUMBERS_3))
            print(range)

    def get_game_difficulty(self):
        return self.__dificulty

    def set_winning_num(self, num):
        self.__winningNum = num

    def get_winning_num(self):
        return self.__winningNum
    
    def check_usr_guess(self, usr_guess):
        if self.__winningNum == usr_guess:
            return True
        return False
