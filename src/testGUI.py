import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

# Default number of entries = 5 (Approx 8 seconds to load if all enormous files)
e = 5

from Pressure import Pressure
from Heating import Heating

def show_loading_screen():
    loading_window = tk.Toplevel()
    loading_window.title("Loading...")
    loading_window.geometry("300x100")
    
    loading_label = tk.Label(loading_window, text="Loading... Please wait.")
    loading_label.pack(pady=20)
    
    return loading_window

def generate_reports(second_frame, loading_window):
    reports = []
    h = Heating("/Users/andrew/Desktop/SNF Projects/Tool-Data/Heating-Data")
    p = Pressure("/Users/andrew/Desktop/SNF Projects/Tool-Data/Pressure-Data")
    p.initialize(e)
    h.initialize(e)

    for _ in range(e):
        text_image_frame = tk.Frame(second_frame, bd=2, relief="groove")
        text_image_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # Add a label for text
        imageh = "/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/Precursor Heating Data.png"
        imagep = "/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/PressureData.png"
        
        out = h.sendData()
        
        text_label = tk.Label(text_image_frame, text=out, wraplength=500, justify=tk.LEFT, font=("System", 18))
        text_label.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Add a label for the image
        img_h = Image.open(imageh)  # Change this to your image path
        img_h = img_h.resize((600, 600), Image.LANCZOS)
        img_h = ImageTk.PhotoImage(img_h)
        image_label_h = tk.Label(text_image_frame, image=img_h)
        image_label_h.image = img_h  # Keep a reference to the image
        image_label_h.pack(side=tk.RIGHT, padx=10, pady=10)

        reports.append((text_image_frame))

    for report in reports:
        report.pack_forget()
        report.pack(pady=20, padx=20, fill=tk.X)

    # After generating reports, destroy the loading screen window
    loading_window.destroy()

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
    if userEntry < 0:
        error_label.config(text="Error: Please enter a valid integer.")
    else:
        e = userEntry
        root.destroy()  # Close the current window
        open_new_window()

def open_new_window():
    global root
    new_window = tk.Tk()
    new_window.title("Savannah Data Report")
    new_window.geometry("1200x1000")  # Set the new window size

    # Create a frame for the canvas and scrollbar
    frame = tk.Frame(new_window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a canvas
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def on_vertical(event):
        canvas.yview_scroll(-1 * event.delta, 'units')

    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Bind the scroll wheel event
    canvas.bind_all('<MouseWheel>', on_vertical)

    # Create another frame inside the canvas
    second_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")

    # Create the "Refresh" button at the top
    top_frame = tk.Frame(new_window)
    top_frame.pack(fill=tk.X, padx=10, pady=10)
    
    refresh_button = tk.Button(top_frame, text="Refresh", command=lambda: refresh(new_window))
    refresh_button.pack(side=tk.LEFT, padx=5)

    # Show loading screen
    loading_window = show_loading_screen()

    # Generate reports
    generate_reports(second_frame, loading_window)

    # Update the scroll region and scroll to the bottom
    second_frame.update_idletasks()  # Ensure all widgets are drawn
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(1.0)  # Scroll to the bottom

    new_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    new_window.mainloop()

def refresh(new_window):
    position = new_window.geometry()  # Get the current position and size of the window
    new_window.destroy()
    open_new_window_with_position(position)

def open_new_window_with_position(position):
    new_window = tk.Tk()
    new_window.title("Savannah Data Report")
    new_window.geometry(position)  # Set the new window position and size

    # Create a frame for the canvas and scrollbar
    frame = tk.Frame(new_window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a canvas
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def on_vertical(event):
        canvas.yview_scroll(-1 * event.delta, 'units')

    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Bind the scroll wheel event
    canvas.bind_all('<MouseWheel>', on_vertical)

    # Create another frame inside the canvas
    second_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")

    # Create the "Refresh" button at the top
    top_frame = tk.Frame(new_window)
    top_frame.pack(fill=tk.X, padx=10, pady=10)
    
    refresh_button = tk.Button(top_frame, text="Refresh", command=lambda: refresh(new_window))
    refresh_button.pack(side=tk.LEFT, padx=5)

    # Show loading screen
    loading_window = show_loading_screen()

    # Generate reports
    generate_reports(second_frame, loading_window)

    # Update the scroll region and scroll to the bottom
    second_frame.update_idletasks()  # Ensure all widgets are drawn
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(1.0)  # Scroll to the bottom

    new_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    new_window.mainloop()

def on_closing(root):
    root.destroy()

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

error_label = tk.Label(root, text="", fg="red")
error_label.pack(pady=5)

# Run the Tkinter event loop
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
root.mainloop()
