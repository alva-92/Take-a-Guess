import os
import time
import random

import speech_recognition as sr

NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] # Number of possible numbers
NUM_GUESSES = 3  # Default number of guess 
PROMPT_LIMIT = 5 # Default number of times it will ask to repeat if it fails to understand

# Analyze speech from recorded from microphone
def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        print("Please wait. Calibrating microphone...")  
        recognizer.adjust_for_ambient_noise(source, duration = 3) # Calibrate the MIC for 3 seconds
        print("Calibration Complete")
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

if __name__ == "__main__":
    os.system('clear')
    print("SpeechRecognition version " + sr.__version__ )

    # create recognizer and mic objects
    r = sr.Recognizer()
    mic = sr.Microphone()

    # get a random word from the list
    word = random.choice(NUMBERS)

    # format the instructions string
    instructions = (
        "I'm thinking of one of these numbers:\n"
        "{words}\n"
        "You have {n} tries to guess which one.\n"
    ).format(words=', '.join(NUMBERS), n=NUM_GUESSES)

    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    time.sleep(3)

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
