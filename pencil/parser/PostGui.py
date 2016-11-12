from __future__ import print_function
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import tkSimpleDialog
from Tkinter import *
import tkFileDialog as fd
from email.mime.text import MIMEText
import gdata.client, gdata.docs.client, gdata.docs.data, os.path, atom.data
import tkMessageBox
import smtplib
from sendgrid.helpers import mail
from sendgrid import *





# import gdata.client, gdata.docs.client, gdata.docs.data, os.path, atom.data
# import tkMessageBox

window = Tk()
window.wm_title("Pencil Parser")

fileString = ''
def copyClipboard(fileString):
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
    f.SetContentString(fileString)
    f.Upload()
def emailFile(fileString):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    youremailusername = tkSimpleDialog.askstring("Email From...", "What is your Email address?")
    password = tkSimpleDialog.askstring("Email From...", "What's your password for the email at " + youremailusername +"?")
    server.login(youremailusername, password)

    target = tkSimpleDialog.askstring("Email From...", "What is your target's Email address?")
    server.sendmail(youremailusername, target, fileString)


class PostGui:
    def __init__(self, file):
        self.fileString = file
        window.maxsize(150, 150)
        window.minsize(150, 150)
        window.resizable(width=False, height=False)
    saveFile = Button(window, text="Save to Local File", command=lambda: saveToLocalFile(fileString)).pack()
    saveDrive = Button(window, text="Send to Google Docs", command=lambda: sendToDrive(fileString)).pack()
    clipBoard = Button(window, text="Copy to Clipboard", command=lambda: copyClipboard(fileString)).pack()
    emailFile = Button(window, text="Email/SMTP", command =lambda: emailFile(fileString)).pack()
    window.mainloop()

















