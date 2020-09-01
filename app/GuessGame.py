import time
import logging
import sys
import os
import random
import speech_recognition as sr
import GameSettings as game

class GuessGame:

    def __init__(self):
        self.__logger     = logging.getLogger('ea-take-a-guess.log')
        self.__winningNum = "Not Set"
        self.__guessedNum = "Not Set"
        self.__dificulty  = 0
        self.__num_range  = "Not Set"
        self.__recognizer = sr.Recognizer()
        self.__microphone = sr.Microphone()
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
            print("Select game difficulty \n 1 - {0}\n 2 - {1}\n 3 - {2}"
            .format(
                game.Lvl.EASY.name,
                game.Lvl.MEDIUM.name,
                game.Lvl.HARD.name))
            
            difficulty = int(input("Selection: "))
            
            if difficulty < 1 or difficulty > 3:
                self.__logger.warning("Not a valid difficulty selection")
                raise ValueError
            else:
                self.__logger.info("Valid difficulty selection, saving selection")
                self.set_game_difficulty(difficulty)
                return game.Status.SUCCESS

        except ValueError:
            print("Must be an integer with a value of 1 to 3. Try again")
            return game.Status.INVALID_DIFFICULTY


    def set_game_difficulty(self, difficulty):
        self.__logger.debug("Saving difficulty as: " + str(difficulty))
        self.__dificulty = difficulty
        
        if (difficulty == game.Lvl.EASY.value):
            self.set_winning_num(random.choice(game.GameSettings.NUMBERS_1))
            self.__num_range = ("\t{words}").format(words=', '.join(game.GameSettings.NUMBERS_1))
        elif (difficulty == game.Lvl.MEDIUM.value):
            self.set_winning_num(random.choice(game.GameSettings.NUMBERS_2))
            self.__num_range = ("\t{words}").format(words=', '.join(game.GameSettings.NUMBERS_2))
        elif (difficulty == game.Lvl.HARD.value):
            self.set_winning_num(random.choice(game.GameSettings.NUMBERS_3))
            self.__num_range = ("\t{words}").format(words=', '.join(game.GameSettings.NUMBERS_3))
        else:
            self.__logger.error("Winning number not set")

        
        print(self.__num_range)
        time.sleep(2)

    def get_game_difficulty(self):
        return self.__dificulty

    def set_winning_num(self, num):
        self.__winningNum = num
        self.__logger.info("Winning number set to " + str(self.__winningNum))

    def get_winning_num(self):
        return self.__winningNum
    
    def check_usr_guess(self, usr_guess):
        
        if self.__winningNum == usr_guess["transcription"]:
            return True
        return False

    def get_num_range(self):
        return self.__num_range
    def get_mic(self):
        return self.__microphone

    def get_recognizer(self):
        return self.__recognizer
        
    """
        Analyze speech from recorded from microphone
        TODO: Should be in a thread - Its blocking in slow networks
    """
    def recognize_speech_from_mic(self):

        microphone = self.get_mic()
        recognizer = self.get_recognizer()

        with microphone as source:
            print("Please wait. Calibrating microphone...")  
            recognizer.adjust_for_ambient_noise(source, duration = 3) # Calibrate the MIC for 3 seconds
            print("Calibration Complete.\nGuess now")
            audio = recognizer.listen(source) # Record the user's input

        # Create and initialize dictionary with three keys for the response object
        response = {
            "success": True,      # API call was successful
            "error": 
            
            None,        # API is unreacheable or speech was not recognized
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

    def validate_speech(self, speech):
        if speech["transcription"]: # Retrieved transcription successfully exit the loop
            print("You said: {}".format(speech["transcription"]))              # Show the trascription to the user
            return True
        if not speech["success"]: # API call succeeded but no transcription was received
            return False
        if speech["error"]: # If there was an error, stop the game
            print("ERROR: {}".format(speech["error"]))
            self.__logger.error("Program failure recognizing speech")
            return False
        else:
            print("I didn't catch that. What did you say?\n")
            return False