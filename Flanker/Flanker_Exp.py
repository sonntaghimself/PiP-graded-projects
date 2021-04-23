# Flanker Experiment modeled after my Bachelors Thesis
import Flanker_helpers
import datetime as dt
import pandas as pd
from psychopy import visual, event, core

###############################################################################
#                              global Parameters                              #
###############################################################################

############################################
#  IMPORTANT: n has to be divideable by 4  #
############################################

parameters = {
    "time": {"fix": 30, "feedback": 30, "iti": 30},
    # "num": {"nblks": 12, "nprac": 10, "ntrls": 60},
    "num": {"nblks": 1, "pracblks": 1, "nprac": 4, "ntrls": 4},
    "keys": "space",
    "size_boxes": (50, 50),
    "clicks": {"H": "left", "S": "right"},
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
inst_text = Flanker_helpers.reading(files, parameters)

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
instStim = visual.TextStim(win, text=inst_text["inst"], alignText="left")
fbStim = visual.TextStim(win)
fixStim = visual.ShapeStim(
    win,
    lineWidth=2,
    lineColor="white",
    pos=(0, 0),
    vertices=((-10, 0), (10, 0), (0, 0), (0, 10), (0, -10)),
    closeShape=False,
)
flankerStim = visual.TextStim(win, height=32)
start_box = visual.Rect(win, pos=(0, -200), size=parameters["size_boxes"])
left_box = visual.Rect(win, pos=(-285, 200), size=parameters["size_boxes"])
right_box = visual.Rect(win, pos=(285, 200), size=parameters["size_boxes"])

mouse = event.Mouse(win=win, visible=True)


###############################################################################
#                              Block/Trial loop                               #
###############################################################################
for blk in expSeq:  # block loop

    blk = [x for x in blk if x]

    # show some instructions before first block and wait for key press

    if blk[0]["blk"] == 1:
        instStim.draw()
        win.flip()
        event.waitKeys(keyList=parameters["keys"])

    for trl in blk:  # trial loop

        mouse.clickReset()
        event.clearEvents()
        start_trl = False

        start_box.draw()
        win.flip()

        while start_trl is not True:
            buttons = mouse.getPressed()
            if mouse.isPressedIn(start_box, buttons=[0]):
                start_trl = True

        # present fixation cross
        for _ in range(parameters["time"]["fix"]):
            fixStim.draw()
            win.flip()

        # present flanker stimulus and reset stop watch
        flankerStim.text = trl["stimulus"]
        flankerStim.draw()
        left_box.draw()
        right_box.draw()

        win.callOnFlip(stopWatch.reset)
        win.flip()

        # get response

        mouse.clickReset()
        # event.clearEvents()
        trl_complete = False
        nclicks = 0
        mouse_positions = [mouse.getPos()]
        first = True
        while trl_complete is not True:
            buttons, times = mouse.getPressed(getTime=True)
            if mouse.mouseMoved():
                mouse_positions.append(mouse.getPos())
                if first is True:
                    first_movement = stopWatch.getTime()
                    first = False
            if buttons[0] > nclicks:
                nclicks += 1
            if mouse.isPressedIn(left_box, buttons=[0]):
                response = "left"
                trl_complete = True
            elif mouse.isPressedIn(right_box, buttons=[0]):
                response = "right"
                trl_complete = True

        if response == trl["corr_resp"]:
            corr = 1
            fbStim.text = "Correct"
        elif response != trl["corr_resp"]:
            corr = 2
            fbStim.text = "Incorrect"

        # show feedback
        for _ in range(parameters["time"]["feedback"]):
            fbStim.draw()
            win.flip()

        # update data dict
        trl["date"] = dt.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
        trl["nclicks"] = nclicks
        trl["rt"] = {"first_movement": first_movement, "times": times}
        trl["corr"] = corr
        trl["pos"] = mouse_positions

        # blank screen for inter-trial-interval
        for _ in range(parameters["time"]["iti"]):
            win.flip()

    # show block feedback and wait for keypress
    # calculate some block DVs
    blk_num = blk[0]["blk"]
    num_trls = len(blk)
    corr = [x["corr"] for x in blk]
    blk_per = (corr.count(1) / num_trls) * 100

    fb_txt = "Block {}, \n Correct: {}%".format(blk_num, blk_per)
    fb_txt = fb_txt + "\n\nPress the spacebar to continue."
    fbStim.text = fb_txt
    fbStim.draw()
    win.flip()
    event.waitKeys(keyList=[parameters["keys"]])

    # blank screen for inter-trial-interval
    for _ in range(parameters["time"]["iti"]):
        win.flip()

###############################################################################
#                               saving Results                                #
###############################################################################
# flatted 2D list of dicts
tmpData = [trial for data in expSeq for trial in data if trial]

# create pandas data frame
dataDF = pd.DataFrame()
dataDF = dataDF.from_dict(tmpData)

# write to * .txt
dataDF.to_csv(files["resfile"], header=True, index=False, sep="\t", mode="w")

# close window and quit
win.close()
core.quit()
