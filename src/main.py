import subprocess
import os

from src.uploader import Uploader

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

        for machine in runMachine:
            for i in range(machine.__len__()):
                subprocess.run(f"python3 src/Machines/{machine[0]}/{machine[i]}.py", shell=True)

        
    subdirectories = [name for name in os.listdir('src/Machines') if os.path.isdir(os.path.join('src/Machines', name))]
    print(subdirectories)

    # RCLONE


if __name__ == "__main__":
    main()