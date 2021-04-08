from psychopy import gui, os
import datetime as dt

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
