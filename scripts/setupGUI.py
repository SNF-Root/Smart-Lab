import tkinter as tk
from tkinter import ttk
import os

from scripts.writeyaml import WriteYaml


# GUI for setting up the necesaary information to run the program
class SetupGUI:

    # Constructor to initialize the user-host list and Rclone path
    def __init__(self):
        self.user_host_list = []
        self.rclone_path = ""
        self.register_file_path = "src/register.txt"  # Path to register.txt file
        self.rclone_file_path = "src/rclone.txt"      # Path to rclone.txt file

        # ADD MORE LATER
        self.machinedict = {
            "Savannah ALD": "Savannah",
            "Fiji ALD": "Fiji"
        }
        self.how_many_folders = {
            "Savannah ALD": (2, "Pressure", "Heating"),
            "Fiji ALD": (2, "Pressure", "Heating")
        }


    # Main runner of the GUI
    def run(self):
        # Opens a second window where the user puts in machine information
        def open_second_window():
            selected_option = combobox.get()
            if selected_option:
                new_window = tk.Toplevel(root)
                new_window.title(selected_option)

                # Create and place the label for the selected option
                label = ttk.Label(new_window, text=f"You selected: {selected_option}")
                label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

                # Create and place the Machine Name label and entry
                machine_name_label = ttk.Label(new_window, text="Machine Name:")
                machine_name_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
                machine_name_entry = ttk.Entry(new_window)
                machine_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))

                # Create and place the User label and entry
                user_label = ttk.Label(new_window, text="User:")
                user_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
                user_entry = ttk.Entry(new_window)
                user_entry.grid(row=2, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))

                # Create and place the Host label and entry
                host_label = ttk.Label(new_window, text="Host (IP):")
                host_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
                host_entry = ttk.Entry(new_window)
                host_entry.grid(row=3, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))

                # Add folder entries based on the selected option
                folder_count, *folder_labels = self.how_many_folders[selected_option]
                folder_entries = []

                for idx, label in enumerate(folder_labels):
                    folder_label = ttk.Label(new_window, text=f"{label}:")
                    folder_label.grid(row=4 + idx, column=0, padx=10, pady=5, sticky=tk.E)
                    folder_entry = ttk.Entry(new_window)
                    folder_entry.grid(row=4 + idx, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))
                    folder_entries.append((label, folder_entry))


                # Submit for the second window that will process all data given by user
                def on_second_submit():
                    machine_name = machine_name_entry.get()
                    if machine_name == "":
                        machine_name = selected_option
                    user = user_entry.get()
                    host = host_entry.get()
                    folder_data = {label: entry.get() for label, entry in folder_entries}
                    self.user_host_list.append((selected_option, machine_name, user, host, folder_data))
                    # print(f"Machine Name: {machine_name}, User: {user}, Host (IP): {host}, Option: {selected_option}")
                    # print("Folder data:", folder_data)
                    # print("Current user-host list:", self.user_host_list)

                    # Error check for empty dictionary
                    realname = self.machinedict[selected_option]
                    if not folder_data:
                        print("No folder data entered")
                        self.user_host_list.pop()  # Remove the last entry
                        return
                    # Process information based on the selected option
                    else:
                        # Make the dictionary into more usable lists
                        # Create the proper data folders for the new machine
                        keys = []
                        values = []
                        os.makedirs(f"src/Machines/{realname}/data({machine_name})", exist_ok=True)
                        os.makedirs(f"src/Machines/{realname}/data({machine_name})/Output_Text", exist_ok=True)
                        os.makedirs(f"src/Machines/{realname}/data({machine_name})/Output_Plots", exist_ok=True)
                        with open(f"src/Machines/{realname}/data({machine_name})/process_stack.txt", "w") as file:
                            file.close()
                            pass
                        for x in folder_data:
                            keys.append(x)
                            values.append(folder_data[x])
                            os.makedirs(f"src/Machines/{realname}/data({machine_name})/{x}-data", exist_ok=True)

                        # Write the YAML file for the new machine
                        write = WriteYaml(host, user, machine_name, values[0], f"src/Machines/{realname}/data({machine_name})")
                        write.write_yaml()
                        for x in range(1, len(keys)):
                            write.add_directory(host, values[x], f"src/Machines/{realname}/data({machine_name})")

                    # Write the user-host list to the register.txt file
                    outstr = ""
                    for machine, machine_name, user, host, folder_data in self.user_host_list:
                        outstr += realname + " " + machine_name + " " + user + " " + host
                        for folder in folder_data:
                            outstr += " " + folder_data[folder]
                        outstr += "\n"

                    with open(self.register_file_path, "a+") as file:
                        file.write(outstr)
                    file.close()

                    # Clear the user-host list
                    new_window.destroy()


                # Create and place the Submit button for the second window
                second_submit_button = ttk.Button(new_window, text="Submit", command=on_second_submit)
                second_submit_button.grid(row=4 + folder_count, column=0, columnspan=2, pady=10)

                # Configure the grid to resize properly
                new_window.grid_columnconfigure(1, weight=1)
            else:
                print("No option selected")


        # Show the content of the register.txt and rclone.txt files
        def show_files_content():
            list_window = tk.Toplevel(root)
            list_window.title("Current Saved details")

            # Read and display register.txt content
            register_label = ttk.Label(list_window, text="Machines Registered:")
            register_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

            with open(self.register_file_path, 'r') as register_file:
                register_content = register_file.read()
            register_file.close()

            register_text = tk.Text(list_window, wrap=tk.WORD, height=10, width=50)
            register_text.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
            register_text.insert(tk.END, register_content)
            register_text.config(state=tk.DISABLED)

            # Read and display rclone.txt content
            rclone_label = ttk.Label(list_window, text="Rclone Root Path:")
            rclone_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

            with open(self.rclone_file_path, 'r') as rclone_file:
                rclone_content = rclone_file.read()
            rclone_file.close()

            rclone_text = tk.Text(list_window, wrap=tk.WORD, height=10, width=50)
            rclone_text.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
            rclone_text.insert(tk.END, rclone_content)
            rclone_text.config(state=tk.DISABLED)


        # Submit the Rclone path if a new path is provided
        def on_submit():
            new_rclone_path = rclone_entry.get()  # Get the Rclone path from the entry
            if new_rclone_path:  # Check if a new path is provided
                self.rclone_path = new_rclone_path
                print(f"Rclone root directory path: {self.rclone_path}")
                with open(self.rclone_file_path, 'w') as rclone_file:
                    rclone_file.write(self.rclone_path)
                rclone_file.close()
            root.destroy()


        # Main window setup
        root = tk.Tk()
        root.title("Smart Lab Setup")

        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for resizing
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        combobox_label = ttk.Label(frame, text="Select an option:")
        combobox_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        # ADD MORE LATER
        options = ["Savannah ALD", "Fiji ALD"]

        combobox = ttk.Combobox(frame, values=options, state="readonly")
        combobox.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        combobox.current(0)  # Set the default option

        add_machine_button = ttk.Button(frame, text="Add Machine", command=open_second_window)
        add_machine_button.grid(row=2, column=0, pady=10, sticky=tk.W)

        list_button = ttk.Button(frame, text="Current Info", command=show_files_content)
        list_button.grid(row=3, column=0, pady=10, sticky=tk.W)

        rclone_label = ttk.Label(frame, text="Rclone path:")
        rclone_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

        rclone_entry = ttk.Entry(frame)
        rclone_entry.grid(row=5, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        submit_button = ttk.Button(frame, text="Submit", command=on_submit)
        submit_button.grid(row=6, column=0, pady=10, sticky=tk.W)

        root.mainloop()


# Main function to run tests on the GUI
def main():
    setup = SetupGUI()
    setup.run()


if __name__ == "__main__":
    main()
