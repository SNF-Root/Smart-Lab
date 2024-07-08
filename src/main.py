import subprocess
import os
from Uploader import Uploader

def main():
    # ANSIBLE
    print("This is the loop main")
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    ansible_command = ['ansible-playbook', '-i', 'ansible/hosts.yml', 'ansible/playbook.yml']

    result = subprocess.run(ansible_command, cwd=parent_directory, capture_output=True, text=True)
    print('Errors:', result.stderr)




    # RCLONE
    

if __name__ == "__main__":
    main()