from src.Machines.Savannah.Pressure import Pressure
from src.Machines.Savannah.Heating import Heating
from src.uploader import Uploader

from datetime import datetime
import timeit
import os
import shutil

# Iterates through all Savannah Machines and runs all algorithms
class Savannah:
    # Constructor
    def __init__(self):
        pass

    
    # Changes the name of a file
    # specifically for renaming raw files
    def changeName(self, filepath, append):
        # RENAME FILE
        # CHANGE FILE PATH TO LINUX FORMAT
        filepath = filepath.replace("\\", "/")
        filename = filepath.split("/")
        name = filename[-1]
        newpath = filepath.replace(name, f"({append}) {name}")
        # CHANGE FILE NAME
        try:
            os.rename(filepath, newpath)
        except:
            print("Error: File not found, Rename failed")
            return
        return newpath
    

    def copy_item(self, src, dst):
        """Copy an item (file or directory) from src to dst."""
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)


    def copy_sources_to_new_folder(self, src_items, base_dst_folder):
        """
        Copies the contents of source items (files or folders) to a new folder in base_dst_folder.
        The new folder is named according to the current date and time.
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


    def copy_folder_contents(self, src_folder1, src_folder2, base_dst_folder):
        """
        Copies the contents of src_folder1 and src_folder2 to a new folder in base_dst_folder.
        The new folder is named according to the current date and time.
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


    # Runs the Pressure and Heating algorithms for all Savannah machines
    def run(self):
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
                    dirname = self.copy_sources_to_new_folder(src_items, f"src/Machines/{machine[0]}/data({machine[1]})/Output_Data")
                    # FIND ROOT DIRECTORY OF CLOUD STORAGE
                    file = open("src/rclone.txt", "r")
                    root = file.readline().strip()
                    if root == "":
                        print("Cloud Storage Not Found, Skipping Upload...")
                        file.close()
                        return
                    file.close()
                    # UPLOAD TO CLOUD STORAGE
                    up = Uploader(f"src/Machines/{machine[0]}/data({machine[1]})/Output_Data/{dirname}", f"{root}/{machine[0]}/{machine[1]}/{dirname}")
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
                    dirname = self.copy_folder_contents(out_plot, out_text, f"src/Machines/{machine[0]}/data({machine[1]})/Output_Data")
                    # FIND ROOT DIRECTORY OF CLOUD STORAGE
                    file = open("src/rclone.txt", "r")
                    root = file.readline().strip()
                    if root == "":
                        print("Cloud Storage Not Found, Skipping Upload...")
                        file.close()
                        return
                    file.close()
                    # UPLOAD TO CLOUD STORAGE
                    up = Uploader(f"src/Machines/{machine[0]}/data({machine[1]})/Output_Data/{dirname}", f"{root}/{machine[0]}/{machine[1]}/{dirname}")
                    up.rclone()


# Main function for testing
def main():
    s = Savannah()
    s.run()


if __name__ == "__main__":
    main()
