from psychopy import gui
import os
import datetime as dt
import csv
import pandas as pd

###############################################################################
#                          dialog to set the game up                          #
###############################################################################
def settings():
    myDlg = gui.Dlg(title="settings")
    myDlg.addField("Name:", tip="your name here", initial="anonymous hero")
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
# a function that calculates x and y coordinates for a snake-type stimulus using
# the tex_size and the number of tiles
def coord(tex_size, n_tiles, size_box, x, y):
    points_x = ((tex_size / 2) * -1) + (size_box[0] / 2) + (size_box[0] * x)
    points_y = ((tex_size / 2) * -1) + (size_box[0] / 2) + (size_box[0] * y)
    return points_x, points_y


###############################################################################
#                        making files and directories                         #
###############################################################################
def make_files():
    files = {"dirname": os.getcwd()}
    files["date"] = dt.datetime.today().strftime("%d/%m/%Y")
    files["scorefile"] = files["dirname"] + os.sep + "highscore.csv"
    files["insdir"] = files["dirname"] + os.sep + "Instructions"
    return files


###############################################################################
#                               Highscore file                                #
###############################################################################
def write_score(name, files, score):
    if os.path.isfile(files["scorefile"]):
        with open("highscore.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Score", "Date"])
            writer.writerow([name, score, files["date"]])
    else:
        with open("highscore.csv", "w+") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Score", "Date"])
            writer.writerow([name, score, files["date"]])


###############################################################################
#                              reading the score                              #
###############################################################################
def reading_score():
    files = make_files()
    if os.path.isfile(files["scorefile"]):
        data = pd.read_csv("highscore.csv")
        # return data[data.Score == data.Score.max()]
        data = data[data.Score == data.Score.max()]
        data = data.to_dict(orient="records")
    else:
        data = None
    return data


###############################################################################
#                            reading Instructions                             #
###############################################################################
def reading_instructions(files, ctrl_keys, name):
    txtInst = {}
    for fname in os.listdir(files["insdir"]):
        if fname.endswith(".txt"):
            with open(os.path.join(files["insdir"], fname), "r") as f:
                txtInst[os.path.splitext(fname)[0]] = f.read().format(
                    name,
                    ctrl_keys["up"].upper(),
                    ctrl_keys["down"].upper(),
                    ctrl_keys["left"].upper(),
                    ctrl_keys["right"].upper(),
                )

    return txtInst


###############################################################################
#                         printing the current score                          #
###############################################################################
def current_score(counter):
    cur_scr = "Your current score: {}".format(counter)
    return cur_scr
