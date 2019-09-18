# Take-a-Guess

Simple game where the user needs to guess the number that the program is "thinking" using speech recognition.

# Description

This simple guessing game starts by letting the user select the difficulty.

+ Easy: The user tries to guess a number between 1 and 3
+ Medium: The user tries to guess a number between 1 and 6
+ Hard: The user tries to guess a number between 1 and 10

The user then gets 3 chances to guess the number the computer is "Thinking of".

# Requirements
In order for this project to operate it needs 2 libraries to be installed 

+ SpeechRecognition
SpeechRecognition is a library that helps in performing speech  recognition in python. It support for several engines and APIs, online and offline e.g. Google Cloud Speech API, Microsoft Bing Voice Recognition, IBM Speech to Text etc.

### Installing SpeechRecognition

```bash
sudo apt-get install libasound-dev
sudo apt-get install portaudio19-dev
pip install SpeechRecognition
```

# Usage

Download the main.py file into your computer.
Once donwloaded, open the terminal on the directory where the game is and run the following commands and enjoy the game!

```bash
chmod +x ./main.py
python ./main.py
```