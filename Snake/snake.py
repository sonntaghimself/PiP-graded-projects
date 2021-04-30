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
up = False
down = True
right = False
left = False
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
            (y + (i + 1)),
        )
    else:
        points = points + little_helpers.coord_list(
            tex_size,
            n_tiles,
            size_box,
            x,
            (y + (i + 1)),
        )


###############################################################################
#                               the actual game                               #
###############################################################################
while not game_over:
    cur_scr.text = little_helpers.current_score(counter)
    cur_scr.setAutoDraw(True)
    keys = event.getKeys()
    if ctrl_keys["up"] in keys:
        if down:
            down = True
        else:
            up = True
            down = right = left = False
            snake.ori = 180
    elif ctrl_keys["down"] in keys:
        if up:
            up = True
        else:
            down = True
            up = right = left = False
            snake.ori = 0
    elif ctrl_keys["right"] in keys:
        if left:
            left = True
        else:
            right = True
            down = up = left = False
            snake.ori = 270
    elif ctrl_keys["left"] in keys:
        if right:
            right = True
        else:
            left = True
            up = right = down = False
            snake.ori = 90
    elif "escape" in keys:
        snake.setAutoDraw(False)
        food.setAutoDraw(False)
        win.flip(clearBuffer=True)
        game_over = True
        break

    if x >= 40 or y >= 40 or x < 0 or y < 0:
        if settings["walls"] == "yes":
            snake.setAutoDraw(False)
            win.flip(clearBuffer=True)
            game_over = True
            break

        elif settings["walls"] != "yes":
            if y >= 40:
                y -= 40
            elif y < 0:
                y += 40
            if x >= 40:
                x -= 40
            elif x < 0:
                x += 40

    snake_pos_x, snake_pos_y = little_helpers.coord(
        tex_size,
        n_tiles,
        size_box,
        x,
        y,
    )

    snake.pos = (snake_pos_x, snake_pos_y)
    current_points = [(snake_pos_x, snake_pos_y)]

    win.flip(clearBuffer=True)
    snake.draw()

    for i in range(length):
        tail.pos = points[i]
        tail.draw()

    for i in range(1, length):
        if snake_pos_x == points[i][0] and snake_pos_y == points[i][1]:
            game_over = True
            break

    if snake.pos[0] == food.pos[0] and snake.pos[1] == food.pos[1]:
        no_food = 0
        food_x = np.random.randint(n_tiles + 1)
        food_y = np.random.randint(n_tiles + 1)
        counter += 1
        length += 1
        food.draw()
    elif snake.pos[0] != food.pos[0] or snake.pos[1] != food.pos[1]:
        no_food += 1
        if no_food >= 50:
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

    if points is None:
        points = current_points
    elif points is not None:
        points = current_points + points

    if len(points) > (length):
        points.pop()

    if up:
        y += 1
        for fps in range(speed):
            fps
            core.wait(0.005)
    elif down:
        y -= 1
        for fps in range(speed):
            fps
            core.wait(0.005)
    elif right:
        x += 1
        for fps in range(speed):
            fps
            core.wait(0.005)
    elif left:
        x -= 1
        for fps in range(speed):
            fps
            core.wait(0.005)

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
