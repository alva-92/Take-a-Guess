""""
    This file is part of TAKE-A-GUESS which is released under an MIT License.
    See file README or go to LICENSE for full license details.    
  
    @name         main.py
    @description  This program uses speech recognition to simulate a guessing game
    @author       Gerardo Enrique Alvarenga
    @version      1.4.0
"""

import signal
import os
import time
import sys
import random
import logging, traceback
from logging.handlers import RotatingFileHandler
import GameSettings as gameSettings

import speech_recognition as sr

from GuessGame import GuessGame as guessGame

# If you need to access files/modules in a different directory
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#gBASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""
    Configure Application logger
    Logs both to console and debug log file.
    Application logs set DEBUG.
"""

### Format string for more detailed debugging
db_a_fmtstr = '[%(asctime)s] - {%(filename)s:%(lineno)d} - %(levelname)s -- %(message)s'

### Format string for basic debugging
db_b_fmtstr = '[%(asctime)s] - {%(lineno)d} - %(levelname)s -- %(message)s'

### Date format
dt_fmtstr = "%d/%m/%Y %I:%M:%S %p"

file_handler   = logging.FileHandler(filename='ea-take-a-guess.log',mode="a")
stdout_handler = logging.StreamHandler(sys.stdout)
handlers       = [file_handler, stdout_handler]

logging.basicConfig(
    level    = logging.DEBUG, 
    format   = db_a_fmtstr,
    handlers = handlers,
    datefmt  = dt_fmtstr
)

logger = logging.getLogger('ea-gGame')

gGame = guessGame()

NUM_GUESSES  = 3  # Default number of guess 
PROMPT_LIMIT = 5  # Default number of times it will ask to repeat if it fails to understand
word         = "None"

def interrupt_signal_handler(signal, frame):
    print("Application terminated before expected by user. Exiting...")
    sys.exit(0)

def initialize_game():
    global word
    
    gGame.show_game_header()
    gGame.show_game_instructions()

    while True:
        result = gGame.configure_game()
        if result == gameSettings.SUCCESS:
            break
        else:
            continue
    
    gGame.show_game_header()
    word = gGame.get_winning_num()
    
    print("\nYou have " + str(NUM_GUESSES) + " chances to guess...Let's see what you got. Ready?\n")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, interrupt_signal_handler) # Register interrupt signal with handler

    initialize_game()
    logger.info("Take a guess - 2020")
    logger.info("Game is starting soon...")
    time.sleep(3) # Wait 3 seconds before starting the game

    for i in range(NUM_GUESSES):
        for j in range(PROMPT_LIMIT):
            print('Guess {}.'.format(i+1))
            
            guess = gGame.recognize_speech_from_mic(gGame.get_recognizer(), gGame.get_mic()) # TODO: Refactor to not take parameters

            if guess["transcription"]: # Retrieved transcription successfully exit the loop
                break
            if not guess["success"]: # API call succeeded but no transcription was received
                break
            print("I didn't catch that. What did you say?\n")

        if guess["error"]: # If there was an error, stop the game
            print("ERROR: {}".format(guess["error"]))
            break

        print("You said: {}".format(guess["transcription"]))              # Show the trascription to the user
        guess_is_correct = guess["transcription"].lower() == word.lower() # Check if guessed number was correct
        user_has_more_attempts = i < NUM_GUESSES - 1                      # Check if there are any attempts left and reduce the count

        if guess_is_correct: # determine if the user has won the game
            print("Oh snap! You actually guessed it! You win! " + format(word))
            break
        elif user_has_more_attempts: # Check if there are any attempts left
            print("Nope. Try again.\n")
        else: # if no attempts left, the user loses the game
            print("You lost!\nI was thinking of '{}'.".format(word))
            break