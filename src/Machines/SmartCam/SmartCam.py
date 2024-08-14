from src.Machines.SmartCam.Camera import Camera
from src.uploader import Uploader

from datetime import datetime
import timeit
import os
import shutil


class SmartCam:
    
    def __init__(self):
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
        # RUN ALGS
        start = timeit.default_timer()
        file = open("src/register.txt", "r")
        runMachine = []
        raw = []
        for line in file:
            m = tuple(line.strip().split())
            if m[0] == "SmartCam":
                runMachine.append(m)
                # if m[4] == "raw":
                #     raw.append(True)
                # else:
                #     raw.append(False)
        file.close()
        # Raw file handling
        for machine in runMachine:
            dataPath = f"src/Machines/{machine[0]}/data({machine[1]})"

            # if not self.has_stopped_updating(dataPath):
            #     print(f"[NOTICE]: Machine data files are still updating OR awaiting new files\n skipping algs for data path: {dataPath}")
            #     continue

            # if not self.verify_transfer(dataPath):
            #     print(f"[WARNING]: Machine data files are NOT synced on local\n skipping algs for data path: {dataPath}")
            #     continue

            # p = Pressure(dataPath)
            # h = Heating(dataPath)

            # Uploading raw files
            # if raw[runMachine.index(machine)]:
            #     newp = p.runRaw()
            #     newh = h.runRaw()
            #     # If new raw files are found, change their names and upload them
            #     if newp and newh:
            #         newp = self.changeName(newp, "Pressure")
            #         newh = self.changeName(newh, "Heating")
            #         src_items = [newp, newh]
            #         dirname = self.copy_sources_to_new_folder(src_items,
            #                                                   f"src/Machines/{machine[0]}/data({machine[1]})/Output_Data")
            #         # FIND ROOT DIRECTORY OF CLOUD STORAGE
            #         file = open("src/rclone.txt", "r")
            #         root = file.readline().strip()
            #         if root == "":
            #             print("Cloud Storage Not Found, Skipping Upload...")
            #             file.close()
            #             return
            #         file.close()
            #         # UPLOAD TO CLOUD STORAGE
            #         up = Uploader(f"src/Machines/{machine[0]}/data({machine[1]})/Output_Data/{dirname}",
            #                         f"{root}/{machine[0]}/{machine[1]}/{dirname}")
            #         up.rclone()
            # Uploading normal output files
            # else:

            # newp = p.run()
            # newh = h.run()
            stop = timeit.default_timer()
            print('Data Processing Runtime: ', stop - start)
            # if newp and newh:
            #     # ADD DATE TIME TO NEW DIRECTORY NAME
            #     out_plot = dataPath + "/Output_Plots"
            #     out_text = dataPath + "/Output_Text"
            #     dirname = self.copy_folder_contents(newh, out_plot, out_text,
            #                                         f"src/Machines/{machine[0]}/data({machine[1]})/Output_Data")
            
            # FIND ROOT DIRECTORY OF CLOUD STORAGE

            dirname = dataPath + "Output_Text"

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