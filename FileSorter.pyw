import datetime
import tkinter as tk
from tkinter import *
import os
import time
import shutil
from tkinter import ttk


app = tk.Tk()
app.title("File Sorter")
app.iconbitmap("icon.ico")

frame = ttk.Frame(app, padding="3 3 12 12")
frame.grid(column=3, row=2, sticky=(N, W, E, S))
app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)


pathEntry = ttk.Entry(frame, width=20, textvariable=StringVar())
pathEntry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(frame, text="Path:").grid(column=1, row=1, sticky=W)
ttk.Label(frame, text="\sort").grid(column=3, row=1, sticky=W)
ttk.Button(frame, text="Sort", command=lambda: sort(pathEntry.get())).grid(column=3, row=2, sticky=W)
def sort(path):
    files = os.listdir(path+"\sort")
    sortWindow = Toplevel(app)
    sortWindow.title("Sorting")
    sortFrame = ttk.Frame(sortWindow, padding="3 3 12 12")
    sortFrame.grid(column=2, row=0, sticky=(N, W, E, S))
    sortWindow.columnconfigure(0, weight=1)
    sortWindow.rowconfigure(0, weight=1)
    sortProgress = ttk.Progressbar(sortFrame, orient="horizontal", length=200, mode="determinate")
    sortProgress.grid(column=2, row=0, sticky=(W, E))
    try:
        progressInterval = 100/len(files)
    except ZeroDivisionError:
        progressInterval = 100
    for file in files:
        date = datetime.datetime.fromtimestamp(os.path.getctime(path + "\sort\\" + file)).strftime("%Y")
        print(date)
        try:
            os.mkdir(path + "\\" + date)
        except FileExistsError:
            pass
        shutil.move(path + "\sort\\" + file, path + "\\" + date + "\\" + file)
        sortProgress["value"] += progressInterval
        sortProgress.update()
    sortWindow.destroy()
    doneWindow = Toplevel(app)
    doneWindow.title("Done!")
    doneFrame = ttk.Frame(doneWindow, padding="3 3 12 12")
    doneFrame.grid(column=3, row=0, sticky=(N, W, E, S))
    doneWindow.columnconfigure(0, weight=1)
    doneWindow.rowconfigure(0, weight=1)

    ttk.Label(doneFrame, text="Done!").grid(column=1, row=0, sticky=W)
    ttk.Label(doneFrame, text="Sorting Complete! Sorted " + str(len(files)) + " files.").grid(column=2, row=0, sticky=W)
    ttk.Button(doneFrame, text="Close", command=doneWindow.destroy).grid(column=3, row=0, sticky=W)

app.mainloop()


        



        