from src.Machines.Fiji202.Pressure import Pressure
from src.Machines.Fiji202.Heating import Heating
from src.Machines.Fiji202.Plasma import Plasma
from src.uploader import Uploader

from datetime import datetime
import timeit
import os
import shutil
import hashlib


class Fiji202:
    """
    Iterates through all Fiji202 Machines and runs all algorithms.
    
    Attributes
    ----------
    None

    Methods
    -------
    changeName(filepath, append):
        Changes the name of a file, specifically for renaming raw files.
    copy_item(src, dst):
        Copy an item (file or directory) from src to dst.
    copy_sources_to_new_folder(src_items, base_dst_folder):
        Copies the contents of source items (files or folders) to a new folder in base_dst_folder.
    copy_folder_contents(src_folder1, src_folder2, base_dst_folder):
        Copies the contents of src_folder1 and src_folder2 to a new folder in base_dst_folder.
    verify_transfer(dataPath):
        Verifies that the transfer of source items to the destination folder was successful.
    calculate_checksum(dataPath):
        Calculate the checksum of the file contents.
    has_stopped_updating(dataPath, max_no_change_cycles=3):
        Monitor a file for updates and return True if no updates are detected for max_no_change_cycles consecutive cycles.
    run():
        Runs the Pressure, Heating, and Plasma algorithms for all Fiji202 machines
    """
    
    def __init__(self):
        """
        Constructor for the Fiji202 class.
        
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
        Changes the name of a file, specifically for renaming raw files.

            Parameters
            -----------
                filepath: str
                    the path to the file to be renamed
                append: str
                    the string to append to the file name

            Returns
            -------
                newpath: str
                    the new path of the renamed file            
        """
        # RENAME FILE
        name = os.path.basename(filepath)
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
                dirname: str
                    the name of the new folder
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


    def copy_folder_contents(self, name, src_folder1, src_folder2, base_dst_folder):
        """
        Copies the contents of src_folder1 and src_folder2 to a new folder in base_dst_folder.
        The new folder is named according to the current date and time.

            Parameters
            -----------
                src_folder1: str
                    the path to the first source folder
                src_folder2: str
                    the path to the second source folder
                base_dst_folder: str
                    the path to the base destination folder

            Returns
            -------
                dirname: str
                    the name of the new folder
        """
        # Create the new folder name
        dirname = name + "~" + datetime.now().strftime("%m:%d:%Y") + "~" + datetime.now().strftime("%H:%M")
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
                dataPath: str
                    the path to the data folder of the machine
            
            Returns
            -------
                bool: True if the files are synced, False otherwise
        """
        p = Pressure(dataPath)
        h = Heating(dataPath)
        pl = Plasma(dataPath)
        if os.path.basename(p.mostRecent()) == os.path.basename(h.mostRecent()) == os.path.basename(pl.mostRecent()):
            print(f"Machine data files are currently synced on local for data path: {dataPath}")
            return True
        else:
            return False
        
    
    def calculate_checksum(self, dataPath):
        """
        Calculate the checksum of the file contents.
        
            Parameters
            -----------
                file_path: str
                    The path to the file to calculate the checksum for.

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
                file_path: str
                    The path to the file to monitor.
                check_interval: int
                    Time in seconds to wait between checks.
                max_no_change_cycles: int
                    Number of cycles to wait with no changes.

            Returns
            -------
                bool: True if the file stopped updating, False otherwise.
        """
        pFile = Pressure(dataPath).mostRecent()
        hFile = Heating(dataPath).mostRecent()
        plFile = Plasma(dataPath).mostRecent()
        pSum = self.calculate_checksum(pFile)
        hSum = self.calculate_checksum(hFile)
        plSum = self.calculate_checksum(plFile)

        metadataPath = os.path.join(dataPath, "metadata.txt")

        with open(metadataPath, 'a+') as file:
            file.write(pSum + "\n")
            file.write(hSum + "\n")
            file.write(plSum + "\n")

        with open(metadataPath, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
            if len(lines) < (3 * max_no_change_cycles):
                return False
            lastCheck = lines[(-3 * max_no_change_cycles):]
        print("Last 9 Checksums: ", lastCheck)
        print("[DEBUG] Pressure Checksum: ", pSum)
        print("[DEBUG] Heating Checksum: ", hSum)
        print("[DEBUG] Plasma Checksum: ", plSum)
        print("[DEBUG] Num of Matching Pressure Checksums: ", lastCheck.count(pSum))
        print("[DEBUG] Num of Matching Heating Checksums: ", lastCheck.count(hSum))
        print("[DEBUG] Num of Matching Plasma Checksums: ", lastCheck.count(plSum))
        if (lastCheck.count(pSum) == max_no_change_cycles) and (lastCheck.count(hSum) == max_no_change_cycles) and (lastCheck.count(plSum) == max_no_change_cycles):
            with open(metadataPath, 'w') as file:
                file.write("")
            return True
        else:
            return False


    def run(self):
        """
        Runs the Pressure, Heating, and Plasma algorithms for all Fiji202 machines and uploads the results to the cloud storage.

            Parameters
            -----------
                None
            
            Returns
            -------
                None
        """
        # RUN ALGS
        start = timeit.default_timer()
        file = open(os.path.join("src", "register.txt"), "r")
        runMachine = []
        raw = []
        for line in file:
            m = tuple(line.strip().split())
            if m[0] == "Fiji202":
                runMachine.append(m)
                for i in range(len(m)):
                    if m[i] == "raw":
                        raw.append(True)
                    else:
                        raw.append(False)
        file.close()
        # Raw file handling
        for machine in runMachine:
            dataPath = os.path.join("src", "Machines", f"{machine[0]}", f"data({machine[1]})")

            if not self.has_stopped_updating(dataPath):
                print(f"[NOTICE]: Machine data files are still updating OR awaiting new files\n skipping algs for data path: {dataPath}")
                continue
            if not self.verify_transfer(dataPath):
                print(f"[WARNING]: Machine data files are NOT synced on local\n skipping algs for data path: {dataPath}")
                continue

            p = Pressure(dataPath)
            h = Heating(dataPath)
            pl = Plasma(dataPath)

            # Uploading raw files
            if raw[runMachine.index(machine)]:
                newp = p.runRaw()
                newh = h.runRaw()
                newpl = p.runRaw()
                # If new raw files are found, change their names and upload them
                if newp and newh and newpl:
                    newp = self.changeName(newp, "Pressure")
                    newh = self.changeName(newh, "Heating")
                    newpl = self.changeName(newpl, "Plasma")
                    src_items = [newp, newh, newpl]
                    dirname = self.copy_sources_to_new_folder(src_items,
                                                              os.path.join(dataPath, "Output_Data"))
                    file = open(os.path.join("src", "rclone.txt"), "r")
                    root = file.readline().strip()
                    if root == "":
                        print("Cloud Storage Not Found, Skipping Upload...")
                        file.close()
                        return
                    file.close()
                    # UPLOAD TO CLOUD STORAGE
                    up = Uploader(os.path.join(dataPath, "Output_Data", f"{dirname}"),
                                    os.path.join(root, machine[0], machine[1], dirname))
                    up.rclone()
            # Uploading normal output files
            else:
                newp = p.run()
                newh = h.run()
                newpl = pl.run()
                stop = timeit.default_timer()
                print('Data Processing Runtime: ', stop - start)
                if newp and newh and newpl:
                    # ADD DATE TIME TO NEW DIRECTORY NAME
                    out_plot = os.path.join(dataPath, "Output_Plots")
                    out_text = os.path.join(dataPath, "Output_Text")
                    dirname = self.copy_folder_contents(newh, out_plot, out_text,
                                                        os.path.join(dataPath, "Output_Data"))
                    # FIND ROOT DIRECTORY OF CLOUD STORAGE
                    file = open(os.path.join("src", "rclone.txt"), "r")
                    root = file.readline().strip()
                    if root == "":
                        print("Cloud Storage Not Found, Skipping Upload...")
                        file.close()
                        return
                    file.close()
                    # UPLOAD TO CLOUD STORAGE
                    up = Uploader(os.path.join(dataPath, "Output_Data", f"{dirname}"),
                                    os.path.join(root, machine[0], machine[1], dirname))
                    up.rclone()


# Main function for testing
def main():
    f = Fiji202()
    f.run()


if __name__ == "__main__":
    main()
