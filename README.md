# Smart Lab

## Overview

The Smart Lab Project is a lab data management software package designed to collect, process, and store data related to various tools used in nanofabrication facilities. The primary goal of this project is to make hard-to-reach data more accessible and readable in a coherent database for better management, monitoring, and decision-making.

This software package includes built-in methods and algorithms for commonly used nanofabrication machines, allowing users to select which machines they want to retrieve data from. Setup is facilitated through a quick and easy GUI that opens upon program execution, as well as through a script that can be executed at any time.


![SmartLab_Flowchart(1)](https://github.com/SNF-Root/Tool-Data/assets/114797850/f6bc6ff8-6643-45f8-8177-fc998c0e0d87)


## Table of Contents
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Packages Used](#packages-used)
- [License](#license)
- [Contact](#contact)

## Getting Started

### Prerequisite Hardware

- **Wireless Access Point (Router)**
   - Set up a private network that only the collector machine and the hosts can connect to
   - Only specific machines can connect to maintain security
> [!IMPORTANT]
> **MUST SET UP STATIC IP ON WIRELESS ACCESS POINT**
- **Linux Computer (Collector Machine)**
   - Set up for dual-homing (able to connect to two networks at once)
   - Any Linux distribution should work (tested on [Ubuntu](https://ubuntu.com/download))

> [!NOTE]
> We use `Linux` as our main OS for this project to ensure customizability and robustness.

### Prerequisite Software

- `Git`
- `Python3` (version 3.6 or higher) with the `tkinter` package installed
- `SSH` **PASSWORDLESS** setup on all hosts (use `OpenSSH` on Windows machines)
   - For security purposes it's best to not store passwords on the program
- `Rclone` setup on collector computer with cloud storage of choice
   - Note down the root with prefered path of your cloud storage

> [!TIP]
> * To install `Python3` on `Linux`, navigate to [this article](https://docs.python-guide.org/starting/install3/linux/)
> * To Set up Passwordless `SSH`, navigate to [this article](https://linuxize.com/post/how-to-setup-passwordless-ssh-login/)
> * To set up `Rclone` for your specific usecase, navigate to [Rclone's Website](https://rclone.org/install/)
>    - Here is the setup for [Rclone Google Drive](https://rclone.org/drive/)

> [!NOTE]
> The project is currently not built for `Python2`, these features may be added in the future.

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/SNF-Root/Smart-Lab.git
   ```
2. Navigate to the repository directory:
   ```sh
   cd Smart-Lab
   ```
3. Create and run the setup `startvenv.sh`:
   ```sh
   chmod +x startvenv.sh
   source ./startvenv.sh
   ```
   
> This will automatically ensure all the requirements are installed, enter a virtual environment, and run the whole program. From here you can add host machines to the program and add your Rclone root using the included setup tool.

## Usage

### Setting Up

To set up the program at any time, use the `setupGUI.sh` script. This script will open a GUI that will guide you to adding new machines/hosts to the existing list.

```sh
chmod +x setupGUI.sh
source ./setupGUI.sh
```

### Editing Existing Machine Entries

* To edit the entries already saved, navigate to the `ansible/hosts.yml` file and feel free to edit existing host information using the same format.
* For each entry edited in `ansible/hosts.yml`, edit the same entry in `src/register.txt` using the same format.
> [!CAUTION]
> **Users editing the files directly instead of using the GUI must be exact about formatting and syntax to ensure program integrity!**

### View Local Output Data

To view the output files of a specific machine stored locally on the collector, navigate to the `src/Machines/Machine-Type/(data)Machine-Name` folder. There you will find a folder name `Output_Data` which contains all the full reports created by that machine.

## Packages Used

### [Ansible](https://www.ansible.com/)

> Ansible is a powerful open source package that is great for automation of tasks related to accessing a fleet of host machines
* We use ansible becuase we can have dozens of machines of all different kinds in the lab
* Ansible is written in a user friendly way which makes coding and debugging easier

### [Rclone](https://rclone.org/)
> Rclone is an open source package that is able to transfer files to and from cloud storage options
* We use Rclone to take local files and upload them so users can access them anywhere at anytime
* Rclone also has the function to sync files stored on local to the cloud, which is useful for data synchronicity

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please contact the project maintainers at:
- **Andrew Chang**: ajchang@ucsb.edu
