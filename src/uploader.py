import os
import shutil
import glob
import subprocess
from datetime import datetime
# import paramiko
import getpass

# from os import join, dirname
# from dotenv import load_dotenv
# from scp import SCPClient
# from src.Machines.Savannah.Pressure import Pressure
# from src.Machines.Savannah.Heating import Heating

import time
    # Uploads the files to the Google Drive
    # def upload():
    #     newdir = dir_path + "/" + datetime.now().strftime("%H:%M:%S") + " | " + datetime.now().strftime("%m:%d:%Y")
    #     os.makedirs(newdir, exist_ok=True)
    #     shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/Precursor Heating Data.png", newdir)
    #     shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/PressureData.png", newdir)
    #     shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/Non-Precursor Heating Data.png", newdir)
    #     shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Text/Pressure Report.txt", newdir)
    #     shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Text/Heating Report.txt", newdir)
    #     print("Upload Complete")


# Class that uploads most recent file from a directory to Google Drive
class Uploader:

    # Constructor
    # dir_path: the path to the directory that contains the files to be uploaded local
    # drive_path: the path to the Google Drive folder where the files will be uploaded
    def __init__(self, dir_path, drive_path):
        self.dir_path = dir_path
        self.drive_path = drive_path
        self.newdir = ""
        self.currFile = "foobar"


    # Uploads the files to the Google Drive using rclone terminal command
    def rclone(self):
        subprocess.run(f"rclone copy \"{self.dir_path}\" {self.drive_path} --progress", shell=True)
        return


def main():
    up = Uploader("src/Machines/Savannah/data/Output_Text", "SNF-Root-Test:Home")
    up.rclone()

    
if __name__ == "__main__":
    main()
