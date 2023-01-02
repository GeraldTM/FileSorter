# Welcome to FileSorter!
# This program will sort files, the way you want them sorted!
#Copyright © 2022 GeraldTM
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.


import datetime,json, shutil, tkinter as tk, os
from posixpath import abspath

#from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image,UnidentifiedImageError




# Set up tkinter window
app = tk.Tk()
app.title("FileSorter")
app.iconbitmap(True,"icon.ico")
app.resizable(width=False, height=False)

selectedSortType = StringVar()
selectedSortType.set("time")
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
pathEntry = ttk.Entry(pathframe, width=50)
pathEntry.grid(column=2, row=0, sticky=(W, E))

# Init Sort Path Frame
sortFrame = ttk.Frame(fileFrame, padding="3 3 12 12")
sortFrame.grid(column=0, row=3, sticky=(W, E))
ttk.Label(sortFrame, text="Sort to: ").grid(column=0, row=0, sticky=W)
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
ttk.Button(buttonframe, text="Sort", command=lambda: sortByPath(pathEntry.get(), sortPath.get())).grid(column=1, row=0, sticky=(E,S))
ttk.Label(buttonframe, text="Copyright © GeraldTM 2022").grid(column=0, row=0, sticky=(W,S))

def sortByPath(path, pathto):
  
    if(selectedSortType.get() == "time"):
        sortByYear(path, pathto)
    elif(selectedSortType.get() == "photo"):
        sortByEXIF(path, pathto)
    elif(selectedSortType.get() == "name"):
        sortByName()





def sortByYear(path, pathto):
    blacklist = []
    # Get sort path
    files = os.listdir(path)
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
            date = datetime.datetime.fromtimestamp(os.path.getctime(path + "\\" + file)).strftime("%Y")
        except PermissionError as e:
            messagebox.showerror("Error", "Permission denied!" + "\n" + str(e))
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
                    messagebox.showerror("Error", "Path not found!" + pathto +"\n" + e)
                    break
                blacklist.append(pathto + "\\" + date)
                
            except PermissionError as e:
                messagebox.showerror("Error", "Permission denied!" + "\n" + e)
                break
            # Move file to folder
            if keepOGFiles.get():
                try:
                    shutil.copy2(path + "\\" + file, pathto + "\\" + date + "\\" + file)
                except PermissionError:
                    try: 
                        shutil.copytree(path + "\\" + file, pathto + "\\" + date + "\\" + file)
                    except shutil.Error as e:
                        messagebox.showerror("Error", "Failed to move file: " + file + " to " + pathto + "\\" + date + "\\" + file + "\n \n" + str(e))
                        errors += 1
                except shutil.Error as e :
                    messagebox.showerror("Error", "Failed to move file: " + file + " to " + pathto + "\\" + date + "\\" + file + "\n \n" + str(e))
                    errors += 1
                
            else:    
                try:    
                    shutil.move(path + "\\" + file, pathto + "\\" + date + "\\" + file, copy_function= shutil.copy2)
                except shutil.Error as e:
                    messagebox.showerror("Error", "Failed to move file: " + file + " to " + pathto + "\\" + date + "\\" + file + "\n \n" + str(e))
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





def sortByEXIF(path, pathto):
    # Get sort path
    files = os.listdir(path)
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
                date = datetime.datetime.fromtimestamp(Image.open(path + "\\" + file).getexif().get(36867)).strftime("%Y")
            except PermissionError:
                try: 
                    date = datetime.datetime.fromtimestamp(os.path.getctime(path + "\\" + file)).strftime("%Y")
                except PermissionError as e:
                    messagebox.showerror("Error", "Permission denied!" + "\n" + str(e))
                    errors += 1
                    continue
            except TypeError as e:
                #messagebox.showerror("Error", "Error reading EXIF data!" + "\n" + str(e))
                date = datetime.datetime.fromtimestamp(os.path.getctime(path + "\\" + file)).strftime("%Y")

        except UnidentifiedImageError: # If file is not a photo
            try: 
                date = datetime.datetime.fromtimestamp(os.path.getctime(path + "\\" + file)).strftime("%Y")
            except PermissionError as e:
                messagebox.showerror("Error", "Permission denied!" + "\n" + str(e))
                errors += 1
                continue
            blacklist.append(pathto + "\\" + date)
        # Create folder if it doesn't exist
        if pathto + "//" + file not in blacklist:
            try:
                os.mkdir(pathto + "\\" + date)
                
            except FileExistsError:
                pass
            except FileNotFoundError:
                try:
                    os.mkdir(pathto)
                    os.mkdir(pathto + "\\" + date)
                except FileNotFoundError as e:
                    messagebox.showerror("Error", "Path not found!" + pathto +"\n" + e)
                    break
            
            except PermissionError as e:
                messagebox.showerror("Error", "Permission denied!" + "\n" + e)
                continue

            # Move file to folder
            if keepOGFiles.get():
                try:
                    shutil.copy2(path + "\\" + file, pathto + "\\" + date + "\\" + file)
                except shutil.Error as e :
                    messagebox.showerror("Error", "Failed to move file: " + file + " to " + pathto + "\\" + date + "\\" + file + "\n \n" + str(e))
                    errors += 1
                except PermissionError as e:
                    messagebox.showerror("Error", "Permission denied!" + "\n" + str(e))
                    errors += 1
            else:    
                try:    
                    shutil.move(path + "\\" + file, pathto + "\\" + date + "\\" + file, copy_function= shutil.copy2)
                except shutil.Error as e:
                    messagebox.showerror("Error", "Failed to move file: " + file + " to " + pathto + "\\" + date + "\\" + file + "\n \n" + str(e))
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


        



        