import subprocess

def main():
    print("This is the loop main")
    subprocess.run("ansible-playbook -i ansible/hosts.yml ansible/playbook.yml", shell=True)
    

if __name__ == "__main__":
    main()