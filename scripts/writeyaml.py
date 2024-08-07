import os
import yaml


class WriteYaml:
    """
    A class that writes YAML data to the hosts.yml file to add a new host machine

    Attributes:
    -----------
    host: str
        the IP address of the host machine
    user: str
        the username to login to the host machine
    toolname: str
        the name of the tool running on the host machine
    source: str
        the source directory on the host machine
    destination: str
        the destination directory on the host machine

    Methods:
    --------
    write_yaml():
        Writes the YAML data to the hosts.yml file
    add_directory(host, source, destination):
        Adds a new directory mapping to an existing host
    """


    def __init__(self, host, user, toolname="", source="", destination=""):
        """
        Constructor for the WriteYaml class
        
            Parameters
            -----------
                host: str
                    the IP address of the host machine
                user: str
                    the username to login to the host machine
                toolname: str
                    the name of the tool running on the host machine
                source: str
                    the source directory on the host machine
                destination: str
                    the destination directory on the host machine
            
            Returns
            -------
                None
        """
        self.host = host
        self.user = user
        self.toolname = toolname
        self.source = source
        self.destination = destination


    def detect_path_style(self, path):
        """
        Helper: Detects the path style (Windows or Linux) based on the path string
            
            Parameters
            ----------
                str
                    the path string to be analyzed
            
            Returns
            -------
                str
                    the path style (Windows or Linux) or Unknown if not detected
        """
        if '\\' in path and not '/' in path:
            return "Windows"
        elif '/' in path and not '\\' in path:
            return "Linux"
        elif (path.startswith('C:\\') or (len(path) > 2 and path[1] == ':' and path[2] == '\\')):
            return "Windows"
        else:
            return "Unknown"


    def write_yaml(self):
        """
        Writes the YAML data to the hosts.yml file
            
            Parameters
            -----------
                None
            
            Returns
            -------
                None
        """
        # Assuming the script is located in Tool-Data/scripts/
        current_directory = os.path.dirname(__file__)  # Get current script directory
        # Navigate up one level to Tool-Data/
        project_directory = os.path.abspath(os.path.join(current_directory, '..'))

        # Specify the relative path to the ansible directory
        ansible_directory = os.path.join(project_directory, 'ansible')

        # File path within the ansible directory
        file_path = os.path.join(ansible_directory, 'hosts.yml')

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            # File already exists and is not empty
            with open(file_path, 'r') as file:
                existing_data = yaml.safe_load(file)
            file.close()
        else:
            # print(f"File {file_path} does not exist or is empty")
            existing_data = {'all': {'hosts': {}}}  # Initialize empty data

        if 'all' in existing_data and 'hosts' in existing_data['all']:
            last_host_number = len(existing_data['all']['hosts'])
        else:
            last_host_number = 0

        # Increment the host number
        new_host_number = last_host_number + 1
        
        if self.detect_path_style(self.source) == "Windows":
            # Data to write
            new_host_data = {
                f'host{new_host_number}': {
                    'ansible_host': self.host,
                    'ansible_user': self.user,
                    'ansible_connection': 'ssh',
                    'ansible_shell_type': 'powershell',
                    'toolname': self.toolname,
                    'directories': [{
                        'src': self.source,
                        'dest': self.destination
                    }]
                }
            }
        else:
            # Data to write
            new_host_data = {
                f'host{new_host_number}': {
                    'ansible_host': self.host,
                    'ansible_user': self.user,
                    'toolname': self.toolname,
                    'directories': [{
                        'src': self.source,
                        'dest': self.destination
                    }]
                }
            }

        existing_data.setdefault('all', {}).setdefault('hosts', {}).update(new_host_data)

        # Write YAML data to file
        with open(file_path, 'w') as yaml_file:
            yaml.dump(existing_data, yaml_file, default_flow_style=False)
        yaml_file.close()
        print(f"YAML data successfully written to {file_path}")


    @staticmethod
    def delete_yaml(toolname):
        """
        Deletes a host entry based on the toolname from the hosts.yml file. 
        If it is the only host, deletes everything from the whole file.
        
        Parameters
        ----------
            toolname: str
                the name of the tool running on the host machine to be deleted
        
        Returns
        -------
            None
        """
        # Assuming the script is located in Tool-Data/scripts/
        current_directory = os.path.dirname(__file__)  # Get current script directory
        # Navigate up one level to Tool-Data/
        project_directory = os.path.abspath(os.path.join(current_directory, '..'))

        # Specify the relative path to the ansible directory
        ansible_directory = os.path.join(project_directory, 'ansible')

        # File path within the ansible directory
        file_path = os.path.join(ansible_directory, 'hosts.yml')

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            # File already exists and is not empty
            with open(file_path, 'r') as file:
                existing_data = yaml.safe_load(file)
        else:
            print(f"File {file_path} does not exist or is empty")
            raise FileNotFoundError(f"File {file_path} does not exist or is empty")
        
        # Flag to check if any host with the toolname was found and deleted
        host_deleted = False

        # Check if the toolname exists in any host
        if 'all' in existing_data and 'hosts' in existing_data['all']:
            hosts_to_delete = []
            for host_key, host_data in existing_data['all']['hosts'].items():
                if host_data.get('toolname') == toolname:
                    hosts_to_delete.append(host_key)
                    host_deleted = True

            # Delete hosts with the specified toolname
            for host_key in hosts_to_delete:
                del existing_data['all']['hosts'][host_key]

            # If no hosts remain, clear the entire file
            if not existing_data['all']['hosts']:
                with open(file_path, 'w') as yaml_file:
                    yaml_file.write('')
            else:
                # Write updated data to file
                with open(file_path, 'w') as yaml_file:
                    yaml.dump(existing_data, yaml_file, default_flow_style=False)

        if host_deleted:
            print(f"Host(s) with toolname '{toolname}' deleted from {file_path}")
        else:
            print(f"No host found with toolname '{toolname}' in {file_path}")


    def add_directory(self, host, toolname, source, destination):
        """
        Adds a new directory mapping to an existing host

            Parameters
            ----------
                host: str
                    the IP address of the host machine
                toolname: str
                    the nickname of the tool running on the host machine
                source: str
                    the source directory on the host machine
                destination: str
                    the destination directory on the host machine

            Returns
            -------
                None
        """
        # Assuming the script is located in Tool-Data/scripts/
        current_directory = os.path.dirname(__file__)  # Get current script directory
        # Navigate up one level to Tool-Data/
        project_directory = os.path.abspath(os.path.join(current_directory, '..'))

        # Specify the relative path to the ansible directory
        ansible_directory = os.path.join(project_directory, 'ansible')

        # File path within the ansible directory
        file_path = os.path.join(ansible_directory, 'hosts.yml')

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            # File already exists and is not empty
            with open(file_path, 'r') as file:
                existing_data = yaml.safe_load(file)
        else:
            # print(f"File {file_path} does not exist or is empty")
            existing_data = {'all': {'hosts': {}}}  # Initialize empty data

        # Check if the host exists
        for host_key, host_data in existing_data.get('all', {}).get('hosts', {}).items():
            if host_data.get('ansible_host') == host and host_data.get('toolname') == toolname:
                # Append new directory mapping
                if 'directories' in host_data:
                    host_data['directories'].append({'src': source, 'dest': destination})
                else:
                    host_data['directories'] = [{'src': source, 'dest': destination}]
                
                # Write updated data to file
                with open(file_path, 'w') as yaml_file:
                    yaml.dump(existing_data, yaml_file, default_flow_style=False)
                yaml_file.close()
                print(f"New directory mapping added to host {host} with toolname {toolname}")
                return
        
        print(f"Host {host} with toolname {toolname} not found in {file_path}")


# Main function to demonstrate usage and test
def main():
    host = "10.32.75.154"
    user = "andrew"
    toolname = "Savannah"
    source = "/Users/andrew/Desktop/"
    destination = "/Users/andrew/Desktop/SNF Projects/Tool-Data/src/Machines/Savannah/data/Output_Text/"
    yml = WriteYaml(host, user, toolname, source, destination)
    yml.write_yaml()
    yml.add_directory(host, "/Users/andrew/Desktop/", "/Users/andrew/Desktop/SNF Projects/Tool-Data/src/Machines/Savannah/data/Output_Plots/")
    WriteYaml.delete_yaml("Savannah")


if __name__ == "__main__":
    main()
