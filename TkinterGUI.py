import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


# default number of entries = 10
e = 10


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



def open_new_window():
    new_window = tk.Tk()
    new_window.title("Savannah Data Report")
    new_window.geometry("1000x1000")  # Set the new window size

    # Create a frame for the canvas and scrollbar
    frame = tk.Frame(new_window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a canvas
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    def on_vertical(event):
        canvas.yview_scroll(-1 * event.delta, 'units')


    # def on_horizontal(event):
    #     canvas.xview_scroll(-1 * event.delta, 'units')

    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Bind the scroll wheel event
    canvas.bind_all('<MouseWheel>', on_vertical)
    # canvas.bind_all('<Shift-MouseWheel>', on_horizontal)

    # Create another frame inside the canvas
    second_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")

    
    # for i in range(50):  # Add many labels to demonstrate the scrollbar
    #     tk.Label(second_frame, text=f"Additional content {i + 1}").pack()

    text_image_frame = tk.Frame(second_frame, bd=2, relief="groove")
    text_image_frame.pack(pady=20, padx=20, fill=tk.X)

    # Add a label for text
    out = "----------------------------------------------\n\nHEATING REPORT AT 11:01:27 ON 06/20/2024\n\n----------------------------------------------\n\nCompleted Cycles: 550 / 550\n\nNumber of Precursors: 3\n\nInner Heater Final Temp: 1000.0°C\n\nOuter Heater Final Temp: 1000.0°C\n\nAverage Temp of Precursor 1: 1000.0°C\n\nAverage Temp of Precursor 2: 1000.0°C\n\nAverage Temp of Precursor 3: 1000.0°C\n\nRecipe: 100C_TiO2\n\n----------------------------------------------"
    text_label = tk.Label(text_image_frame, text=out, wraplength=500, justify=tk.LEFT, font=("System", 18))
    text_label.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

    # Add a label for the image
    img = Image.open("Output_Plots/Non-Precursor Heating Data.png")  # Change this to your image path
    img = img.resize((600,600), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    image_label = tk.Label(text_image_frame, image=img)
    image_label.image = img  # Keep a reference to the image
    image_label.pack(side=tk.RIGHT, padx=10, pady=10)



    quit_button_frame = tk.Frame(new_window)
    quit_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    new_quit_button = tk.Button(second_frame, text="Quit", command=new_window.destroy)
    new_quit_button.pack(side=tk.BOTTOM, pady=10)

    new_window.mainloop()

# Create the main window
root = tk.Tk()
root.title("Savannah Data Report")

# Create a label above the text box
label = tk.Label(root, text="How Many Reports?")
label.pack(pady=5)

# Create a text box (Entry widget)
entry = tk.Entry(root, width=50)
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
