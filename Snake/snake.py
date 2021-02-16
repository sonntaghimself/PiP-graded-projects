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

import numpy as np
import little_helpers
from psychopy import visual, core, event

# ######################## global Parameters ##################################
# parameters defining the size of the grid
tex_size = 800
n_tiles = 40
size_box = ((tex_size / n_tiles), (tex_size / n_tiles))

# ######################## the visual window ##################################

win = visual.Window(size=(800, 800), units="pix")

grey = [0, 0, 0]

tex = np.array([grey, grey])
tex = np.tile(tex, (int(n_tiles / 2), int(n_tiles / 2), 1))

grid = visual.ImageStim(win, image=tex, size=tex_size, units="pix")
grid.draw()
win.flip()

# ######################### the actual snake ##################################

snake = visual.Circle(
    win,
    units="pix",
    fillColor="limegreen",
    size=((size_box[0] * 0.9), (size_box[1] * 0.9)),
)


# ######################### the actual game ###################################
up = False
down = False
right = False
left = False
x = y = 0


while True:
    keys = event.getKeys()
    win.flip()
    if "w" in keys:
        up = True
        down = right = left = False
    elif "s" in keys:
        down = True
        up = right = left = False
    elif "d" in keys:
        right = True
        down = up = left = False
    elif "a" in keys:
        left = True
        up = right = down = False
    elif "escape" in keys:
        break
        win.close()

    if up:
        # y += 1

    snake.pos = little_helpers.coord(tex_size, n_tiles, size_box, 20, 20)
    snake.setAutoDraw = True

# win.flip()
# core.wait(5)

# win.close()
# core.quit()


# food = visual.ImageStim(win, image="mouse.png", units="pix")
