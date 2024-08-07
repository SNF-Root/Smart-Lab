from src.Machines.Savannah.Pressure import Pressure
from src.Machines.Savannah.Heating import Heating
from src.uploader import Uploader

from datetime import datetime
import timeit
import os
import shutil
import hashlib


class Savannah:
    """
    Iterates through all Savannah Machines and runs all algorithms.

    Attributes
    ----------
    None

    Methods
    -------
    changeName(filepath, append)
        Changes the name of a file by appending a string to the file name. 
    copy_item(src, dst)
        Copy an item (file or directory) from src to dst.
    copy_sources_to_new_folder(src_items, base_dst_folder)
        Copies the contents of source items (files or folders) to a new folder in base_dst_folder.
    copy_folder_contents(src_folder1, src_folder2, base_dst_folder)
        Copies the contents of src_folder1 and src_folder2 to a new folder in base_dst_folder.
    verify_transfer(dataPath)
        Verifies that the transfer of source items to the destination folder was successful.
    calculate_checksum(file_path)
        Calculate the checksum of the file contents.
    has_stopped_updating(file_path, max_no_change_cycles=3)
        Monitor a file for updates and return True if no updates are detected
        for max_no_change_cycles consecutive cycles.
    run()
        Runs the Pressure and Heating algorithms for all Savannah machines and uploads the results to the cloud storage.
    """

    def __init__(self):
        """
        Constructor for the Savannah class.

            Parameters
            -----------
                None
            
            Returns
            -------
                None
        """
        pass

    
    def changeName(self, filepath, append):
        """
        Changes the name of a file by appending a string to the file name.
            
            Parameters
            -----------
                filepath: str
                    the path to the file to be renamed
                append: str
                    the string to append to the file name
            Returns
            -------
                str
                    the new path to the renamed file
        """
        # RENAME FILE
        filename = filepath.split("/")
        name = filename[-1]
        newpath = filepath.replace(name, f"({append}) {name}")
        # CHANGE FILE NAME
        try:
            os.rename(filepath, newpath)
        except:
            print("Error: File not found, Rename failed")
            raise FileNotFoundError("File not found, Rename failed")
        return newpath
    

    def copy_item(self, src, dst):
        """
        Copy an item (file or directory) from src to dst.
        
            Parameters
            -----------
                src (str): the path to the source item
                dst (str): the path to the destination item

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
                src_items (list): a list of paths to the source items
                base_dst_folder (str): the path to the base destination folder

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


    def copy_folder_contents(self, src_folder1, src_folder2, base_dst_folder):
        """
        Copies the contents of src_folder1 and src_folder2 to a new folder in base_dst_folder.
        The new folder is named according to the current date and time.

            Parameters
            -----------
                src_folder1 (str): the path to the first source folder
                src_folder2 (str): the path to the second source folder
                base_dst_folder (str): the path to the base destination folder
            
            Returns
            -------
                str: the name of the new folder created
        """
        # Create the new folder name
        dirname = datetime.now().strftime("%m:%d:%Y") + "~" + datetime.now().strftime("%H:%M")
        dst_folder = os.path.join(base_dst_folder, dirname)
        
        try:
            # Check if source folders exist
            if not os.path.exists(src_folder1):
                raise FileNotFoundError(f"Source folder '{src_folder1}' does not exist.")
            if not os.path.exists(src_folder2):
                raise FileNotFoundError(f"Source folder '{src_folder2}' does not exist.")
            
            # Create destination folder
            os.makedirs(dst_folder, exist_ok=True)
            
            # Copy the contents of the first source folder to the destination folder
            for item in os.listdir(src_folder1):
                src_item = os.path.join(src_folder1, item)
                dst_item = os.path.join(dst_folder, item)
                
                if os.path.isdir(src_item):
                    shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_item, dst_item)
            
            # Copy the contents of the second source folder to the destination folder
            for item in os.listdir(src_folder2):
                src_item = os.path.join(src_folder2, item)
                dst_item = os.path.join(dst_folder, item)
                
                if os.path.isdir(src_item):
                    shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_item, dst_item)
            
            print(f"Contents of '{src_folder1}' and '{src_folder2}' have been copied to '{dst_folder}'.")
            return dirname

        except Exception as e:
            print(f"An error occurred: {e}")
            raise e


    def verify_transfer(self, dataPath):
        """
        Verifies that the transfer of source items to the destination folder was successful.

            Parameters
            -----------
                dataPath (str): the path to the data folder for the machine

            Returns
            -------
                bool: True if the files are synced, False otherwise
        """
        p = Pressure(dataPath)
        h = Heating(dataPath)
        if os.path.basename(p.mostRecent()) == os.path.basename(h.mostRecent()):
            print(f"Machine data files are currently synced on local for data path: {dataPath}")
            return True
        else:
            return False
        

    def calculate_checksum(self, dataPath):
        """
        Calculate the checksum of the file contents.
        
            Parameters
            -----------
                file_path (str): The path to the file to calculate the checksum for.

            Returns
            -------
                str: The checksum of the file contents.
        """
        with open(dataPath, 'rb') as file:
            file_content = file.read()
            return hashlib.md5(file_content).hexdigest()


    def has_stopped_updating(self, dataPath, max_no_change_cycles=3):
        """
        Monitor a file for updates and return True if no updates are detected
        for max_no_change_cycles consecutive cycles.

            Parameters
            ----------
                file_path (str): The path to the file to monitor.
                check_interval (int): Time in seconds to wait between checks.
                max_no_change_cycles (int): Number of cycles to wait with no changes.

            Returns
            -------
                bool: True if the file stopped updating, False otherwise.
        """
        pFile = Pressure(dataPath).mostRecent()
        hFile = Heating(dataPath).mostRecent()
        pSum = self.calculate_checksum(pFile)
        hSum = self.calculate_checksum(hFile)

        metadataPath = dataPath + "/metadata.txt"

        with open(metadataPath, 'a+') as file:
            file.write(pSum + "\n")
            file.write(hSum + "\n")

        with open(metadataPath, 'r') as file:
            lines = [line for line in file.readlines() if line.strip()]
            if len(lines) < (2 * max_no_change_cycles):
                return False
            lastSix = lines[(-2 * max_no_change_cycles):]
        print("Last 6 Checksums: ", lastSix)
        print("[DEBUG] Num of Matching Pressure Checksums: ", lastSix.count(pSum))
        print("[DEBUG] Num of Matching Heating Checksums: ", lastSix.count(hSum))
        if (lastSix.count(pSum) == max_no_change_cycles) and (lastSix.count(hSum) == max_no_change_cycles):
            with open(metadataPath, 'w') as file:
                file.write("")
            return True
        else:
            return False


    def run(self):
        """
        Runs the Pressure and Heating algorithms for all Savannah machines and uploads the results to the cloud storage.

            Parameters
            -----------
                None
            
            Returns
            -------
                None
        """
        # RUN ALGS
        start = timeit.default_timer()
        file = open("src/register.txt", "r")
        runMachine = []
        raw = []
        for line in file:
            m = tuple(line.strip().split())
            if m[0] == "Savannah":
                runMachine.append(m)
                if m[4] == "raw":
                    raw.append(True)
                else:
                    raw.append(False)
        file.close()
        # Raw file handling
        for machine in runMachine:
            dataPath = f"src/Machines/{machine[0]}/data({machine[1]})"

            if not self.has_stopped_updating(dataPath):
                print(f"[NOTICE]: Machine data files are still updating\n skipping algs for data path: {dataPath}")
                continue
            if not self.verify_transfer(dataPath):
                print(f"[WARNING]: Machine data files are NOT synced on local\n skipping algs for data path: {dataPath}")
                continue

            p = Pressure(dataPath)
            h = Heating(dataPath)
            # Uploading raw files
            if raw[runMachine.index(machine)]:
                newp = p.runRaw()
                newh = h.runRaw()
                # If new raw files are found, change their names and upload them
                if newp and newh:
                    newp = self.changeName(newp, "Pressure")
                    newh = self.changeName(newh, "Heating")
                    src_items = [newp, newh]
                    dirname = self.copy_sources_to_new_folder(src_items,
                                                              f"src/Machines/{machine[0]}/data({machine[1]})/Output_Data")
                    # FIND ROOT DIRECTORY OF CLOUD STORAGE
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
            # Uploading normal output files
            else:
                newp = p.run()
                newh = h.run()
                stop = timeit.default_timer()
                print('Data Processing Runtime: ', stop - start)
                if newp and newh:
                    # ADD DATE TIME TO NEW DIRECTORY NAME
                    out_plot = dataPath + "/Output_Plots"
                    out_text = dataPath + "/Output_Text"
                    dirname = self.copy_folder_contents(out_plot, out_text,
                                                        f"src/Machines/{machine[0]}/data({machine[1]})/Output_Data")
                    # FIND ROOT DIRECTORY OF CLOUD STORAGE
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
    s = Savannah()
    s.run()


if __name__ == "__main__":
    main()
