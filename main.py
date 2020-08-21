""""
    This file is part of TAKE-A-GUESS which is released under an MIT License.
    See file README or go to LICENSE for full license details.    
  
    @name         main.py
    @description  This program uses speech recognition to simulate a guessing game
    @author       Gerardo Enrique Alvarenga
    @version      1.2
"""

import signal
import os
import time
import sys
import random

import logging, traceback

import speech_recognition as sr


# If you need to access files/modules in a different directory
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#gBASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

###
### Logger
###

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logFile = 'ea-take-a-guess.log'

#logging.basicConfig(filename='realtime.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Possible numbers
NUMBERS_1 = ["1", "2", "3"] 
NUMBERS_2 = ["1", "2", "3", "4", "5", "6"]
NUMBERS_3 = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] 

NUM_GUESSES  = 3  # Default number of guess 
PROMPT_LIMIT = 5  # Default number of times it will ask to repeat if it fails to understand
difficulty   = 0
word         = "None"

print("SpeechRecognition version " + sr.__version__ + "\n" )

def interrupt_signal_handler(signal, frame):
    print("Application terminated before expected by user. Exiting...")
    sys.exit(0)
    
# Analyze speech from recorded from microphone
def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        print("Please wait. Calibrating microphone...")  
        recognizer.adjust_for_ambient_noise(source, duration = 3) # Calibrate the MIC for 3 seconds
        print("Calibration Complete.\nGuess now")
        audio = recognizer.listen(source) # Record the user's input

    # Create and initialize dictionary with three keys for the response object
    response = {
        "success": True,      # API call was successful
        "error": None,        # API is unreacheable or speech was not recognized
        "transcription": None # Speech input already transcribed to text.
    }

    # Attempt to recognize the recorded input
    try:
        response["transcription"] = recognizer.recognize_google(audio, language='en-CA', show_all = False)
    except sr.RequestError: # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError: # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    return response

def configure_game():
    global difficulty
    show_game_header()
    print("Select game difficulty")
    print("1. EASY")
    print("2. MEDIUM")
    print("3. HARD")
    difficulty = input("Selection: ")

def show_game_header():
    if (sys.platform == 'win32'):
        os.system('cls')
    else:
        os.system('clear')

    print("|------------------------------|")
    print("\tGuess that number\t")
    print("|------------------------------|")

def show_game_instructions():
    print("The game is simple, you must guess the number the computer is thinking.")
    proceed = input("\nWant to play (y/n): ")
    if (proceed != 'y'):
        print("Bye...")
        exit(0)

def initialize_game():
    global word
    show_game_header()
    show_game_instructions()
    configure_game()
    show_game_header()

    if (difficulty == '1'):
        word = random.choice(NUMBERS_1) 
        print("I am thinking of a number in the given range:")
        range = ("\t{words}").format(words=', '.join(NUMBERS_1))
        print(range)
    elif (difficulty == '2'):
        word = random.choice(NUMBERS_2)
        print("I am thinking of a number in the given range:")
        range = ("\t{words}").format(words=', '.join(NUMBERS_2))
        print(range)
    elif (difficulty == '3'):
        word = random.choice(NUMBERS_3) 
        print("I am thinking of a number in the given range:")
        range = ("\t{words}").format(words=', '.join(NUMBERS_3))
        print(range)    

    print("\nYou have " + str(NUM_GUESSES) + " chances to guess...Let's see what you got. Ready?\n")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, interrupt_signal_handler) # Register interrupt signal with handler

    # create recognizer and mic objects
    r = sr.Recognizer()
    mic = sr.Microphone()

    initialize_game()
    logger.info("Take a guess - 2020")
    logger.info("Game is starting soon...")
    time.sleep(3) # Wait 3 seconds before starting the game

    for i in range(NUM_GUESSES):
        for j in range(PROMPT_LIMIT):
            print('Guess {}.'.format(i+1))
            guess = recognize_speech_from_mic(r, mic)
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