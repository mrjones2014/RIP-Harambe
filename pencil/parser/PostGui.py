from __future__ import print_function
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import tkSimpleDialog
from Tkinter import *
import tkFileDialog as fd
import gdata.client, gdata.docs.client, gdata.docs.data, os.path, atom.data
import tkMessageBox







window = Tk("Pencil Parser")

fileString = ''
def copyClipboard(window, fileString):
    window.clipboard_append(fileString)


def saveToLocalFile(fileString):
    file = fd.asksaveasfile()
    file.write(fileString)
    file.close()


def sendToDrive(fileString):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    fileName = tkSimpleDialog.askstring("File Name", "Name of the file?")
    f = drive.CreateFile({'title': fileName + ".txt"})
    f.SetContentString("sup guys.")
    f.Upload()


class PostGui:
    def __init__(self, file):
        print("1")
        self.fileString = file
        window.maxsize(150, 150)
        window.minsize(150, 150)
        window.resizable(width=False, height=False)
    saveFile = Button(window, text="Save to Local File", command=lambda: saveToLocalFile(fileString)).pack()
    saveDocs = Button(window, text="Send to Google Docs", command=lambda: sendToDrive(fileString)).pack()
    clipBoard = Button(window, text="Copy to Clipboard", command=lambda: copyClipboard(fileString)).pack()
    window.mainloop()

















