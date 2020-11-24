import cmpt120image
import helper

# list of scenes
scene = [i.strip('\n') for i in open('data/scenes.txt')]

# initializes scene scores as a dictionary
scene_scores = dict(zip(scene, [0, 0, 0, 0]))
hard_scene_scores = dict(zip(scene, [0, 0, 0, 0]))

# Initializes user scene
user_scene = 0

# gets the initial image
img = cmpt120image.getImage(f"images/{scene[user_scene]}.jpg")

# displays the initial image
cmpt120image.showImage(img, scene[user_scene])

# Initial welcome / introduction
print("Oki (Hello)! Welcome to Brocket, Alberta! I can teach you some Blackfoot\n"
      "while you are here!")

# Main loop
active = True
while active:

    # Asks user what to do
    app_mode = input("Do you want to learn some words around you (learn),\n"
                     "Have me test you (test),\n"
                     "Have me test you harder (hard test)\n"
                     "See the leaderboard (scores)\n"
                     "Go somewhere else (move),\n"
                     "Hear a sentence in Blackfoot (sentence)\n"
                     "or leave? (exit)?\n")

    if app_mode.lower().strip() == "learn":
        helper.learn(helper.create_dict(f"data/vocab/{scene[user_scene]}.txt"))

    elif app_mode.lower().strip() == "test":
        new_score = helper.test(helper.create_dict(f"data/vocab/{scene[user_scene]}.txt"))
        helper.update_score(new_score, scene, user_scene, scene_scores)

    elif app_mode.lower().strip() == "hard test":
        new_score = helper.custom_testing(helper.create_dict(f"data/vocab/{scene[user_scene]}.txt"))
        helper.update_score(new_score, scene, user_scene, hard_scene_scores)

    elif app_mode.lower().strip() == "scores":
        helper.display_score(scene_scores, hard_scene_scores)

    elif app_mode.lower().strip() == "sentence":
        helper.create_sentence()

    elif app_mode.lower().strip() == "move":
        user_scene = helper.move(scene, user_scene)

    elif app_mode.lower().strip() == "exit":
        print("\nThanks for learning!")
        active = False

    else:
        print("Sorry, I'm unfamiliar with that command.")
