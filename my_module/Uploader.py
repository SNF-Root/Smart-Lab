import os
import shutil
import glob
import subprocess
from datetime import datetime
import paramiko
import getpass

# from os import join, dirname
from dotenv import load_dotenv
from scp import SCPClient
from Pressure import Pressure
from Heating import Heating

import time

dir_path = "/Users/andrew/Library/CloudStorage/GoogleDrive-ajchang@ucsb.edu/My Drive/SNF Data/Savannah Data"
newdir= ""
currFile = "foobar"



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


# main loop of the program
# def loop():
#     global currFile
#     while True:
#         list_of_files = glob.glob("/Users/andrew/Desktop/SNF Projects/Tool-Data/Heating-Data/*")
#         latest_file = max(list_of_files, key=os.path.getctime)

#         if (currFile == None) or (latest_file != currFile):
#             currFile = latest_file
#             print("New File Detected")
#             # upload()
#             rclone()
#         time.sleep(2)



def rclone():
    subprocess.run("rclone copy \"Tool-Data/data/Output_Text\" SNF-Root-Test:Output_Text --progress", shell=True)
    # subprocess.run("rclone copy \"/Users/andrew/Desktop/SNF Projects/Tool-Data/data/Output_Plots\" SNF-Root-Test:Output_Plots --progress", shell=True)
    return


# def runparamiko(passkey):
#     ssh_client = paramiko.SSHClient()
#     ssh_client.connect(hostname=host, username=user, password=passkey)
#     return


def create_ssh_client(host, port, username, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, username, password)
    return client



def transfer_file(ssh_client, local_file, remote_path):
    with SCPClient(ssh_client.get_transport()) as scp:
        scp.put(local_file, remote_path, recursive=True)


def prompt_for_password():
    password = getpass.getpass("Enter your password: ")
    print("Password entered successfully.")
    return password


def main():
    host = "10.32.74.194"
    user = "andrew"
    passkey = ""
    port = 22
    local_path = "Tool-Data/data/Output_Plots"
    remote_path = "/Users/andrew/Desktop/"
    # env_path = "/Users/andrew/Desktop/SNF Projects/Tool-Data/.env"


    # with open(env_path, "r") as file:
    #     file.write(f"PASSKEY={prompt_for_password()}")

    load_dotenv()
    passkey = os.getenv("PASSKEY")


    ssh_client = create_ssh_client(host, port, user, passkey)
    transfer_file(ssh_client, local_path, remote_path)
    ssh_client.close()

    # runparamiko(passkey)
    # rclone()
    # time.sleep(20)
    # os.remove(newdir)
    

if __name__ == "__main__":
    main()