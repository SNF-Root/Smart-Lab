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
    subdirectories = [name for name in os.listdir('src/Machines') if os.path.isdir(os.path.join('src/Machines', name))]
    print(subdirectories)

    # RCLONE


if __name__ == "__main__":
    main()