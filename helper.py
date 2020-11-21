# Helper functions for Blackfoot project
# CMPT 120 
# Nov. 12, 2020

import wave
import random
import cmpt120image
import pygame
import time


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


def show_vocab():
    """
    input: none
    output: returns all vocab in a list of dictionaries
    """
    # Opens file and formats the naming
    filename = open("data/data_files.txt")
    files = [line.strip("\n") for line in filename]

    # Create dictionary for each vocab file and store them in a list
    all_vocab = [create_dict(f"data/{file}.txt") for file in files]

    # Prints out vocab dictionary from create vocab function
    print("Here are the all the words available!\n")
    for vocab in all_vocab:
        for blackfoot, eng in vocab.items():
            print(f"{blackfoot} - {eng}")

    return all_vocab


def create_sentence():
    user_words = []
    all_vocab = show_vocab()

    print("\nGive me two vocab in english, and I will format"
          " them into a Blackfoot sentence!\n")

    for x in range(2):
        user_word = input("Give me a word in english!\n")
        user_words.append(user_word)

    concat([f"sounds/{i.strip('?!,.').replace(' ', '_')}.wav" for i in user_words], [])


def create_dict(txt_file):
    """
    input: a text file containing string data
    output: a formatted dictionary
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


def custom_testing(vocab):
    """
    input: dictionary of vocab, Blackfoot : English
    output: user score
    """
    print("Okay, here's a harder test. Get ready!\n")

    # Keeps track of number correct
    num_correct = 0

    # Reverses order to English to Blackfoot for word generation
    vocab_two = {value: key for key, value in vocab.items()}

    # Asks 10 questions
    for x in range(10):

        # Generates random english word
        english_word = random.choice(list(vocab_two.keys()))

        # Gets correct word and initializes incorrect word
        correct_word = vocab_two[english_word]

        # Loops to ensure incorrect word is not correct word
        while True:
            incorrect_eng_word = random.choice(list(vocab_two.keys()))
            incorrect_word = vocab_two[incorrect_eng_word]

            if incorrect_word != correct_word:
                break

        # Stores word choices
        words = [correct_word, incorrect_word]

        # Generates the first random choice
        choice_one = random.choice(words)

        # Generates the second random choice that isn't choice one
        while True:
            choice_two = random.choice(words)
            if choice_two != choice_one:
                break

        # Plays the sound of words
        play_sound(vocab[choice_one])
        time.sleep(1.5)    # Gives speaker time to speak
        play_sound(vocab[choice_two])

        # asks user vocab
        user_word = input(f"What is '{english_word.lower()}' in Blackfoot?\n"
                          f"{choice_one.title()} or {choice_two.title()}\n").strip().lower()

        # Tells user if they are correct / incorrect
        if user_word == correct_word.lower():
            print("You got it!\n")
            num_correct += 1
        else:
            print("Sorry, that isn't correct.\n")

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
    # Maps out scene relative to index into dictionary
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
    word = word.replace(" ", "_").lower().strip("?!,")  # Formats for .wav files
    word_sound = pygame.mixer.Sound(f"sounds/{word}.wav")  # Initializes file
    pygame.mixer.Sound.play(word_sound)  # Plays file


def update_score(new_score, scene, user_scene, scene_scores):
    """
    input: variables to update scene scores value
    output: updated scene scores value
    """
    top_score = scene_scores[scene[user_scene]]

    # If new score is greater; replace top score
    if new_score > top_score:
        scene_scores[scene[user_scene]] = new_score
    else:
        pass


def display_score(scene_scores, hard_scene_scores):
    """
    input: Dictionary containing scene scores
    output: none (prints score)
    """
    # Prints out standard test leaderboard from dictionary
    print("\n**********************")
    print("Test Leaderboard")
    for scene, score in scene_scores.items():
        print(f"{scene.title()} - {score}/10")
    print("**********************\n")

    # Prints out harder test leaderboard from dictionary
    print("\n**********************")
    print("Hard Test Leaderboard")
    for scene, score in hard_scene_scores.items():
        print(f"{scene.title()} - {score}/10")
    print("**********************\n")


# Initializes pygame
pygame.init()
