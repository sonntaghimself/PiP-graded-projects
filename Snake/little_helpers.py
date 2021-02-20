# a function that calculates x and y coordinates for a snake-type stimulus using
# the tex_size and the number of tiles
from psychopy import gui

###############################################################################
#                          dialog to set the game up                          #
###############################################################################
def settings():
    myDlg = gui.Dlg(title="settings")
    myDlg.addField("Name:", tip="your name here")
    myDlg.addField(
        "difficulty:",
        choices=["easy", "medium", "hard", "insane", "yoda"],
    )
    myDlg.addField("obstacles:", choices=["yes", "no I'm scared"])
    myDlg.addField("dark mode:", choices=["yes", "no I'm scared"])
    myDlg.addField("the walls are lava:", choices=["yes", "no I'm scared"])
    ok_data = myDlg.show()
    if (
        isinstance(ok_data[0], str)
        and isinstance(ok_data[1], str)
        and isinstance(ok_data[2], str)
        and isinstance(ok_data[3], str)
        and isinstance(ok_data[4], str)
    ):
        stuff = {
            "name": ok_data[0],
            "difficulty": ok_data[1],
            "obstacles": ok_data[2],
            "dark mode": ok_data[3],
            "walls": ok_data[4],
        }
        return stuff
    else:
        settings()


###############################################################################
#           calculating coordinates in accordance with the texture            #
###############################################################################
def coord(tex_size, n_tiles, size_box, x, y):
    points_x = ((tex_size / 2) * -1) + (size_box[0] / 2) + (size_box[0] * x)
    points_y = ((tex_size / 2) * -1) + (size_box[0] / 2) + (size_box[0] * y)
    return points_x, points_y
