import subprocess
import os
import timeit
from datetime import datetime

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
    # current_directory = os.getcwd()
    # ansible_command = ['ansible-playbook', '-i', os.path.join('ansible', 'hosts.yml'), os.path.join('ansible', 'playbook.yml')]

    # try:
    #     result = subprocess.run(ansible_command, cwd=current_directory, capture_output=True, text=True)
    #     print('Errors:', result.stderr)
    #     print('Output:', result.stdout)
    # except Exception as e:
    #     raise e


    # Loops through all machines registered in the register.txt file
    start = timeit.default_timer()
    with open(os.path.join('src', 'register.txt'), 'r') as file:
        runMachine = []
        for line in file:
            values = line.strip().split()
            runMachine.append(tuple(values))
        if not runMachine:
            raise Exception("No machines registered in register.txt")

        # Each machine named .py file will process all of that type of machine, we don't want to run the same machine twice
        donepile = []
        for machine in runMachine:
            subprocess.run(f"pwd", shell=True)
            # MAYBE CHANGE THIS TO CALLING MAIN FUNC INSTEAD OF RUNNING THE FILE
            if machine[0] not in donepile:
                try:
                    runner_path = os.path.join('src', 'Machines', machine[0], f"{machine[0]}.py")
                    subprocess.run(f"python3 {runner_path}", shell=True)
                    print("---------------------------------------\n")
                    print(f"Finished {machine[0]} at: " + datetime.now().strftime("%m:%d:%Y") +  "~" + datetime.now().strftime("%H:%M:%S") + "\n")
                    print("---------------------------------------")
                    donepile.append(machine[0])
                except Exception as e:
                    raise e
                
    file.close()
    stop = timeit.default_timer()
    print('Runtime of Algs: ', stop - start)


if __name__ == "__main__":
    main()