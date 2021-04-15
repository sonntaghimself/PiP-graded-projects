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
