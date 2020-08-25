import os
import sys

sys.path.insert(0, 
                os.path.abspath(os.path.join(
                    os.path.dirname(__file__), # Test dir
                    '../app')                  # Src dir
                ))

from GuessGame import GuessGame
import GameSettings as gameSettings