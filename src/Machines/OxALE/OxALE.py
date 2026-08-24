from src.Machines.OxALE.Job import Job
from src.uploader import Uploader
from src.Machines.BaseClasses.Runner_Base import Runner_Base

import timeit
import os


class OxALE(Runner_Base):
    """
    Iterates through all Ox-ALE (Oxford Instruments Cobra ALE, PTIQ control software)
    machines registered in register.txt and runs the Job algorithm for each of them.

    Unlike the other machines in this project, Ox-ALE's process history lives in the PTIQ
    software's Jobs.db SQLite database rather than one file per run. Ansible copies the
    tool's PTIQ/Databases/Jobs.db into this machine's Databases-Data folder, and the Job
    algorithm reads the most recently completed job out of it.

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
    copy_folder_contents(name, src_folder1, src_folder2, base_dst_folder)
        Copies the contents of src_folder1 and src_folder2 to a new folder in base_dst_folder.
    calculate_checksum(file_path)
        Calculate the checksum of the file contents.
    has_stopped_updating(dataPath, max_no_change_cycles=3)
        Monitor Jobs.db for changes and return True if no changes are detected for
        max_no_change_cycles consecutive cycles.
    run()
        Runs the Job algorithm for all Ox-ALE machines and uploads the results to the cloud storage.
    """

    def __init__(self):
        """
        Constructor for the OxALE class.

            Parameters
            -----------
                None

            Returns
            -------
                None
        """
        super().__init__()
        pass


    def has_stopped_updating(self, dataPath, max_no_change_cycles=3):
        """
        Monitor Jobs.db for changes and return True if no changes are detected for
        max_no_change_cycles consecutive cycles. Guards against reading a copy of the
        database mid-sync.

            Parameters
            ----------
                dataPath: str
                    The path to the machine's data folder.
                max_no_change_cycles: int
                    Number of cycles to wait with no changes.

            Returns
            -------
                bool: True if the database stopped changing, False otherwise.
        """
        job = Job(dataPath)
        if not os.path.exists(job.dbPath):
            return False
        dbSum = self.calculate_checksum(job.dbPath)

        metadataPath = os.path.join(dataPath, "metadata.txt")

        with open(metadataPath, 'a+') as file:
            file.write(dbSum + "\n")

        with open(metadataPath, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
            if len(lines) < max_no_change_cycles:
                return False
            lastCheck = lines[-max_no_change_cycles:]
        print("[DEBUG] Num of Matching Jobs.db Checksums: ", lastCheck.count(dbSum))
        if lastCheck.count(dbSum) == max_no_change_cycles:
            with open(metadataPath, 'w') as file:
                file.write("")
            return True
        else:
            return False


    def run(self):
        """
        Runs the Job algorithm for all Ox-ALE machines and uploads the results to the cloud storage.

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
            if m[0] == "OxALE":
                runMachine.append(m)
                for i in range(len(m)):
                    if m[i] == "raw":
                        raw.append(True)
                    else:
                        raw.append(False)
        file.close()

        for machine in runMachine:
            dataPath = os.path.join("src", "Machines", f"{machine[0]}", f"data({machine[1]})")

            if not self.has_stopped_updating(dataPath):
                print(f"[NOTICE]: Machine data files are still updating OR awaiting new files\n skipping algs for data path: {dataPath}")
                continue

            j = Job(dataPath)

            # Uploading raw files
            if raw[runMachine.index(machine)]:
                newj = j.runRaw()
                if newj:
                    newj = self.changeName(newj, "Job")
                    dirname = self.copy_sources_to_new_folder([newj], os.path.join(dataPath, "Output_Data"))
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
                newj = j.run()
                stop = timeit.default_timer()
                print('Data Processing Runtime: ', stop - start)
                if newj:
                    # ADD DATE TIME TO NEW DIRECTORY NAME
                    out_plot = os.path.join(dataPath, "Output_Plots")
                    out_text = os.path.join(dataPath, "Output_Text")
                    dirname = self.copy_folder_contents(newj, out_plot, out_text,
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
    o = OxALE()
    o.run()


if __name__ == "__main__":
    main()
