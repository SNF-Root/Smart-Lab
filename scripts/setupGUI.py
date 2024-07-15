import tkinter as tk
from tkinter import ttk
import os
from scripts.writeyaml import WriteYaml

class SetupGUI:

    def __init__(self):
        self.user_host_list = []
        self.rclone_path = ""
        self.register_file_path = "src/register.txt"
        self.rclone_file_path = "src/rclone.txt"
        self.machinedict = {
            "Savannah ALD": "Savannah",
            "Fiji ALD": "Fiji"
        }
        self.how_many_folders = {
            "Savannah ALD": (2, "Pressure", "Heating"),
            "Fiji ALD": (2, "Pressure", "Heating")
        }

    def run(self):
        def open_second_window():
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

                remote_paths_label = ttk.Label(new_window, text="Remote File Paths")
                remote_paths_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky=tk.N)

                folder_count, *folder_labels = self.how_many_folders[selected_option]
                folder_entries = []

                for idx, label in enumerate(folder_labels):
                    folder_label = ttk.Label(new_window, text=f"{label}:")
                    folder_label.grid(row=5 + idx, column=0, padx=10, pady=5, sticky=tk.E)
                    folder_entry = ttk.Entry(new_window)
                    folder_entry.grid(row=5 + idx, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))
                    folder_entries.append((label, folder_entry))

                def on_second_submit():
                    machine_name = machine_name_entry.get()
                    if machine_name == "":
                        machine_name = selected_option
                    if machine_name_exists(machine_name):
                        show_error_window("Machine name already exists. Please enter a different name.")
                        return
                    user = user_entry.get()
                    host = f"{ip_part1.get()}.{ip_part2.get()}.{ip_part3.get()}.{ip_part4.get()}"
                    folder_data = {label: entry.get() for label, entry in folder_entries}
                    self.user_host_list.append((selected_option, machine_name, user, host, folder_data))
                    
                    realname = self.machinedict[selected_option]
                    if not folder_data:
                        print("No folder data entered")
                        self.user_host_list.pop()
                        return
                    else:
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
                            os.makedirs(f"src/Machines/{realname}/data({machine_name})/{x}-Data", exist_ok=True)

                        write = WriteYaml(host, user, machine_name, values[0], f"src/Machines/{realname}/data({machine_name})/{self.how_many_folders[selected_option][1]}-Data")
                        write.write_yaml()
                        for x in range(1, len(keys)):
                            write.add_directory(host, values[x], f"src/Machines/{realname}/data({machine_name})/{self.how_many_folders[selected_option][x+1]}-Data")

                    outstr = ""
                    for machine, machine_name, user, host, folder_data in self.user_host_list:
                        outstr += realname + " " + machine_name + " " + user + " " + host
                        for folder in folder_data:
                            outstr += " " + folder_data[folder]
                        outstr += "\n"

                    with open(self.register_file_path, "a+") as file:
                        file.write(outstr)
                    file.close()

                    new_window.destroy()

                second_submit_button = ttk.Button(new_window, text="Submit", command=on_second_submit)
                second_submit_button.grid(row=5 + folder_count, column=0, columnspan=2, pady=10)
                new_window.grid_columnconfigure(1, weight=1)
            else:
                print("No option selected")

        def show_files_content():
            list_window = tk.Toplevel(root)
            list_window.title("Current Saved details")

            register_label = ttk.Label(list_window, text="Machines Registered:")
            register_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

            with open(self.register_file_path, 'r') as register_file:
                register_content = register_file.read()
            register_file.close()

            register_text = tk.Text(list_window, wrap=tk.WORD, height=10, width=50)
            register_text.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
            register_text.insert(tk.END, register_content)
            register_text.config(state=tk.DISABLED)

            rclone_label = ttk.Label(list_window, text="Rclone Root Path:")
            rclone_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

            with open(self.rclone_file_path, 'r') as rclone_file:
                rclone_content = rclone_file.read()
            rclone_file.close()

            rclone_text = tk.Text(list_window, wrap=tk.WORD, height=10, width=50)
            rclone_text.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
            rclone_text.insert(tk.END, rclone_content)
            rclone_text.config(state=tk.DISABLED)

        def on_submit():
            new_rclone_path = rclone_entry.get()
            if new_rclone_path:
                self.rclone_path = new_rclone_path
                print(f"Rclone root directory path: {self.rclone_path}")
                with open(self.rclone_file_path, 'w') as rclone_file:
                    rclone_file.write(self.rclone_path)
                rclone_file.close()
            root.destroy()

        def machine_name_exists(machine_name):
            if not os.path.exists(self.register_file_path):
                return False
            with open(self.register_file_path, 'r') as file:
                for line in file:
                    values = line.strip().split()
                    if values[1] == machine_name:
                        return True
            return False

        def show_error_window(message):
            error_window = tk.Toplevel(root)
            error_window.title("Error")
            label = ttk.Label(error_window, text=message, foreground="red")
            label.pack(padx=10, pady=10)
            button = ttk.Button(error_window, text="OK", command=error_window.destroy)
            button.pack(pady=5)

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

        options = ["Savannah ALD", "Fiji ALD"]

        combobox = ttk.Combobox(frame, values=options, state="readonly")
        combobox.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        combobox.current(0)

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

def main():
    setup = SetupGUI()
    setup.run()

if __name__ == "__main__":
    main()
