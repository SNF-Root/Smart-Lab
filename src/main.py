import subprocess
import os


def main():
    """
    Main function to run the entire data collection, processing, and uploading pipeline

        Parameters
        ----------
            None

        Returns
        -------
            None
    """
    # ANSIBLE
    current_directory = os.getcwd()
    ansible_command = ['ansible-playbook', '-i', 'ansible/hosts.yml', 'ansible/playbook.yml']

    result = subprocess.run(ansible_command, cwd=current_directory, capture_output=True, text=True)
    print('Errors:', result.stderr)


    # Loops through all machines registered in the register.txt file
    with open('src/register.txt', 'r') as file:
        runMachine = []
        for line in file:
            values = line.strip().split()
            runMachine.append(tuple(values))

        # Each machine named .py file will process all of that type of machine, we don't want to run the same machine twice
        donepile = []
        for machine in runMachine:
            # subprocess.run(f"pwd", shell=True)
            # MAYBE CHANGE THIS TO CALLING MAIN FUNC INSTEAD OF RUNNING THE FILE
            if machine[0] not in donepile:
                subprocess.run(f"python3 src/Machines/{machine[0]}/{machine[0]}.py", shell=True)
                donepile.append(machine[0])

    file.close()
    # subdirectories = [name for name in os.listdir('src/Machines') if os.path.isdir(os.path.join('src/Machines', name))]
    # print(subdirectories)


if __name__ == "__main__":
    main()