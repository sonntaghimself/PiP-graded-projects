# Flanker Experiment modeled after my Bachelors Thesis
import Flanker_helpers
import datetime as dt
import pandas as pd
from psychopy import visual, event, core

###############################################################################
#                              global Parameters                              #
###############################################################################
parameters = {
    "time": {"fix": 30, "feedback": 30, "iti": 30},
    "num": {"nblks": 12, "nprac": 10, "ntrls": 60},
    "keys": {"cont": "space", "left": "q", "right": "p", "resp": [keys["left"],
        keys["right"], "escape"]
}

###############################################################################
#                          gathering Vp Information                           #
###############################################################################
vp_info = Flanker_helpers.gather_information()

###############################################################################
#                           making necessary Files                            #
###############################################################################
files = Flanker_helpers.make_dirs("Flanker_Exp.py")

###############################################################################
#                              Stimulus Sequence                              #
###############################################################################
stimuli = ["HHHHH", "SSSSS", "SSHSS", "HHSHH"]
compatibility = ["comp", "comp", "incomp", "incomp"]

expSeq = Flanker_helpers.randomization(
    stimuli, compatibility, vp_info, parameters, files
)

###############################################################################
#                            Reading Instructions                             #
###############################################################################
inst_text = Flanker_helpers.reading(files, parameters["keys"])

###############################################################################
#                              Psychopy Objects                               #
###############################################################################
############
#  window  #
############
win = visual.Window(size=(640, 480), color=(0, 0, 0), units="pix")

###########
#  timer  #
###########
stopWatch = core.Clock()

#############
#  stimuli  #
#############
instStim = visual.TextStim(win, text=inst_text["inst1"], alignText="left")
fbStim = visual.TextStim(win)
fixStim = visual.ShapeStim(
        win,
        lineWidth=2,
        lineColor="white",
        pos=(0, 0),
        vertices=((-10, 0), (10, 0), (0, 0), (0, 10), (0, -10)),
        closeShape=False,
)
