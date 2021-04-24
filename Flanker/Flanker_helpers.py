from psychopy import gui, os
import datetime as dt
import random

###############################################################################
#                                   VP Info                                   #
###############################################################################
def gather_information():
    # Dictionary, to store the information in.
    myDlg = gui.Dlg(title="participant information")
    myDlg.addText("Subject info")
    myDlg.addField("Vp Num:", initial=1, tip="this must be a number.")
    myDlg.addField("Age:", initial=18, tip="this must be a number.")
    myDlg.addField(
        "Gender:", choices=["female", "male", "diverse", "I don't want to answer"]
    )
    myDlg.addField("Handedness", choices=["l", "r"])
    myDlg.addField("record movement", choices=["True", "False"])
    ok_data = myDlg.show()
    if (
        # type(ok_data[0]) == int
        isinstance(ok_data[0], int)
        and isinstance(ok_data[1], int)
        # and type(ok_data[1]) == int
        and (ok_data[1]) in range(18, 61)
    ):
        global vpInfo
        vpInfo = {
            "vp_num": ok_data[0],
            "age": ok_data[1],
            "gender": ok_data[2],
            "handedness": ok_data[3],
            "record_pos": ok_data[4],
        }
        return vpInfo
    else:
        gather_information()


###############################################################################
#                                making Files                                 #
###############################################################################
def make_dirs(filename):
    files = {"dirname": os.getcwd(), "filename": filename}
    files["expname"] = os.path.basename(files["filename"])[:-3]
    files["date"] = dt.datetime.today().strftime("%d/%m/%Y")
    files["insdir"] = files["dirname"] + os.sep + "Instructions"
    files["resdir"] = files["dirname"] + os.sep + "Results"

    # create results directory if required
    if not os.path.isdir(files["resdir"]):
        os.makedirs(files["resdir"])

    tmpName = files["resdir"] + os.sep + files["expname"]
    files["resfile"] = tmpName + "_" + str(vpInfo["vp_num"]) + ".res"

    if os.path.isfile(files["resfile"]):
        askUser = None
        while askUser not in ["y", "n"]:
            askUser = input("File exists! Overwrite? (y, n): ").lower()
        if askUser == "y":
            os.remove(files["resfile"])
        elif askUser == "n":
            sys.exit()
    return files


###############################################################################
#                    Randomizing the experimental sequence                    #
###############################################################################


def randomization(stimuli, compatibility, vpInfo, parameters, files):
    stim = list(zip(stimuli, compatibility))

    totblks = parameters["num"]["pracblks"] + parameters["num"]["nblks"]

    if parameters["num"]["ntrls"] < 4:
        expSeq = [[{} for _ in range(4)] for _ in range(totblks)]
    elif parameters["num"]["ntrls"] >= 4:
        expSeq = [
            [{} for _ in range(parameters["num"]["ntrls"])] for _ in range(totblks)
        ]

    for iblk, blk in enumerate(expSeq):

        if iblk < parameters["num"]["pracblks"]:
            if parameters["num"]["nprac"] <= 4:
                stim_blk = stim
            else:
                stim_blk = stim * int((parameters["num"]["nprac"] / len(stim)))
            practice = True
        else:
            if parameters["num"]["ntrls"] <= 4:
                stim_blk = stim
            else:
                stim_blk = stim * int((parameters["num"]["ntrls"] / len(stim)))
            practice = False

        random.shuffle(stim_blk)

        for itrl, trl in enumerate(blk):

            if itrl >= len(stim_blk):
                break

            for i in vpInfo:
                trl[i] = vpInfo[i]

            trl["expname"] = files["expname"]
            trl["blk"] = iblk + 1
            trl["trl"] = itrl + 1
            trl["practice"] = practice
            trl["stimulus"] = stim_blk[itrl][0]
            trl["compatibility"] = stim_blk[itrl][1]

            if trl["stimulus"][2] == "H":
                trl["corr_resp"] = parameters["clicks"]["H"]
            elif trl["stimulus"][2] == "S":
                trl["corr_resp"] = parameters["clicks"]["S"]

    return expSeq


###############################################################################
#                            Reading instructions                             #
###############################################################################


def reading(files, parameters):
    txtInst = {}
    for fname in os.listdir(files["insdir"]):
        if fname.endswith(".txt"):
            with open(os.path.join(files["insdir"], fname), "r") as f:
                txtInst[os.path.splitext(fname)[0]] = f.read().format(
                    parameters["clicks"]["H"].capitalize(),
                    parameters["clicks"]["S"].capitalize(),
                    parameters["keys"],
                )

    return txtInst
