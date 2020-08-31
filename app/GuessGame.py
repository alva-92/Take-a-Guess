import logging
import sys
import os
import random
import speech_recognition as sr
import GameSettings as gameSettings

class GuessGame:

    def __init__(self):
        self.__logger     = logging.getLogger('ea-take-a-guess.log')
        self.__winningNum = "Not Set"
        self.__guessedNum = "Not Set"
        self.__dificulty  = 0
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
        if (proceed != 'y' or proceed != 'Y'):
            print("Bye...")
            exit(0)

    def configure_game(self) -> int:    
        try:
            print("Select game difficulty \n 1 - {0}\n 2 - {1}\n 3 - {2}"
            .format(
                gameSettings.Lvl.EASY.name,
                gameSettings.Lvl.MEDIUM.name,
                gameSettings.Lvl.HARD.name))
            
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
        num_range = None
        if (difficulty == gameSettings.Lvl.EASY):
            self.set_winning_num(random.choice(gameSettings.NUMBERS_1))
            num_range = ("\t{words}").format(words=', '.join(gameSettings.NUMBERS_1))
        elif (difficulty == gameSettings.Lvl.MEDIUM):
            self.set_winning_num(random.choice(gameSettings.NUMBERS_2))
            num_range = ("\t{words}").format(words=', '.join(gameSettings.NUMBERS_2))
        elif (difficulty == gameSettings.Lvl.HARD):
            self.set_winning_num(random.choice(gameSettings.NUMBERS_3))
            num_range = ("\t{words}").format(words=', '.join(gameSettings.NUMBERS_3))

        print("I am thinking of a number in the given range:")
        print(num_range)

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

    def get_mic(self):
        return self.__microphone

    def get_recognizer(self):
        return self.__recognizer
        
    """
        Analyze speech from recorded from microphone
        TODO: Should be in a thread - Its blocking in slow networks
    """
    def recognize_speech_from_mic(self, recognizer, microphone):

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
