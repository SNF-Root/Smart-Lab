import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

# default number of entries = 5
e = 5

from Pressure import Pressure
from Heating import Heating

def save_and_open_new_window():
    global e
    # If the entry is empty, open a new window
    if entry.get() == "":
        root.destroy()
        open_new_window()
        return
    # Check if the entry is a valid integer
    try:
        userEntry = int(entry.get())
    except ValueError:
        error_label.config(text="Error: Please enter a valid integer.")
        return
    
    # Check if the entry is a positive integer
    if (not userEntry.is_integer()) or (userEntry < 0):
        error_label.config(text="Error: Please enter a valid integer.")
    else:
        e = userEntry
        root.destroy()  # Close the current window
        open_new_window()

def quit_app():
    root.quit()

def on_vertical(event):
    canvas.yview_scroll(-1 * event.delta, 'units')

def open_new_window():
    new_window = tk.Tk()
    new_window.title("Savannah Data Report")
    new_window.geometry("1200x1000")  # Set the new window size

    # Create a frame for the canvas and scrollbar
    frame = tk.Frame(new_window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a canvas
    global canvas
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Bind the scroll wheel event
    canvas.bind_all('<MouseWheel>', on_vertical)

    # Create another frame inside the canvas
    global second_frame
    second_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")

    generate_reports()

    quit_button_frame = tk.Frame(new_window)
    quit_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    new_quit_button = tk.Button(quit_button_frame, text="Quit", command=new_window.destroy)
    new_quit_button.pack(pady=10)

    new_window.mainloop()

def generate_reports():
    reports = []
    for i in range(e):
        text_image_frame = tk.Frame(second_frame, bd=2, relief="groove")
        text_image_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # Add a label for text
        h = Heating("/Users/andrew/Desktop/SNF Projects/Tool-Data/Heating-Data/2024_06_13-21-21_MV standard Al2O3 4wtr pulse first 80deg.txt", "/Users/andrew/Desktop/SNF Projects/Tool-Data/Heating-Data")
        p = Pressure("/Users/andrew/Desktop/SNF Projects/Tool-Data/Pressure-Data/2024_06_13-12-56_Al2O3 - STANDARD.txt", "/Users/andrew/Desktop/SNF Projects/Tool-Data/Pressure-Data")
        imageh = "/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/Precursor Heating Data.png"
        out = h.genReport()
        text_label = tk.Label(text_image_frame, text=out, wraplength=500, justify=tk.LEFT, font=("System", 18))
        text_label.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Add a label for the image
        img = Image.open(imageh)  # Change this to your image path
        img = img.resize((600,600), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        image_label = tk.Label(text_image_frame, image=img)
        image_label.image = img  # Keep a reference to the image
        image_label.pack(side=tk.RIGHT, padx=10, pady=10)

        reports.append(text_image_frame)
    
    for report in reports:
        report.pack_forget()
        report.pack(pady=20, padx=20, fill=tk.X)

# Create the main window
root = tk.Tk()
root.title("Savannah Data Report")
root.geometry("400x200")  # Set the window size

# Create a label above the text box
label = tk.Label(root, text="How Many Reports?")
label.pack(pady=5)

# Create a text box (Entry widget)
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Create a button to save the entry and open a new window
start_button = tk.Button(root, text="Start", command=save_and_open_new_window)
start_button.pack(pady=10)

# Create a button to quit the application
quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.pack(pady=10)

error_label = tk.Label(root, text="", fg="red")
error_label.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
