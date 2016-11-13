from __future__ import print_function

import urllib
import Tkinter as Tk
from urllib2 import Request
import BeautifulSoup as BeautifulSoup
import cStringIO
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import tkSimpleDialog
import tkFileDialog as fd
# from email.mime.text import MIMEText
# import gdata.client, gdata.docs.client, gdata.docs.data, os.path, atom.data
import smtplib
from slacker import Slacker
import slacker
import slackclient
from slackclient import SlackClient
import ntpath
# from sendgrid.helpers import mail
# from sendgrid import *
import email
import email.mime
import re

import os
import shutil

# import gdata.client, gdata.docs.client, gdata.docs.data, os.path, atom.data
# import tkMessageBox

window = Tk.Tk()
window.wm_title("Pencil Parser")

fileString = ''
def exit(window):
    window.quit()

def sendToSlack(fileString, window):
    #ossibleUsers = slack.users.list()
    #possibleUsers = possibleUsers.body['members']
    slackWindow = Tk.Tk()
    slack_client = SlackClient("xoxp-44074671280-84759794208-104528428742-bc1637235e9b43babdece4c797318535")
    slack = Slacker("xoxp-44074671280-84759794208-104528428742-bc1637235e9b43babdece4c797318535")

    channels_call = slack_client.api_call("users.list")
    usersRaw = channels_call['members']
    all_users = re.findall(str("u'real_name_normalized': u'.+?(?=',)"),str(usersRaw) )
    possibleChannels = slack.channels.list()
    userAvatarList = re.findall(str("u'image_32': u'.+?(?=',)"), str(usersRaw))
    curUser = 0
    userAvatar = 0
    var = Tk.IntVar
    for user in all_users:
        userArray = user[27:]
        if "API" in (user):
            continue
        if "image" in user:
            continue

        if "raid" in user:
            continue
        if "slackbot" in user:
            continue
        if "dad" in user:
            continue


        userAvatar = urllib.urlretrieve(userAvatarList[curUser][15:])
        print (userAvatar)

        canvas_width = 80
        canvas_height = 40

        print(curUser)

        c = Tk.Checkbutton(slackWindow, text=userArray)
        # c.grid(row=curUser)
        c.pack()
        curUser = curUser + 1
    listOfUsersToSend = list()
    '''

    for user in userArray:
        if var.get(var) == 1:
            listOfUsersToSend.add(user)
    '''
    submitButton = Tk.Button(slackWindow, text = "Send", command = sendSlackOut(listOfUsersToSend, fileString)).pack()

    #submit



def sendSlackOut(usersSelected, fileString):
    for user in usersSelected:
        #slack.chat.post_message(user, fileString, username='@from_user')
        print(user)



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
    password = tkSimpleDialog.askstring("Email From...", "What's your password for the email at " + youremailusername + "?", show='*')
    server.login(youremailusername, password)

    target = tkSimpleDialog.askstring("Email To...", "What is your target's Email address?")
    server.sendmail(youremailusername, target, fileString)


class PostGui:
    def __init__(self, file):
        self.fileString = file
        window.maxsize(150, 150)
        window.minsize(150, 150)
        window.resizable(width=False, height=False)
    saveFile = Tk.Button(window, text="Save to Local File", command=lambda: saveToLocalFile(fileString)).pack()
    saveDrive = Tk.Button(window, text="Send to Google Drive", command=lambda: sendToDrive(fileString)).pack()
    clipBoard = Tk.Button(window, text="Copy to Clipboard", command=lambda: copyClipboard(fileString)).pack()
    emailFile = Tk.Button(window, text="Email/SMTP", command =lambda: emailFile(fileString)).pack()
    sendToSlack = Tk.Button(window, text="Upload to Slack!", command = lambda: sendToSlack(fileString, window)).pack()
    exit = Tk.Button(window, text = "Exit", command = lambda: exit(window)).pack()
    window.mainloop()

















