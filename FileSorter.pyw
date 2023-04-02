# Welcome to FileSorter!
# This program will sort files, the way you want them sorted!
# Copyright © 2022 GeraldTM

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


import datetime,json, shutil, tkinter as tk, os
from posixpath import abspath

from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image,UnidentifiedImageError

if os.name == "nt":
    newline = "\r\n"
else:
    newline = "\n"


# Set up tkinter window
app = TkinterDnD.Tk()
app.title("FileSorter")
app.iconbitmap(True,"icon.ico")
app.resizable(width=False, height=False)

selectedSortType = StringVar()
selectedSortType.set("time")
fileListValue = StringVar()
keepOGFiles = BooleanVar()

# Init File Frame
fileFrame = ttk.Frame(app, padding="3 3 12 12")
fileFrame.grid(column=0, row=0, sticky=(N, W, E))
fileFrame.columnconfigure(0, weight=1)
fileFrame.rowconfigure(0, weight=1)
ttk.Label(fileFrame, text="Files to sort:").grid(column=0, row=0, sticky=W)


# Init Path input Frame
pathframe = ttk.Frame(fileFrame, padding="3 3 12 12")
pathframe.grid(column=0, row=2, sticky=(W, E))
ttk.Label(pathframe, text="Path: ").grid(column=1, row=0, sticky=W)
ttk.Button(pathframe, text="Browse", command=lambda: pathEntry.insert(0, filedialog.askdirectory())).grid(column=3, row=0, sticky=E)
pathEntry = ttk.Entry(pathframe, width=50)
pathEntry.grid(column=2, row=0, sticky=(W, E))

# Init Sort Path Frame
sortFrame = ttk.Frame(fileFrame, padding="3 3 12 12")
sortFrame.grid(column=0, row=3, sticky=(W, E))
ttk.Label(sortFrame, text="Sort to: ").grid(column=0, row=0, sticky=W)
ttk.Button(sortFrame, text="Browse", command=lambda: sortPath.insert(0, filedialog.askdirectory())).grid(column=2, row=0, sticky=E)
sortPath = ttk.Entry(sortFrame, width=50)
sortPath.grid(column=1, row=0, sticky=(W, E))

# Init Sort Type Frame
settingsFrame = ttk.Frame(app, padding="3 3 12 12")
settingsFrame.grid(column=1, row=0, sticky=(N, W, E, S))
ttk.Label(settingsFrame, text="Sort by:").grid(column=0, row=0, sticky=W)
ttk.Button(settingsFrame, text="Settings", command=lambda: messagebox.showerror("Error", "Settings not implemented yet!")).grid(column=1, row=0, sticky=E)
configFrame = ttk.Frame(settingsFrame, padding="3 3 12 12")
configFrame.grid(column=0, row=1, sticky=(W, E))
ttk.Radiobutton(configFrame, text="Sort by Date Created (Year)", variable=selectedSortType, value="time").grid(column=0, row=0, sticky=W)
ttk.Radiobutton(configFrame, text="Sort by Date Taken (Photos)", variable=selectedSortType, value="photo").grid(column=0, row=1, sticky=W)
#ttk.Radiobutton(configFrame, text="Sort by Name (A-Z)", variable=selectedSortType, value="name").grid(column=0, row=2, sticky=W)

keepOGButton = ttk.Checkbutton(configFrame, text="Keep original files", variable= keepOGFiles, onvalue=True, offvalue=False)
keepOGButton.grid(column=0, row=3, sticky=W)

buttonframe = ttk.Frame(settingsFrame, padding="3 3 12 12")
buttonframe.grid(column=0, row=3, sticky=(S,W,E), columnspan= 2)
ttk.Button(buttonframe, text="Sort", command=lambda: sort()).grid(column=1, row=0, sticky=(E,S))
ttk.Label(buttonframe, text="Copyright © GeraldTM 2022").grid(column=0, row=0, sticky=(W,S))

fileList = tk.Listbox(fileFrame, width=75, height=30, listvariable = fileListValue)
fileList.insert(0,"drop files here")
fileList.drop_target_register(DND_FILES)
fileList.dnd_bind('<<Drop>>', lambda e: datatolist(e.data))
fileList.grid(column=0, row=1, sticky=(N, W, E, S))

def datatolist(data):
    dlist = str(data.replace("{", "").replace("}", ",").replace("'", "").replace('"', "")).split(",")
    iteration = 0
    for e in dlist:
        if (fileList.get(0) == "drop files here"):
            fileList.delete(0)
        fileList.insert(tk.END, e)

def sort():
    if (pathEntry.get() == "" and fileListValue.get() == ""):
        messagebox.showerror("Error", "No files to sort!")
    elif(pathEntry.get() == "" and fileListValue.get() != ""):
        sortByList(fileListValue.get(), sortPath.get())
    elif(pathEntry.get() != "" and fileListValue.get() == ""):
        sortByPath(pathEntry.get(), sortPath.get())
    elif (pathEntry.get() != "" and fileListValue.get() != ""):
        sortByList(fileListValue.get(), sortPath.get())
        sortByPath(pathEntry.get(), sortPath.get())
        

def sortByList(files, pathto):
    if(pathto == ""):
        messagebox.showerror("Error", "No path to sort to!")
        
    else:
        if(selectedSortType.get() == "time"):
            sortByYear(files, pathto)
        elif(selectedSortType.get() == "photo"):
            sortByEXIF()
        elif(selectedSortType.get() == "name"):
            sortByName()
            
def listdirpath(path):
    return [str(os.path.join(path, f)) for f in os.listdir(path)]

def sortByPath(path, pathto):
    files = listdirpath(path)
    if(pathto.get() == ""):
        pathto = pathEntry.get()
    if(selectedSortType.get() == "time"):
        sortByYear(files, pathto)
    elif(selectedSortType.get() == "photo"):
        sortByEXIF(files, pathto)
    elif(selectedSortType.get() == "name"):
        sortByName()




def sortByYear(files, pathto):
    blacklist = []
    # Get sort path

    # get percentage of files
    try:
        progressInterval = 100/len(files)
    except ZeroDivisionError:
        progressInterval = 100
    # Init progress bar
    ttk.Label(sortFrame, text="Sorting: ").grid(column=0, row=0, sticky=W)
    sortProgress = ttk.Progressbar(sortFrame, orient="horizontal", length=200, mode="determinate")
    sortProgress.grid(column=1, row=0, sticky=(W, E))
    # Sort files
    errors = 0
    for file in files:
        print(file)
        try: 
            date = datetime.datetime.fromtimestamp(os.path.getctime(file)).strftime("%Y")
        except PermissionError as e:
            messagebox.showerror("Error", "Permission denied!" + newline + str(e))
            errors += 1
            continue
        
        # Create folder if it doesn't exist
        if pathto + "\\" + date not in blacklist:
            try:
                os.mkdir(pathto + "\\" + date)
            except FileExistsError:
                pass
            except FileNotFoundError:
                try:
                    os.mkdir(pathto)
                    os.mkdir(pathto + "\\" + date)
                except FileNotFoundError as e:
                    messagebox.showerror("Error", "Path not found!" + pathto +newline + e)
                    break
            except PermissionError as e:
                messagebox.showerror("Error", "Permission denied!" + newline + e)
                break
            blacklist.append(pathto + "\\" + date)
            # Move file to folder
        if keepOGFiles.get():
                try:
                    shutil.copy2(file, pathto + "\\" + date + "\\" + os.path.basename(file))
                except PermissionError:
                    try: 
                        shutil.copytree(file, pathto + "\\" + date + "\\" + os.path.basename(file))
                    except shutil.Error as e:
                        messagebox.showerror("Error", "Failed to move file: " + os.path.basename(file) + " to " + pathto + "\\" + date + "\\" + os.path.basename(file) + "newline newline" + str(e))
                        errors += 1
                except shutil.Error as e :
                    messagebox.showerror("Error", "Failed to move file: " + os.path.basename(file) + " to " + pathto + "\\" + date + "\\" + os.path.basename(file) + "newline newline" + str(e))
                    errors += 1
                
        else:    
            try:    
                shutil.move(file, pathto + "\\" + date + "\\" + os.path.basename(file), copy_function= shutil.copy2)
            except shutil.Error as e:
                messagebox.showerror("Error", "Failed to move file: " + os.path.basename(file) + " to " + pathto + "\\" + date + "\\" + os.path.basename(file) + "newline newline" + str(e))
                errors += 1
        sortProgress["value"] += progressInterval
        sortProgress.update()

    # Reset sort to path entry
    ttk.Label(sortFrame, text="Sort to: ").grid(column=0, row=0, sticky=W)
    sortPath = ttk.Entry(sortFrame, width=50)
    sortPath.grid(column=1, row=0, sticky=(W, E))
    #create finished dialog window
    doneWindow = Toplevel(app)
    doneWindow.title("Done!")
    doneFrame = ttk.Frame(doneWindow, padding="3 3 12 12")
    doneFrame.grid(column=3, row=0, sticky=(N, W, E, S))
    doneWindow.columnconfigure(0, weight=1)
    doneWindow.rowconfigure(0, weight=1)
    ttk.Label(doneFrame, text="Sorting Complete! Sorted " + str(len(files)- errors) + " files.").grid(column=0, row=1, sticky=W)
    ttk.Button(doneFrame, text="Close", command=doneWindow.destroy).grid(column=0, row=3, sticky=E)





def sortByEXIF(files, pathto):
    # Get sort path

    blacklist = []
    # get percentage of files
    try:
        progressInterval = 100/len(files)
    except ZeroDivisionError:
        progressInterval = 100
    # Init progress bar
    ttk.Label(sortFrame, text="Sorting: ").grid(column=0, row=0, sticky=W)
    sortProgress = ttk.Progressbar(sortFrame, orient="horizontal", length=200, mode="determinate")
    sortProgress.grid(column=1, row=0, sticky=(W, E))
    # Sort files
    errors = 0
    for file in files:
        #Get photo taken date
        try:
            try: 
                date = datetime.datetime.fromtimestamp(Image.open(file).getexif().get(36867)).strftime("%Y")
            except PermissionError:
                try: 
                    date = datetime.datetime.fromtimestamp(os.path.getctime(file)).strftime("%Y")
                except PermissionError as e:
                    messagebox.showerror("Error", "Permission denied!" + newline + str(e))
                    errors += 1
                    continue
            except TypeError as e:
                #messagebox.showerror("Error", "Error reading EXIF data!" + newline + str(e))
                date = datetime.datetime.fromtimestamp(os.path.getctime(file)).strftime("%Y")

        except UnidentifiedImageError: # If file is not a photo
            try: 
                date = datetime.datetime.fromtimestamp(os.path.getctime(file)).strftime("%Y")
            except PermissionError as e:
                messagebox.showerror("Error", "Permission denied!" + newline + str(e))
                errors += 1
                continue
            blacklist.append(pathto + "\\" + date)
        # Create folder if it doesn't exist
        if pathto + "//" + os.path.basename(file) not in blacklist:
            try:
                os.mkdir(pathto + "\\" + date)
                
            except FileExistsError:
                pass
            except FileNotFoundError:
                try:
                    os.mkdir(pathto)
                    os.mkdir(pathto + "\\" + date)
                except FileNotFoundError as e:
                    messagebox.showerror("Error", "Path not found!" + pathto +newline + e)
                    break
            
            except PermissionError as e:
                messagebox.showerror("Error", "Permission denied!" + newline + e)
                continue

            # Move file to folder
            if keepOGFiles.get():
                try:
                    shutil.copy2(file, pathto + "\\" + date + "\\" + os.path.basename(file))
                except shutil.Error as e :
                    messagebox.showerror("Error", "Failed to move file: " + os.path.basename(file) + " to " + pathto + "\\" + date + "\\" + os.path.basename(file) + "newline newline" + str(e))
                    errors += 1
                except PermissionError as e:
                    messagebox.showerror("Error", "Permission denied!" + newline + str(e))
                    errors += 1
            else:    
                try:    
                    shutil.move(file, pathto + "\\" + date + "\\" + os.path.basename(file), copy_function= shutil.copy2)
                except shutil.Error as e:
                    messagebox.showerror("Error", "Failed to move file: " + os.path.basename(file) + " to " + pathto + "\\" + date + "\\" + os.path.basename(file) + "newline newline" + str(e))
                    errors += 1
                # Update progress bar
            sortProgress["value"] += progressInterval
            sortProgress.update()
        else:
            errors += 1
            sortProgress["value"] += progressInterval
            sortProgress.update()
    # Reset sort to path entry
    ttk.Label(sortFrame, text="Sort to: ").grid(column=0, row=0, sticky=W)
    sortPath = ttk.Entry(sortFrame, width=50)
    sortPath.grid(column=1, row=0, sticky=(W, E))
    #create finished dialog window
    doneWindow = Toplevel(app)
    doneWindow.title("Done!")
    doneFrame = ttk.Frame(doneWindow, padding="3 3 12 12")
    doneFrame.grid(column=3, row=0, sticky=(N, W, E, S))
    doneWindow.columnconfigure(0, weight=1)
    doneWindow.rowconfigure(0, weight=1)
    ttk.Label(doneFrame, text="Sorting Complete! Sorted " + str(len(files)- errors) + " files.").grid(column=0, row=1, sticky=W)
    ttk.Button(doneFrame, text="Close", command=doneWindow.destroy).grid(column=0, row=3, sticky=E)

def sortByName():
    pass

# Run tkinter window
app.mainloop()


        



        