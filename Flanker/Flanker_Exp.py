# Flanker Experiment modeled after my Bachelors Thesis
import Flanker_helpers
###############################################################################
#                              global Parameters                              #
###############################################################################
parameters = {
    "time": {"fix": 30, "feedback": 30, "iti": 30},
    "num": {"nblks": 12, "nprac": 10, "ntrls": 60},
}

###############################################################################
#                          gathering Vp Information                           #
###############################################################################
vp_info = Flanker_helpers.gather_information()
