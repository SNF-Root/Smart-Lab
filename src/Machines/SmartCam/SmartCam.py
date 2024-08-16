from src.Machines.SmartCam.Camera import Camera
from src.uploader import Uploader

from datetime import datetime
import timeit
import os
import shutil


class SmartCam:
    """
    Iterates through the SmartCam machines in the register.txt file and processes the data.
    
    Attributes
    ----------
    None

    Methods
    -------
    copy_item(src, dst):
        Copy an item (file or directory) from src to dst.
    copy_sources_to_new_folder(src_items, base_dst_folder):
        Copies the contents of source items (files or folders) to a new folder in base_dst_folder.
    run():
        Runs the SmartCam machine processing algorithm.
    """
    
    def __init__(self):
        """
        Constructor for the SmartCam class
        
            Parameters
            -----------
                None
            
            Returns
            -------
                None
        """
        pass

    
    def copy_item(self, src, dst):
        """
        Copy an item (file or directory) from src to dst.
        
            Parameters
            -----------
                src: str
                    the path to the source item
                dst: str
                    the path to the destination item

            Returns
            -------
                None
        """
        if os.path.isdir(src):
            try:
                shutil.copytree(src, dst, dirs_exist_ok=True)
            except FileNotFoundError as e:
                raise e
        else:
            try:
                shutil.copy2(src, dst)
            except FileNotFoundError as e:
                raise e


    def copy_sources_to_new_folder(self, src_items, base_dst_folder):
        """
        Copies the contents of source items (files or folders) to a new folder in base_dst_folder.
        The new folder is named according to the current date and time.

            Parameters
            -----------
                src_items: list
                    a list of paths to the source items
                base_dst_folder: str
                    the path to the base destination folder

            Returns
            -------
                str: the name of the new folder created
        """
        # Create the new folder name
        dirname = datetime.now().strftime("%m:%d:%Y") + "~" + datetime.now().strftime("%H:%M")
        dst_folder = os.path.join(base_dst_folder, dirname)
        
        try:
            # Create destination folder
            os.makedirs(dst_folder, exist_ok=True)
            
            # Copy the contents of the source items to the destination folder
            for src in src_items:
                if not os.path.exists(src):
                    raise FileNotFoundError(f"Source item '{src}' does not exist.")
                
                item_name = os.path.basename(src)
                dst_item = os.path.join(dst_folder, item_name)
                self.copy_item(src, dst_item)
            
            print(f"Contents of {src_items} have been copied to '{dst_folder}'.")
            return dirname

        except Exception as e:
            print(f"An error occurred: {e}")
            raise e


    def run(self):
        # RUN ALGS, find all SmartCam machines in register.txt
        start = timeit.default_timer()
        file = open("src/register.txt", "r")
        runMachine = []
        for line in file:
            m = tuple(line.strip().split())
            if m[0] == "SmartCam":
                runMachine.append(m)

        file.close()
        # Raw file handling
        for machine in runMachine:
            dataPath = f"src/Machines/{machine[0]}/data({machine[1]})"

            c = Camera(dataPath)
            newc = c.run()
            if newc == None:
                return
            stop = timeit.default_timer()
            print('Data Processing Runtime: ', stop - start)

            dirname = dataPath + "/Output_Text"

            file = open("src/rclone.txt", "r")
            root = file.readline().strip()
            if root == "":
                print("Cloud Storage Not Found, Skipping Upload...")
                file.close()
                return
            file.close()
            # UPLOAD TO CLOUD STORAGE
            up = Uploader(f"src/Machines/{machine[0]}/data({machine[1]})/Output_Data/{dirname}",
                            f"{root}/{machine[0]}/{machine[1]}/{dirname}")
            up.rclone()


# Main function for testing
def main():
    s = SmartCam()
    s.run()


if __name__ == '__main__':
    main()