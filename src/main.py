import subprocess
import os
import timeit
import datetime

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

    try:
        result = subprocess.run(ansible_command, cwd=current_directory, capture_output=True, text=True)
        print('Errors:', result.stderr)
        print('Output:', result.stdout)
    except Exception as e:
        raise e


    # Loops through all machines registered in the register.txt file
    start = timeit.default_timer()
    with open('src/register.txt', 'r') as file:
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
                    subprocess.run(f"python3 src/Machines/{machine[0]}/{machine[0]}.py", shell=True)
                    print("--------------------------------------- + \n")
                    print(f"Finished {machine[0]} at {datetime.now().strftime("%m:%d:%Y") + "~" + datetime.now().strftime("%H:%M:%S")} + \n")
                    print("---------------------------------------")
                    donepile.append(machine[0])
                except Exception as e:
                    raise e
                
    file.close()
    stop = timeit.default_timer()
    print('Runtime of Algs: ', stop - start)


if __name__ == "__main__":
    main()