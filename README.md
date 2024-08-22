# Smart Lab

## Overview

The Smart Lab Project is a lab data management software package designed to collect, process, and store data from various tools used in nanofabrication facilities. The primary goal of this project is to make hard-to-reach data more accessible and readable in a coherent database for better management, monitoring, and decision-making.

This software package includes built-in methods and algorithms for commonly used nanofabrication machines, allowing users to select which machines they want to retrieve data from. Setup is facilitated through a quick and easy GUI that opens upon program execution, as well as through a script that can be executed at any time.

![SmartLab_Flowchart](https://github.com/user-attachments/assets/f7f04656-9825-4226-8dd7-7646ddcf4272)

## Table of Contents
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Supported Machines](#supported-machines)
- [Packages Used](#packages-used)
- [License](#license)
- [Contact](#contact)

## Getting Started

### Prerequisite Hardware :hammer_and_wrench:

- **Wireless Access Point (Router)**
  - Set up a private network that only the collector machine and the hosts can connect to.
  - Only specific machines can connect to maintain security.
> [!IMPORTANT]
> **Must set up static IP on the wireless access point!**

- **Linux Computer (Collector Machine)**
  - Set up for dual-homing (able to connect to two networks at once).
    - One connection to the wireless access point, other to outbound internet (wired connection).
  - Any Linux distribution should work (tested on [Ubuntu](https://ubuntu.com/download)).

> [!NOTE]
> We use Linux as our preferred OS for this project to ensure customizability and robustness.

### Prerequisite Software :floppy_disk:

- `Git`
- `Python 3` (version 3.6 or higher) with the `tkinter` package installed.
- `SSH` **PASSWORDLESS** setup on all hosts (use `OpenSSH` on Windows machines).
  - For security purposes, it's best not to store passwords in the program.
- `Rclone` setup on the collector computer with the cloud storage of your choice.
  - Note down the root and preferred path of your cloud storage.

> [!TIP]
> * To install Python 3 on Linux, navigate to [this article](https://docs.python-guide.org/starting/install3/linux/).
> * To set up passwordless SSH, navigate to [this article](https://linuxize.com/post/how-to-setup-passwordless-ssh-login/).
> * To set up Rclone for your specific use case, navigate to [Rclone's website](https://rclone.org/install/).
>   - Here is the setup for [Rclone with Google Drive](https://rclone.org/drive/).


### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/SNF-Root/Smart-Lab.git
   ```
2. Navigate to the repository directory:
   ```sh
   cd Smart-Lab
   ```
3. Create and run the setup script `startvenv.sh`:
   ```sh
   chmod +x startvenv.sh
   source ./startvenv.sh
   ```

> This will automatically ensure all the requirements are installed, enter a virtual environment, and run the whole program. From here, you can add host machines to the program and add your Rclone root using the included setup tool.

## Usage

### Setting Up

To set up the program at any time, use the `setupGUI.sh` script. This script will open a GUI that will guide you through adding new machines/hosts to the existing list.

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

To view the output files of a specific machine stored locally on the collector, navigate to the `src/Machines/Machine-Type/(data)Machine-Name` folder. There you will find a folder named `Output_Data` which contains all the full reports created by that machine.

## Supported Machines

| Machine Name | Supported Algorithms | Support Status |
| --- | :---: | :---: |
| Cambridge Savannah ALD | Pressure, Heating | Beta |
| Veeco Fiji 202 ALD | Pressure, Heating, Plasma (RF) | Beta |

## Packages Used

### [Ansible](https://www.ansible.com/)

> Ansible is a powerful open-source package that is great for automating tasks related to accessing a fleet of host machines.
* We use Ansible to easily manage dozens of machines of all different kinds in the lab.
* Ansible is written in a user-friendly way, making coding and debugging easier.

### [Rclone](https://rclone.org/)
> Rclone is an open-source package that is able to transfer files to and from cloud storage options.
* We use Rclone to take local files and upload them so users can access them anywhere at any time.
* Rclone also has the function to sync files stored locally to the cloud, which is useful for data synchronicity.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please contact the project maintainers at:
- **Andrew Chang**: ajchang@ucsb.edu
