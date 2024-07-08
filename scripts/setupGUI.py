import tkinter as tk
from tkinter import ttk

# Global list to store user and host inputs
user_host_list = []

def on_submit():
    selected_option = combobox.get()
    if selected_option:
        new_window = tk.Toplevel(root)
        new_window.title(selected_option)

        # Create and place the label for the selected option
        label = ttk.Label(new_window, text=f"You selected: {selected_option}")
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Create and place the User label and entry
        user_label = ttk.Label(new_window, text="User:")
        user_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        user_entry = ttk.Entry(new_window)
        user_entry.grid(row=1, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))

        # Create and place the Host label and entry
        host_label = ttk.Label(new_window, text="Host:")
        host_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        host_entry = ttk.Entry(new_window)
        host_entry.grid(row=2, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))

        # Define the submit function for the second window
        def on_second_submit():
            user = user_entry.get()
            host = host_entry.get()
            user_host_list.append((selected_option, user, host))
            print(f"User: {user}, Host: {host}, Option: {selected_option}")
            print("Current user-host list:", user_host_list)
            new_window.destroy()

        # Create and place the Submit button for the second window
        second_submit_button = ttk.Button(new_window, text="Submit", command=on_second_submit)
        second_submit_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Configure the grid to resize properly
        new_window.grid_columnconfigure(1, weight=1)
    else:
        print("No option selected")

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

options = ["Savannah ALD", "Fiji ALD"]

combobox = ttk.Combobox(frame, values=options, state="readonly")
combobox.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
combobox.current(0)  # Set the default option

submit_button = ttk.Button(frame, text="Submit", command=on_submit)
submit_button.grid(row=2, column=0, pady=10, sticky=tk.W)

# Add the Done button to the main window
done_button = ttk.Button(frame, text="Done", command=root.destroy)
done_button.grid(row=3, column=0, pady=10, sticky=tk.W)

root.mainloop()
