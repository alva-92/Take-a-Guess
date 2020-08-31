from enum import Enum, unique

# Possible numbers
NUMBERS_1 = ["1", "2", "3"] 
NUMBERS_2 = ["1", "2", "3", "4", "5", "6"]
NUMBERS_3 = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] 

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

    def __init__(self):
        pass