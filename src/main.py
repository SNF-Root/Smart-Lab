import subprocess
import os

from src.uploader import Uploader

def main():
    # ANSIBLE
    print("This is the loop main")
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    ansible_command = ['ansible-playbook', '-i', 'ansible/hosts.yml', 'ansible/playbook.yml']

    result = subprocess.run(ansible_command, cwd=parent_directory, capture_output=True, text=True)
    print('Errors:', result.stderr)


    # Loops through all machines registered in the register.txt file
    with open('src/register.txt', 'r') as file:
        runMachine = []
        for line in file:
            values = line.strip().split()
            runMachine.append(tuple(values))

        for machine in runMachine:
            # subprocess.run(f"pwd", shell=True)
            # MAYBE CHANGE THIS TO CALLING MAIN FUNC INSTEAD OF RUNNING THE FILE
            subprocess.run(f"python3 src/Machines/{machine[0]}/{machine[1]}", shell=True)

        
    # subdirectories = [name for name in os.listdir('src/Machines') if os.path.isdir(os.path.join('src/Machines', name))]
    # print(subdirectories)


if __name__ == "__main__":
    main()