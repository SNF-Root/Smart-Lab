import subprocess
import os

from src.uploader import Uploader
from src.Machines.Savannah.Pressure import Pressure
from src.Machines.Savannah.Heating import Heating

def main():
    # ANSIBLE
    # print("This is the loop main")
    # current_directory = os.getcwd()
    # parent_directory = os.path.dirname(current_directory)
    # ansible_command = ['ansible-playbook', '-i', 'ansible/hosts.yml', 'ansible/playbook.yml']

    # result = subprocess.run(ansible_command, cwd=parent_directory, capture_output=True, text=True)
    # print('Errors:', result.stderr)


    # For machine in machines:
    #  if machine is registered, run appropriate scripts on data
    #  use uploader class to upload data to Google Drive
    with open('src/register.txt', 'r') as file:
        runMachine = []
        for line in file:
            values = line.strip().split()
            runMachine.append(tuple(values))

        # for machine in runMachine:
        #     subprocess.run(f"cd src/Machines/{machine[0]}", shell=True)
        #     print("1\n")
        #     subprocess.run(f"pwd", shell=True)
        #     for i in range(1, machine.__len__()):
        #         subprocess.run(f"python3 src/Machines/{machine[0]}/{machine[i]}", shell=True)
        #         print("2\n")
        #     subprocess.run(f"cd ../../..", shell=True)
        #     print("3\n")

        p = Pressure("src/Machines/Savannah/data/Pressure-Data")
        h = Heating("src/Machines/Savannah/data/Heating-Data")
        p.run()
        h.run()


        
    subdirectories = [name for name in os.listdir('src/Machines') if os.path.isdir(os.path.join('src/Machines', name))]
    print(subdirectories)

    # RCLONE


if __name__ == "__main__":
    main()