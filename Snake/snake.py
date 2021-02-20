# the idea is to reproduce the popular phone game snake.
# pygame.key (see Solutions 8.12.2020) would be a smart option for me to use i
# think.

# important things i need to implement:
#     > if snake moves out on one edge, it reenters on the next
#     > food appears in random locations, if the snake eats it, it grows.
#     > if the snake bites itself, you loose
#     > when do you complete a level and move on to the next?

# some additional ideas:
# > obstacles on new levels
# > snake in the dark, not actually being able to see the whole game, but just
# a few degrees of visual angle in front of my snake. Plus/minus 30 degrees
# > when the snake eats, a little munching sound
# TIPP: A mask.

# having a high_score file that acutally is printed out at the start and the
# end would be cool?
# also, increase score every time a snack is eaten

import numpy as np
import little_helpers
from psychopy import visual, core, event

###############################################################################
#                              global Parameters                              #
###############################################################################
# parameters defining the size of the grid
tex_size = 800
n_tiles = 40
size_box = ((tex_size / n_tiles), (tex_size / n_tiles))
settings = little_helpers.settings()
text_color = [255, 0, 0]
ctrl_keys = {"up": "w", "down": "s", "left": "a", "right": "d"}
files = little_helpers.make_files()
inst_text = little_helpers.reading_instructions(files, ctrl_keys, settings["name"])
inst_text = inst_text["instructions"]
highscore = little_helpers.reading_score()

###############################################################################
#                              the visual window                              #
###############################################################################
win = visual.Window(size=(800, 800), units="pix", colorSpace="rgb255")

# grey = [0, 0, 0]
# darkolivegreen1 = [85, 107, 47]
darkolivegreen1 = [-0.33, -0.16, -0.63]
darkolivegreen2 = [0.58, 1, -0.12]

tex = np.array([darkolivegreen1, darkolivegreen2])
# tex = np.array([grey, grey])
tex = np.tile(tex, (int(n_tiles / 2), int(n_tiles / 2), 1))

grid = visual.ImageStim(win, image=tex, size=tex_size, units="pix", colorSpace="rgb255")
grid.draw()
win.flip()

###############################################################################
#                                Start screen                                 #
###############################################################################
start_text = visual.TextStim(
    win,
    units="pix",
    colorSpace="rgb255",
    font="times",
    color=text_color,
    height=(tex_size / 32),
    text=inst_text,
)
start_text.draw()
win.flip()
event.waitKeys()
###############################################################################
#                              the actual snake                               #
###############################################################################
snake = visual.Circle(
    win,
    units="pix",
    fillColor="limegreen",
    size=((size_box[0] * 0.9), (size_box[1] * 0.9)),
    # size=(100, 100),
)

snake.setAutoDraw(True)
###############################################################################
#                                  the food                                   #
###############################################################################
food = visual.ImageStim(
    win,
    image="mouse.png",
    units="pix",
    size=((size_box[0] * 0.9), (size_box[1] * 0.9)),
)
###############################################################################
#                               the actual game                               #
###############################################################################
if settings["difficulty"] == "easy":
    speed = 30
elif settings["difficulty"] == "medium":
    speed = 20
elif settings["difficulty"] == "hard":
    speed = 10
elif settings["difficulty"] == "insane":
    speed = 5
elif settings["difficulty"] == "yoda":
    speed = 1


up = False
down = False
right = False
left = False
x = y = 19
score = 0
counter = 0


while True:
    # counter += 1
    keys = event.getKeys()
    win.flip()
    if ctrl_keys["up"] in keys:
        up = True
        down = right = left = False
    elif ctrl_keys["down"] in keys:
        down = True
        up = right = left = False
    elif ctrl_keys["right"] in keys:
        right = True
        down = up = left = False
    elif ctrl_keys["left"] in keys:
        left = True
        up = right = down = False
    elif "escape" in keys:
        break
        win.close()

    if up:
        y += 1
        for fps in range(speed):
            win.flip()
    elif down:
        y -= 1
        for fps in range(speed):
            win.flip()
    elif right:
        x += 1
        for fps in range(speed):
            win.flip()
    elif left:
        x -= 1
        for fps in range(speed):
            win.flip()

    if x >= 40 or y >= 40 or x < 0 or y < 0:
        if settings["walls"] == "yes":
            snake.setAutoDraw(False)
            # End.draw()
            # win.flip()
            # event.waitKeys()
            break
            win.flip()

        elif settings["walls"] != "yes":
            if y >= 40:
                y -= 40
            elif y < 0:
                y += 40
            if x >= 40:
                x -= 40
            elif x < 0:
                x += 40

    snake_pos_x, snake_pos_y = little_helpers.coord(tex_size, n_tiles, size_box, x, y)
    snake.pos = (snake_pos_x, snake_pos_y)

    if "f" in keys:
        food_x = np.random.randint(n_tiles + 1)
        food_y = np.random.randint(n_tiles + 1)
        food.pos = little_helpers.coord(
            tex_size,
            n_tiles,
            size_box,
            food_x,
            food_y,
        )
        food.draw()

###############################################################################
#                                 End screen                                  #
###############################################################################
End = visual.TextStim(
    win,
    text="Game Over. \nYour Score was: {} \n\nThe current highscore is: {} \nand it is held by: {}".format(
        counter,
        highscore[0]["Score"],
        highscore[0]["Name"],
    ),
    units="pix",
    height=(tex_size / 16),
    font="times",
    colorSpace="rgb255",
    color=text_color,
)
End.draw()
win.flip()
event.waitKeys()


little_helpers.write_score(settings["name"], files, counter)
