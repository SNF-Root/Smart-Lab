# Smart Lab

## Overview

The Tool-Data repository is designed to manage and organize data related to various tools used in our projects. This includes tool specifications, usage data, maintenance logs, and other relevant information. The repository aims to provide a centralized, easily accessible location for all tool-related data, facilitating better management and decision-making.


![SmartLab_Flowchart(1)](https://github.com/SNF-Root/Tool-Data/assets/114797850/f6bc6ff8-6643-45f8-8177-fc998c0e0d87)



## Table of Contents
- [Getting Started](#getting-started)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Getting Started

To get started with the Tool-Data repository, clone the repository to your local machine and follow the setup instructions below.

### Prerequisites

- `Git`
- `Python3` (version 3.6 or higher)
- `SSH` **PASSWORDLESS** setup on all hosts (use `OpenSSH` on Windows machines)
- `Rclone` setup on collector computer with cloud storage of choice

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/SNF-Root/Tool-Data.git
   ```
2. Navigate to the repository directory:
   ```sh
   cd Tool-Data
   ```
3. Create and run the setup `startvenv.sh`:
   ```sh
   chmod +x startvenv.sh
   source ./startvenv.sh
   ```
   This will automatically ensure all the requirements are installed, enter a virtual environment, and run the whole program. From here you can add host machines to the program and add your Rclone root using the included setup tool.

## Usage

### Setting Up

To set up the program at any time, use the `setupGUI.py` script. This script will open a GUI that will guide you to adding new machines/hosts to the existing list.

```sh
python3 scripts/setupGUI.py
```

### Editing Existing Machine Entries

To edit the entries already saved, navigate to the `ansible/hosts.yml` file and feel free to add/edit new/existing host information using the same format.

### View Local Output Data

To view the output files of a specific machine stored locally on the collector, navigate to the `src/Machines/Machine-Of-Your-Choice/data` directory. There you will find directories labeled `Output_Plots` and `Output_Text` that contain graphs and reports respectively.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please contact the project maintainers at:
- **Andrew Chang**: ajchang@ucsb.edu
