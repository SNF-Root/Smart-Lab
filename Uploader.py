import os
import shutil
from datetime import datetime

from Pressure import Pressure
from Heating import Heating

import time

dir_path = "/Users/andrew/Library/CloudStorage/GoogleDrive-ajchang@ucsb.edu/My Drive/SNF Data/Savannah Data"
newdir= ""

def upload():
    newdir = dir_path + "/" + datetime.now().strftime("%H;%M;%S") + " | " + datetime.now().strftime("%m:%d:%Y")
    os.makedirs(newdir, exist_ok=True)
    shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/Precursor Heating Data.png", newdir)
    shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/PressureData.png", newdir)
    shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/Non-Precursor Heating Data.png", newdir)
    print("Upload Complete")




def main():
    upload()
    # time.sleep(20)
    # os.remove(newdir)
    

if __name__ == "__main__":
    main()