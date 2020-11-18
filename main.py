import cmpt120image
import helper

# list of scenes
scene = [i.strip('\n') for i in open('data/scenes.txt')]

# Initializes user scene
user_scene = 0

# gets the initial image
img = cmpt120image.getImage(f"images/{scene[0]}.jpg")

# displays the initial image
cmpt120image.showImage(img, scene[0])

# Initial welcome / introduction
print("Oki (Hello)! Welcome to Brocket, Alberta! I can teach you some Blackfoot\n"
      "while you are here!")

# Main loop
active = True
while active:
    app_mode = input("Do you want to learn some words around you (learn),\n"
                     "Have me test you (test),\n"
                     "Go somewhere else (move),\n"
                     "or leave? (exit)?\n")

    if app_mode.lower().strip() == "learn":
        helper.learn(helper.create_dict(f"data/{scene[user_scene]}.txt"))

    elif app_mode.lower().strip() == "test":
        top_score = helper.test(helper.create_dict(f"data/{scene[user_scene]}.txt"))
        print(top_score)

    elif app_mode.lower().strip() == "move":
        user_scene = helper.move(scene, user_scene)

    elif app_mode.lower().strip() == "exit":
        active = False

    else:
        print("Sorry, I'm unfamiliar with that command.")
