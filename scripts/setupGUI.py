import tkinter as tk
from tkinter import ttk

from scripts.writeyaml import WriteYaml

# Global list to store user and host inputs
class SetupGUI:

    # Constructor to initialize the user-host list and Rclone path
    def __init__(self):
        self.user_host_list = []
        self.rclone_path = ""

        # ADD MORE LATER
        self.machinedict = {
            "Savannah ALD": "Savannah",
            "Fiji ALD": "Fiji"
        }

        self.how_many_folders = {
            "Savannah ALD": (2, "Pressure", "Heating"),
            "Fiji ALD": (2, "Pressure", "Heating")
        }

        self.destinations = {
            "Savannah ALD": ["src/Machines/Savannah/data/Output_Text", "src/Machines/Savannah/data/Output_Plots"],
            "Fiji ALD": ""
        }

    # Main runner of the GUI
    def run(self):
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

                # Define the submit function for the second window
                def on_second_submit():
                    machine_name = machine_name_entry.get()
                    if machine_name == "":
                        machine_name = selected_option
                    user = user_entry.get()
                    host = host_entry.get()
                    folder_data = {label: entry.get() for label, entry in folder_entries}
                    self.user_host_list.append((selected_option, machine_name, user, host, folder_data))
                    print(f"Machine Name: {machine_name}, User: {user}, Host (IP): {host}, Option: {selected_option}")
                    print("Folder data:", folder_data)
                    print("Current user-host list:", self.user_host_list)
                    new_window.destroy()

                # Create and place the Submit button for the second window
                second_submit_button = ttk.Button(new_window, text="Submit", command=on_second_submit)
                second_submit_button.grid(row=4 + folder_count, column=0, columnspan=2, pady=10)

                # Configure the grid to resize properly
                new_window.grid_columnconfigure(1, weight=1)
            else:
                print("No option selected")

        def on_submit():
            self.rclone_path = rclone_entry.get()  # Get the Rclone path
            print(f"Rclone root directory path: {self.rclone_path}")
            root.destroy()

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

        rclone_label = ttk.Label(frame, text="Rclone path:")
        rclone_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        rclone_entry = ttk.Entry(frame)
        rclone_entry.grid(row=4, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        submit_button = ttk.Button(frame, text="Submit", command=on_submit)
        submit_button.grid(row=5, column=0, pady=10, sticky=tk.W)

        root.mainloop()

    def processInfo(self):
        print("User-Host List:", self.user_host_list)
        print("Rclone Path:", self.rclone_path)
        for machine, machine_name, user, host, folder_data in self.user_host_list:
            realname = self.machinedict[machine]
        file = open("src/register.txt", "w")
        file.write(f"\n{realname} {realname}.py")

def main():
    setup = SetupGUI()
    setup.run()

if __name__ == "__main__":
    main()
