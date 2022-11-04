import datetime
import tkinter as tk
from tkinter import *
import os
import time
import shutil
from tkinter import ttk

# Set up tkinter window
app = tk.Tk()
app.title("File Sorter")
app.iconbitmap("icon.ico")

# Initialize tkinter frame
frame = ttk.Frame(app, padding="3 3 12 12")
frame.grid(column=3, row=2, sticky=(N, W, E, S))
app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)

# Add Path Entry widget
pathEntry = ttk.Entry(frame, width=20, textvariable=StringVar())
pathEntry.grid(column=2, row=1, sticky=(W, E))

# Add other widgets
ttk.Label(frame, text="Path:").grid(column=1, row=1, sticky=W)
ttk.Label(frame, text="\sort").grid(column=3, row=1, sticky=W)
ttk.Button(frame, text="Sort", command=lambda: sort(pathEntry.get())).grid(column=3, row=2, sticky=W)


def sort(path):
    # Get sort path
    files = os.listdir(path+"\sort")

    #Create and init Sorting Window
    sortWindow = Toplevel(app)
    sortWindow.title("Sorting")
    sortFrame = ttk.Frame(sortWindow, padding="3 3 12 12")
    sortFrame.grid(column=2, row=0, sticky=(N, W, E, S))
    sortWindow.columnconfigure(0, weight=1)
    sortWindow.rowconfigure(0, weight=1)
    sortProgress = ttk.Progressbar(sortFrame, orient="horizontal", length=200, mode="determinate")
    sortProgress.grid(column=2, row=0, sticky=(W, E))

    # get percentage of files
    try:
        progressInterval = 100/len(files)
    except ZeroDivisionError:
        progressInterval = 100

    # Sort files
    for file in files:
        #Get creation date
        date = datetime.datetime.fromtimestamp(os.path.getctime(path + "\sort\\" + file)).strftime("%Y")
        try:
            # Create folder if it doesn't exist
            os.mkdir(path + "\\" + date)
        except FileExistsError:
            pass
        # Move file to folder
        shutil.move(path + "\sort\\" + file, path + "\\" + date + "\\" + file)
        # Update progress bar
        sortProgress["value"] += progressInterval
        sortProgress.update()
    # close window when finished
    sortWindow.destroy()
    #create finished dialog window
    doneWindow = Toplevel(app)
    doneWindow.title("Done!")
    doneFrame = ttk.Frame(doneWindow, padding="3 3 12 12")
    doneFrame.grid(column=3, row=0, sticky=(N, W, E, S))
    doneWindow.columnconfigure(0, weight=1)
    doneWindow.rowconfigure(0, weight=1)
    ttk.Label(doneFrame, text="Done!").grid(column=1, row=0, sticky=W)
    ttk.Label(doneFrame, text="Sorting Complete! Sorted " + str(len(files)) + " files.").grid(column=2, row=0, sticky=W)
    ttk.Button(doneFrame, text="Close", command=doneWindow.destroy).grid(column=3, row=0, sticky=W)

# Run tkinter window
app.mainloop()


        



        