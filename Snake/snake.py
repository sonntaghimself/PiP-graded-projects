import numpy as np
import little_helpers
import os
from psychopy import visual, core, event

###############################################################################
#                              global Parameters                              #
###############################################################################
# parameters defining the size of the grid; just change tex_size to change size
# of the window and all other size variables
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
win = visual.Window(
    size=(tex_size, tex_size), units="pix", colorSpace="rgb255", useFBO=False
)

grey = [0, 0, 0]

tex = np.array([grey, grey])
tex = np.tile(tex, (int(n_tiles / 2), int(n_tiles / 2), 1))

grid = visual.ImageStim(win, image=tex, size=tex_size, units="pix")
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
snake = visual.ImageStim(
    win,
    image=files["images"] + os.sep + "snake.png",
    units="pix",
    size=((size_box[0] * 0.9), (size_box[1] * 0.9)),
)

###############################################################################
#                                 tail pieces                                 #
###############################################################################
tail = visual.Circle(
    win,
    units="pix",
    fillColor="limegreen",
    size=((size_box[0] * 0.9), (size_box[1] * 0.9)),
)

###############################################################################
#                                  the food                                   #
###############################################################################
food = visual.ImageStim(
    win,
    image=files["images"] + os.sep + "mouse.png",
    units="pix",
    size=((size_box[0] * 0.9), (size_box[1] * 0.9)),
)

###############################################################################
#                                current score                                #
###############################################################################
cur_scr = visual.TextStim(
    win,
    font="times",
    units="pix",
    colorSpace="rgb255",
    color=text_color,
    height=(tex_size / 32),
    pos=(-250, 350),
)

###############################################################################
#                            setting up the speed                             #
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

###############################################################################
#                       preparing the experimental loop                       #
###############################################################################
direction = "down"
x = y = 19
score = 0
counter = 0
game_over = False
food_x = np.random.randint(n_tiles + 1)
food_y = np.random.randint(n_tiles + 1)
no_food = 0
length = 3
points = None
for i in range(length):
    if points is None:
        points = little_helpers.coord_list(
            tex_size,
            n_tiles,
            size_box,
            x,
            (y + i),
        )
    else:
        points = points + little_helpers.coord_list(
            tex_size,
            n_tiles,
            size_box,
            x,
            (y + i),
        )


###############################################################################
#                               the actual game                               #
###############################################################################
while not game_over:
    cur_scr.text = little_helpers.current_score(counter)
    cur_scr.setAutoDraw(True)

    keys = event.getKeys()
    if ctrl_keys["up"] in keys:
        if direction == "down":
            direction = "down"
        else:
            direction = "up"
            snake.ori = 180
    elif ctrl_keys["down"] in keys:
        if direction == "up":
            direction = "up"
        else:
            direction = "down"
            snake.ori = 0
    elif ctrl_keys["right"] in keys:
        if direction == "left":
            direction = "left"
        else:
            direction = "right"
            snake.ori = 270
    elif ctrl_keys["left"] in keys:
        if direction == "right":
            direction = "right"
        else:
            direction = "left"
            snake.ori = 90
    elif "escape" in keys:
        snake.setAutoDraw(False)
        food.setAutoDraw(False)
        win.flip(clearBuffer=True)
        game_over = True
        break

    if direction == "up":
        y += 1
    elif direction == "down":
        y -= 1
    elif direction == "right":
        x += 1
    elif direction == "left":
        x -= 1

    if x >= n_tiles or y >= n_tiles or x < 0 or y < 0:
        if settings["walls"] == "yes":
            snake.setAutoDraw(False)
            win.flip(clearBuffer=True)
            game_over = True
            break

        elif settings["walls"] != "yes":
            if y >= n_tiles:
                y -= n_tiles
            elif y < 0:
                y += n_tiles
            if x >= n_tiles:
                x -= n_tiles
            elif x < 0:
                x += n_tiles

    snake_pos_x, snake_pos_y = little_helpers.coord(
        tex_size,
        n_tiles,
        size_box,
        x,
        y,
    )

    snake.pos = (snake_pos_x, snake_pos_y)
    current_points = [(snake_pos_x, snake_pos_y)]

    snake.draw()

    for point in points:
        tail.pos = point
        tail.draw()
        if snake_pos_x == point[0] and snake_pos_y == point[1]:
            game_over = True
            break

    if snake.pos[0] == food.pos[0] and snake.pos[1] == food.pos[1]:
        no_food = 0
        food_x = np.random.randint(n_tiles)
        food_y = np.random.randint(n_tiles)
        counter += 1
        length += 1
        food.draw()
    elif snake.pos[0] != food.pos[0] or snake.pos[1] != food.pos[1]:
        no_food += 1
        if no_food >= (75 * (30 / speed)):
            no_food = 0
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

    points.insert(0, snake.pos)
    points = points[0:length]

    win.flip()
    core.wait(0.005 * speed)

###############################################################################
#                                 End screen                                  #
###############################################################################
if highscore is None:
    End = visual.TextStim(
        win,
        text="NEW HIGHSCORE !!!! CONGRATULATIONS !!!!! \nYour New highscore is: {}".format(
            counter
        ),
        units="pix",
        height=(tex_size / 16),
        font="times",
        colorSpace="rgb255",
        color=text_color,
    )

    little_helpers.write_score(settings["name"], files, counter)

elif counter <= highscore[0]["Score"]:
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

elif counter > highscore[0]["Score"]:
    End = visual.TextStim(
        win,
        text="NEW HIGHSCORE !!!! CONGRATULATIONS !!!!! \nYour New highscore is: {}".format(
            counter
        ),
        units="pix",
        height=(tex_size / 16),
        font="times",
        colorSpace="rgb255",
        color=text_color,
    )

    little_helpers.write_score(settings["name"], files, counter)

cur_scr.setAutoDraw(False)
End.draw()
win.flip()
event.waitKeys()
