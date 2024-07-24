import subprocess


class Uploader:
    """
    Uploader class uploads most recent file from a directory to Google Drive

    Attributes:
    -----------
    dir_path: str
        the path to the directory that contains the files to be uploaded local
    drive_path: str
        the path to the Google Drive folder where the files will be uploaded

    Methods:
    --------
    rclone():
        Uploads the files to the Google Drive using rclone terminal command
    """


    def __init__(self, dir_path, drive_path):
        """
        Constructor for the Uploader class
        
            Parameters
            -----------
                dir_path: str
                    the path to the directory that contains the files to be uploaded local
                drive_path: str
                    the path to the Google Drive folder where the files will be uploaded
            
            Returns
            -------
                None
        """
        self.dir_path = dir_path
        self.drive_path = drive_path
        self.newdir = ""
        self.currFile = "foobar"


    def rclone(self):
        """
        Uploads the files to the Google Drive using rclone terminal command

            Parameters
            -----------
                None
            
            Returns
            -------
                None
        """
        subprocess.run(f"rclone copy \"{self.dir_path}\" {self.drive_path} --progress", shell=True)
        return
    
    def sync(self):
        """
        Syncs the files to the Google Drive using rclone terminal command

            Parameters
            -----------
                None
            
            Returns
            -------
                None
        """
        subprocess.run(f"rclone sync --interactive \"{self.dir_path}\" {self.drive_path} --progress", shell=True)
        return


def main():
    up = Uploader("src/Machines/Savannah/data/Output_Text", "SNF-Root-Test:Home")
    up.rclone()

    
if __name__ == "__main__":
    main()
