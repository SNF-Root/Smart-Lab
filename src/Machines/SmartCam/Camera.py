import os
from datetime import datetime


class Camera:
    def __init__(self, dataPath):

        self.dataPath = dataPath
        self.cameraFilePath = ""
        self.cameraDirPath = ""
        self.dir_list = []
        
    
    def readDir(self):
        """
        Reads through directory and prints out how many of each recipe is in the directory.

            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        path = self.cameraDirPath
        try:
            self.dir_list = os.listdir(path)
        except NotADirectoryError:
            print("DIRECTORY NOT FOUND, PROCESS ABORTED AT: \"src/Machines/SmartCam/Camera.py\" AT METHOD: readDir(). \n Hint: Try putting in a valid directory path.")
            raise NotADirectoryError


    def mostRecent(self):
        """
        Returns the most recent file in the directory.
        Calls readDir() to load all files in directory into a list
            
            Parameters
            ----------
                None
            
            Returns
            -------
                times[-1][0] (str): the file path of the most recent file
        """
        # tuples of (filename, creation time)
        self.readDir()
        times = []
        listFiles = self.dir_list
        for i in listFiles:
            filepath = self.cameraDirPath + "/" + i
            # get creation time
            times.append((filepath, os.path.getctime(filepath)))
        if times.__len__() == 0:
            print("NO FILES FOUND, PROCESS ABORTED AT: \"src/Machines/SmartCam/Camera.py\" AT METHOD: mostRecent(). \n Hint: Ansible may have trouble copying files.")
            return None
        # sort by creation time
        times.sort(key=lambda x: x[1])
        return times[-1][0]
    

    def initialize(self):
        """
        Initializes the Heating Data Stack with the most recent files
        Calls mostRecent() to grab the most recent file and read it

            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        self.cameraFilePath = self.mostRecent()
        print("Initialized Camera Data Stack")
        

    def run(self):
        """
        Returns the file path of the file to be uploaded

            Parameters
            ----------
                None

            Returns
            -------
                cameraFilePath (str): the file path of the new data
        """
        self.initialize()
        return self.cameraFilePath


# Main function to test the Camera class
def main():
    c = Camera()
    c.run()
    return


if __name__ == '__main__':
    main()