import os
import shutil
import glob
from datetime import datetime

from Pressure import Pressure
from Heating import Heating

import time

dir_path = "/Users/andrew/Library/CloudStorage/GoogleDrive-ajchang@ucsb.edu/My Drive/SNF Data/Savannah Data"
newdir= ""
currFile = "foobar"

# Uploads the files to the Google Drive
def upload():
    newdir = dir_path + "/" + datetime.now().strftime("%H:%M:%S") + " | " + datetime.now().strftime("%m:%d:%Y")
    os.makedirs(newdir, exist_ok=True)
    shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/Precursor Heating Data.png", newdir)
    shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/PressureData.png", newdir)
    shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/Non-Precursor Heating Data.png", newdir)
    shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Text/Pressure Report.txt", newdir)
    shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Text/Heating Report.txt", newdir)
    print("Upload Complete")


# main loop of the program
def loop():
    global currFile
    while True:
        list_of_files = glob.glob("/Users/andrew/Desktop/SNF Projects/Tool-Data/Heating-Data/*")
        latest_file = max(list_of_files, key=os.path.getctime)

        if (currFile == None) or (latest_file != currFile):
            currFile = latest_file
            print("New File Detected")
            upload()
        time.sleep(2)

def main():
    loop()
    # time.sleep(20)
    # os.remove(newdir)
    

if __name__ == "__main__":
    main()