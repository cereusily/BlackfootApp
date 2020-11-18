# Helper functions for Blackfoot project
# CMPT 120 
# Nov. 12, 2020

import wave
import random
import cmpt120image
import pygame


def concat(infiles, outfile):
    """
  Input: 
  - infiles: a list containing the filenames of .wav files to concatenate,
    e.g. ["hello.wav","there.wav"]
  - outfile: name of the file to write the concatenated .wav file to,
    e.g. "hellothere.wav"
  Output: None
  """
    data = []
    for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()
    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()


def create_dict(txt_file):
    """
    input: a text file containing translations
    output: a formatted dictionary Blackfoot : English
    """
    # Initializes and creates dictionary
    vocab = {}
    with open(txt_file) as file:
        for line in file:
            (key, value) = line.split(",")
            vocab[key] = value.strip("\n")
    return vocab


def learn(vocab):
    """
    input: takes in vocab dictionary and prompts user to learn
    output: none
    """
    # Introduces user what to do
    print("Great, let's learn! Look around and tell me a world in English.\n")

    # Reverses order to English to Blackfoot
    vocab = {value: key for key, value in vocab.items()}

    # Asking loop
    active = True
    while active:
        user_word = input("What do you want to learn "  # prompts  user for a word
                          "the Blackfoot word for? Type 'done' to finish\n").lower().strip()

        # Check is user word is valid in vocab // checks for user quit
        if user_word in vocab:
            play_sound(user_word)  # Plays word from sounds
            print(vocab[user_word].title())

        elif user_word == "done":
            active = False

        else:
            print("Sorry, I'm not sure I see that word around us.")


def test(vocab):
    """
    input: takes in vocab dictionary and tests user
    output: the user's score
    """
    # Readies user for test
    print("Okay, I will test you--get ready!\n")

    # Keeps track of correct answers
    num_correct = 0

    # Asks ten questions
    for x in range(10):
        test_word = random.choice(list(vocab.keys()))  # retrieves random word from vocab
        play_sound(vocab[test_word])  # Plays sound of the word

        user_word = input(f"What is {test_word.lower()}?\n").strip()  # asks user vocab

        # If user is correct; add to counter, else, reveal correct answer
        if user_word == vocab[test_word]:
            print("Good job!\n")
            num_correct += 1
        else:
            print(f"It actually means {vocab[test_word]}.\n")

    # Gives user message depending on score
    if num_correct == 10:
        input("Wow! You got 10/10! A perfect score! Press <enter>\n")
    elif num_correct == 0:
        input("Unfortunately, you didn't get any right. Press <enter>\n")
    else:
        input(f"You got {num_correct}/10! Press <enter>\n")

    return num_correct


def move(scene, user_scene):
    """
    input: current user scene (index) of scene array
    output: new user scene (index) of scene array
    """
    # Maps out scene relative to index
    scene_map = dict(zip(scene, range(0, len(scene))))

    # Formats list of scenes into string
    scene_options = "".join([i.title() + "/" for i in scene])

    # Main loop to ask for new scene
    active = True
    while active:
        print("Where do you want to go?")
        # Displays scene options for user + formats response
        user_scene = input(f"{scene_options}\n").lower().strip()

        # checks if user scene is in map + exits loop else tells user it's valid
        if user_scene in scene_map:
            user_scene = scene_map[user_scene]
            active = False
        else:
            print("Sorry, that's not a valid scene.\n")

    # gets the new image
    img = cmpt120image.getImage(f"images/{scene[user_scene]}.jpg")

    # displays the new image
    cmpt120image.showImage(img, scene[user_scene])

    # returns new user scene
    return user_scene


def play_sound(word):
    """
    input: a word passed in from a function
    output: none (plays a sound)
    """
    word = word.replace(" ", "_")  # Formats for .wav files
    word_sound = pygame.mixer.Sound(f"sounds/{word}.wav")  # Initializes file
    pygame.mixer.Sound.play(word_sound)  # Plays file


# Initializes pygame
pygame.init()
