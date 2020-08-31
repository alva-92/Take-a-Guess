from enum import Enum, unique




SUCCESS            = 1001
INVALID_DIFFICULTY = 1800

@unique
class Lvl(Enum):
    EASY   = 1
    MEDIUM = 2
    HARD   = 3

class GameCodes:
    pass

class GameSettings:

    # Possible numbers
    NUMBERS_1 = ["1", "2", "3"] 
    NUMBERS_2 = ["1", "2", "3", "4", "5", "6"]
    NUMBERS_3 = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] 

    NUM_GUESSES  = 3  # Default number of guess 
    PROMPT_LIMIT = 5  # Default number of times it will ask to repeat if it fails to understand