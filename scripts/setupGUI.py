import tkinter as tk
from tkinter import ttk
import os
import re
from scripts.writeyaml import WriteYaml

class SetupGUI:
    """
    Class for GUI for setting up the project

    Attributes:
    ----------
        user_host_list : list
            A list of tuples containing the user, host, and machine details
        rclone_path : str
            The path to the Rclone directory
        register_file_path : str
            The path to the register file
        rclone_file_path : str
            The path to the rclone file
        machinelist : list
            A list of machine names
        machinedict : dict
            A dictionary mapping machine names to their real names
        how_many_folders : dict
            A dictionary mapping machine names to the number of folders and their names

    Methods:
    ----------
        run()
            Run the GUI
    """
    def __init__(self):
        self.user_host_list = []
        self.rclone_path = ""
        self.register_file_path = os.path.join("src", "register.txt")
        self.rclone_file_path = os.path.join("src", "rclone.txt")
        self.machinelist = ["Savannah ALD", "Fiji ALD (F202)", "Smart Cam"]
        self.machinedict = {
            "Savannah ALD": "Savannah",
            "Fiji ALD (F202)": "Fiji202",
            "Smart Cam": "SmartCam"
        }
        self.how_many_folders = {
            "Savannah ALD": (2, "Pressure", "Heating"),
            "Fiji ALD (F202)": (3, "Pressure", "Heating", "Plasma"),
            "Smart Cam": (1, "Data")
        }


    def run(self):
        """
        Run the GUI

            Parameters:
            ----------
                None

            Returns:
            ----------
                None
        """
        def open_second_window():
            """
            Open a new window to add a machine to the entries

                Parameters:
                ----------
                    None
                
                Returns:
                ----------
                    None
            """
            selected_option = combobox.get()
            if selected_option:
                new_window = tk.Toplevel(root)
                new_window.title(f"{selected_option} Setup")

                label = ttk.Label(new_window, text=f"You selected: {selected_option}")
                label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

                machine_name_label = ttk.Label(new_window, text="Machine Name:")
                machine_name_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
                machine_name_entry = ttk.Entry(new_window)
                machine_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))

                user_label = ttk.Label(new_window, text="User:")
                user_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
                user_entry = ttk.Entry(new_window)
                user_entry.grid(row=2, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))

                host_label = ttk.Label(new_window, text="Host (IP):")
                host_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
                
                ip_part1 = ttk.Entry(new_window, width=5)
                ip_part1.grid(row=3, column=1, padx=(10, 2), pady=5, sticky=tk.W)
                ip_dot1 = ttk.Label(new_window, text=".")
                ip_dot1.grid(row=3, column=1, sticky=tk.W, padx=(50, 0))

                ip_part2 = ttk.Entry(new_window, width=5)
                ip_part2.grid(row=3, column=1, padx=(55, 2), pady=5, sticky=tk.W)
                ip_dot2 = ttk.Label(new_window, text=".")
                ip_dot2.grid(row=3, column=1, sticky=tk.W, padx=(95, 0))

                ip_part3 = ttk.Entry(new_window, width=5)
                ip_part3.grid(row=3, column=1, padx=(100, 2), pady=5, sticky=tk.W)
                ip_dot3 = ttk.Label(new_window, text=".")
                ip_dot3.grid(row=3, column=1, sticky=tk.W, padx=(140, 0))

                ip_part4 = ttk.Entry(new_window, width=5)
                ip_part4.grid(row=3, column=1, padx=(145, 0), pady=5, sticky=tk.W)

                remote_paths_label = ttk.Label(new_window, text="Remote File Paths:")
                remote_paths_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

                raw_var = tk.IntVar()
                raw_checkbox = ttk.Checkbutton(new_window, text="Raw files", variable=raw_var)
                raw_checkbox.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

                folder_count, *folder_labels = self.how_many_folders[selected_option]
                folder_entries = []

                for idx, label in enumerate(folder_labels):
                    folder_label = ttk.Label(new_window, text=f"{label}:")
                    folder_label.grid(row=5 + idx, column=0, padx=10, pady=5, sticky=tk.E)
                    folder_entry = ttk.Entry(new_window)
                    folder_entry.grid(row=5 + idx, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))
                    folder_entries.append((label, folder_entry))


                def on_second_submit():
                    """
                    Submit the machine details to the register file and write the YAML file

                        Parameters:
                        ----------
                            None
                        
                        Returns:
                        ----------
                            None
                    """
                    machine_name = machine_name_entry.get()
                    if machine_name == "":
                        machine_name = selected_option
                    if not is_valid_directory_name(machine_name):
                        show_error_window("Invalid machine directory name. Please enter a valid machine name.")
                        return
                    if machine_name_exists(machine_name):
                        show_error_window("Machine name already exists. Please enter a different name.")
                        return
                    user = user_entry.get()
                    if not user or user.isspace():
                        show_error_window("User name cannot be empty. Please enter a user name.")
                        return
                    host = f"{ip_part1.get()}.{ip_part2.get()}.{ip_part3.get()}.{ip_part4.get()}"
                    if not is_valid_ip_address(host):
                        show_error_window("Invalid IP address. Please enter a valid IP address.")
                        return
                    folder_data = {label: entry.get() for label, entry in folder_entries}
                    for folder in folder_data:
                        if not is_valid_path(folder_data[folder]):
                            show_error_window(f"Invalid path for {folder}. Please enter a valid path.")
                            return
                        
                    raw_status = "raw" if raw_var.get() == 1 else "processed"
                    self.user_host_list.append((selected_option, machine_name, user, host, folder_data, raw_status))
                    
                    realname = self.machinedict[selected_option]
                    if not folder_data:
                        print("No folder data entered")
                        self.user_host_list.pop()
                        return
                    else:
                        keys = []
                        values = []
                        folder_path = os.path.join('src', 'Machines', realname, f"data({machine_name})")
                        additional_items = ["Output_Text", "Output_Plots", "Output_Data", "process_stack.txt", "metadata.txt"]
                        
                        os.makedirs(folder_path, exist_ok=True)
                        for item in additional_items:
                            if os.path.splitext(item)[1] != "":
                                with open(os.path.join(folder_path, item), "w") as file:
                                    file.close()
                                    pass
                            else:
                                os.makedirs(os.path.join(folder_path, item), exist_ok=True)

                        for x in folder_data:
                            keys.append(x)
                            values.append(folder_data[x])
                            os.makedirs(os.path.join(folder_path, f"{x}-Data"), exist_ok=True)

                        write = WriteYaml(host, user, machine_name, values[0], 
                                          os.path.join(folder_path, f"{self.how_many_folders[selected_option][1]}-Data"))
                        write.write_yaml()
                        for x in range(1, len(keys)):
                            write.add_directory(host, machine_name, values[x],
                                                os.path.join(folder_path, f"{self.how_many_folders[selected_option][x+1]}-Data"))
                    
                    outstr = ""
                    for machine, machine_name, user, host, folder_data, raw_status in self.user_host_list:
                        outstr += realname + " " + machine_name + " " + user + " " + host + " " + raw_status
                        for folder in folder_data:
                            outstr += " " + folder_data[folder]
                        outstr += "\n"

                    with open(self.register_file_path, "a+") as file:
                        file.write(outstr)
                    file.close()

                    new_window.destroy()

                submit_button = ttk.Button(new_window, text="Submit", command=on_second_submit)
                submit_button.grid(row=7 + len(folder_entries), column=0, columnspan=2, pady=10)


        def show_files_content():
            """
            Show the contents of the register.txt and rclone.txt files
                
                Parameters:
                ----------
                    None
                
                Returns:
                ----------
                    None
            """
            list_window = tk.Toplevel(root)
            list_window.title("Current Info")
            list_window.geometry("400x400")  # Set an initial size for the window
            list_window.resizable(True, True)  # Make the window resizable

            register_label = ttk.Label(list_window, text="Contents of register.txt:")
            register_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

            with open(self.register_file_path, 'r') as register_file:
                register_content = register_file.read()
            
            register_text = tk.Text(list_window, wrap=tk.WORD)
            register_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            register_text.insert(tk.END, register_content)
            register_text.config(state=tk.DISABLED)

            rclone_label = ttk.Label(list_window, text="Contents of rclone.txt:")
            rclone_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

            with open(self.rclone_file_path, 'r') as rclone_file:
                rclone_content = rclone_file.read()
            
            rclone_text = tk.Text(list_window, wrap=tk.WORD)
            rclone_text.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
            rclone_text.insert(tk.END, rclone_content)
            rclone_text.config(state=tk.DISABLED)

            # Configure rows and columns to be resizable
            list_window.grid_rowconfigure(1, weight=1)
            list_window.grid_rowconfigure(3, weight=1)
            list_window.grid_columnconfigure(0, weight=1)


        def open_remove_window():
            """
            Open a new window to remove a machine from the entries
                
                Parameters:
                ----------
                    None
                
                Returns:
                ----------
            """
            remove_window = tk.Toplevel(root)
            remove_window.title("Remove a Machine")

            remove_label = ttk.Label(remove_window, text="Select a machine to remove:")
            remove_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

            with open(self.register_file_path, 'r') as register_file:
                machines = [line.split()[1] for line in register_file]
            register_file.close()

            remove_combobox = ttk.Combobox(remove_window, values=machines, state="readonly")
            remove_combobox.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
            if machines:
                remove_combobox.current(0)


            def on_remove():
                """
                Remove the selected machine from the register file and delete it on the YAML file
                
                    Parameters:
                    ----------
                        None
                    
                    Returns:
                    ----------
                        None
                """
                selected_machine = remove_combobox.get()
                if selected_machine:
                    remove_machine(selected_machine)
                    remove_window.destroy()

            remove_button = ttk.Button(remove_window, text="Remove", command=on_remove, width=10)
            remove_button.grid(row=2, column=0, pady=10, padx=(50, 50))

            # Configure grid column to center the button
            remove_window.grid_columnconfigure(0, weight=1)


        def on_submit():
            """
            Submit the new Rclone path to the rclone.txt file
                    
                Parameters:
                ----------
                    None
                
                Returns:
                ----------
                    None
            """
            new_rclone_path = rclone_entry.get()
            if new_rclone_path:
                if not is_valid_path(new_rclone_path):
                    show_error_window("Invalid Rclone directory/path name. Please enter a valid Rclone directory name.")
                    return
                if new_rclone_path[-1] == '/':
                    new_rclone_path = new_rclone_path[:-1]
                self.rclone_path = new_rclone_path
                print(f"Rclone root directory path: {self.rclone_path}")
                with open(self.rclone_file_path, 'w') as rclone_file:
                    rclone_file.write(self.rclone_path)
                rclone_file.close()
            root.destroy()


        def machine_name_exists(machine_name):
            """
            Check if the machine name already exists in the register file
                
                Parameters:
                ----------
                    machine_name : str
                        The machine name to check for existence
                
                Returns:
                ----------
                    bool
                        True if the machine name exists, False otherwise
            """
            if not os.path.exists(self.register_file_path):
                return False
            with open(self.register_file_path, 'r') as file:
                for line in file:
                    values = line.strip().split()
                    if values[1] == machine_name:
                        return True
            return False


        def show_error_window(message):
            """
            Show an error window with the given message

                Parameters:
                ----------
                    message : str
                        The error message to display
                
                Returns:
                ----------
                    None
            """
            error_window = tk.Toplevel(root)
            error_window.title("ERROR")
            label = ttk.Label(error_window, text=message, foreground="red")
            label.pack(padx=10, pady=10)
            button = ttk.Button(error_window, text="OK", command=error_window.destroy)
            button.pack(pady=5)


        def is_valid_directory_name(name):
            """
            Check if the directory name is valid
                
                Parameters:
                ----------
                    name : str
                        The directory name to check
                
                Returns:
                ----------
                    bool
                        True if the directory name is valid, False otherwise
            """
            invalid_characters = r'[/?<>\\:*|"\0]'
            if re.search(invalid_characters, name):
                return False
            if name in (".", ".."):  # Avoid using . or .. as directory names
                return False
            if not name:  # Name should not be empty
                return False
            return True


        def is_valid_path(path):
            """
            Check if the path is valid given a path string
                    
                Parameters:
                ----------
                    path : str
                        The path to check
                
                Returns:
                ----------
                    bool
                        True if the path is valid, False otherwise
            """
            print(path)
            invalid_characters = r'[<>"|?*\0]'
            if re.search(invalid_characters, path):
                print("Invalid characters")
                return False
            if not path:
                return False
            parts = path.split('/')
            if not parts:
                parts = path.split('\\')
            for part in parts:
                if part in ('.', '..'):  # Avoid using . or .. in path segments
                    return False
                if not part:  # Avoid empty segments (e.g., double slashes //)
                    continue
                if re.search(invalid_characters, part):
                    return False
            return True


        def is_valid_ip_address(ip):
            """
            Check if the IP address is valid in terms of format
                    
                Parameters:
                ----------
                    ip : str
                        The IP address to check
                
                Returns:
                ----------
                    bool
                        True if the IP address is valid, False otherwise
            """
            if not all(char.isdigit() or char == '.' for char in ip):
                return False
            parts = ip.split('.')
            for part in parts:
                if len(part) > 3:
                    return False
                if not part.isdigit():
                    return False
            return True


        def remove_machine(machine_name):
            """
            Remove the machine from the register file and delete it from the YAML file
                    
                Parameters:
                ----------
                    machine_name : str
                        The machine name to remove
                
                Returns:
                ----------
                    None
            """
            with open(self.register_file_path, 'r') as file:
                lines = file.readlines()
            with open(self.register_file_path, 'w') as file:
                for line in lines:
                    if line.split()[1] != machine_name:
                        file.write(line)
                    # else:
                    #     # Extracting necessary details for WriteYaml's delete_yaml
                    #     details = line.split()
            file.close()

            # Call the static delete_yaml method
            WriteYaml.delete_yaml(machine_name)

            # Implement additional cleanup if needed (e.g., removing directories)
            # Here, implement the removal of the machine from hosts.yml if needed

        root = tk.Tk()
        root.title("Smart Lab Setup")

        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        combobox_label = ttk.Label(frame, text="Select an option:")
        combobox_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        options = self.machinelist

        combobox = ttk.Combobox(frame, values=options, state="readonly")
        combobox.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        combobox.current(0)

        add_machine_button = ttk.Button(frame, text="Add Machine", command=open_second_window)
        add_machine_button.grid(row=2, column=0, pady=10, sticky=tk.W)

        list_button = ttk.Button(frame, text="Current Info", command=show_files_content)
        list_button.grid(row=3, column=0, pady=10, sticky=tk.W)

        remove_machine_button = ttk.Button(frame, text="Remove a Machine", command=open_remove_window)
        remove_machine_button.grid(row=4, column=0, pady=10, sticky=tk.W)

        rclone_label = ttk.Label(frame, text="Rclone path:")
        rclone_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

        rclone_entry = ttk.Entry(frame)
        rclone_entry.grid(row=6, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        submit_button = ttk.Button(frame, text="Submit", command=on_submit)
        submit_button.grid(row=7, column=0, pady=10, sticky=tk.W)

        root.mainloop()


def main():
    setup = SetupGUI()
    setup.run()

if __name__ == "__main__":
    main()
