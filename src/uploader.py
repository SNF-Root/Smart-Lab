import subprocess

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
