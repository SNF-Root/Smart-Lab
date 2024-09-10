from src.Machines.MVD.Pressure import Pressure
from src.Machines.MVD.Heating import Heating
from src.uploader import Uploader
from src.Machines.BaseClasses.Runner_Base import Runner_Base

import timeit
import os


class MVD(Runner_Base):
    """
    Iterates through all MVD Machines and runs all algorithms.

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
        Runs the Pressure and Heating algorithms for all MVD machines and uploads the results to the cloud storage.
    """

    def __init__(self):
        """
        Constructor for the MVD class.

            Parameters
            -----------
                None
            
            Returns
            -------
                None
        """
        super().__init__()
        pass


    def verify_transfer(self, dataPath):
        """
        Verifies that the transfer of source items to the destination folder was successful.

            Parameters
            -----------
                dataPath: str
                    the path to the data folder for the machine

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
        pSum = self.calculate_checksum(pFile)
        hSum = self.calculate_checksum(hFile)

        metadataPath = os.path.join(dataPath, "metadata.txt")

        with open(metadataPath, 'a+') as file:
            file.write(pSum + "\n")
            file.write(hSum + "\n")

        with open(metadataPath, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
            if len(lines) < (2 * max_no_change_cycles):
                return False
            lastCheck = lines[(-2 * max_no_change_cycles):]
        print("Last 6 Checksums: ", lastCheck)
        print("[DEBUG] Pressure Checksum: ", pSum)
        print("[DEBUG] Heating Checksum: ", hSum)
        print("[DEBUG] Num of Matching Pressure Checksums: ", lastCheck.count(pSum))
        print("[DEBUG] Num of Matching Heating Checksums: ", lastCheck.count(hSum))
        if (lastCheck.count(pSum) == max_no_change_cycles) and (lastCheck.count(hSum) == max_no_change_cycles):
            with open(metadataPath, 'w') as file:
                file.write("")
            return True
        else:
            return False


    def run(self):
        """
        Runs the Pressure and Heating algorithms for all MVD machines and uploads the results to the cloud storage.

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
            if m[0] == "MVD":
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
            # Uploading normal output files
            else:
                newp = p.run()
                newh = h.run()
                stop = timeit.default_timer()
                print('Data Processing Runtime: ', stop - start)
                if newp and newh:
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


def main():
    m = MVD()
    m.run()


if __name__ == "__main__":
    main()