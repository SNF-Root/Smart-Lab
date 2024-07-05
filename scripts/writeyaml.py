import os
import yaml


# setup class that writes to the hosts.yml file to add a new host machine
class WriteYaml:
    
    # Constructor to initialize the host, user, source, and destination
    def __init__(self, host, user, source, destination):
        self.host = host
        self.user = user
        self.source = source
        self.destination = destination


    # Write YAML data to the hosts.yml file
    def write_yaml(self):
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
            existing_data = {'all': {'hosts': {}}}  # Initialize empty data

        if 'all' in existing_data and 'hosts' in existing_data['all']:
            last_host_number = len(existing_data['all']['hosts'])
        else:
            last_host_number = 0

        # Increment the host number
        new_host_number = last_host_number + 1
        
        # Data to write
        new_host_data = {
            f'host{new_host_number}': {
                'ansible_host': self.host,
                'ansible_user': self.user,
                'directories' : [{
                    'src': self.source,
                    'dest': self.destination
                }]
            }
        }

        existing_data.setdefault('all', {}).setdefault('hosts', {}).update(new_host_data)

        # Write YAML data to file
        with open(file_path, 'w') as yaml_file:
            yaml.dump(existing_data, yaml_file, default_flow_style=False)

        print(f"YAML data successfully written to {file_path}")


    # Add a new directory mapping to an existing host
    def add_directory(self, host, source, destination):
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
            existing_data = {'all': {'hosts': {}}}  # Initialize empty data

        # Check if the host exists
        for host_key, host_data in existing_data.get('all', {}).get('hosts', {}).items():
            if host_data.get('ansible_host') == host:
                # Append new directory mapping
                if 'directories' in host_data:
                    host_data['directories'].append({'src': source, 'dest': destination})
                else:
                    host_data['directories'] = [{'src': source, 'dest': destination}]
                
                # Write updated data to file
                with open(file_path, 'w') as yaml_file:
                    yaml.dump(existing_data, yaml_file, default_flow_style=False)
                
                print(f"New directory mapping added to host {host}")
                return
        
        print(f"Host {host} not found in {file_path}")



def main():
    host = "10.32.78.231"
    user = "andrew"
    source = "/Users/andrew/Desktop/"
    destination = "/Users/andrew/Desktop/SNF Projects/Tool-Data/data/Output_Text/"
    yml = WriteYaml(host, user, source, destination)
    yml.write_yaml()
    yml.add_directory(host, "/Users/andrew/Desktop/", "/Users/andrew/Desktop/SNF Projects/Tool-Data/data/Output_Plots/")


if __name__ == "__main__":
    main()