<div align="center">
<h1 align="center">Take-a-Guess </h1>

<p align="center">
<img src="./assets/logo-1.jpg" width="400px" height="400px">
</p>

<p align="center">
Simple game where the user needs to guess the number that the program is "thinking" using speech recognition.
</p>

![technology-1-badge][technology-1-image] ![license-badge][license-image]
</div>


## Table of contents
+ [Description](#Description)
+ [Requirements](#Requirements)
+ [Usage](#Usage)
+ [License](#License)

## Description

This simple guessing game starts by letting the user select the difficulty.

+ <strong>Easy:</strong>: The user tries to guess a number between 1 and 3.
+ <strong>Medium:</strong> The user tries to guess a number between 1 and 6.
+ <strong>Hard:</strong> The user tries to guess a number between 1 and 10.

The user then gets 3 chances to guess the number the computer is "Thinking of".

## Requirements

### Linux
In order for this project to operate it needs the following lib to be installed

+ SpeechRecognition
SpeechRecognition is a library that helps in performing speech  recognition in python. It support for several engines and APIs, online and offline e.g. Google Cloud Speech API, Microsoft Bing Voice Recognition, IBM Speech to Text etc.

```bash
sudo apt-get install libasound-dev
sudo apt-get install portaudio19-dev
pip install SpeechRecognition
pip install PyAudio
```

### Windows
pip install SpeechRecognition
pip install PyAudio

# Usage

Download the main.py file into your computer.
Once donwloaded, open the terminal on the directory where the game is and run the following commands and enjoy the game!

```bash
chmod +x ./main.py
python ./main.py
```

Note if running on Windows using Git Bash run using the following command:

```bash
winpty ptyhon ./main.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

[technology-1-image]: https://images1-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&url=https://img.shields.io/badge/Python-v3.6-blue
[license-image]: https://images1-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&url=https://img.shields.io/badge/License-MIT-blue
