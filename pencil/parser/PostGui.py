from __future__ import print_function

import tkSimpleDialog
from Tkinter import *
import tkFileDialog as fd
import gdata.client, gdata.docs.client, gdata.docs.data, os.path, atom.data
import tkMessageBox

def saveToLocalFile(fileString):
    file = fd.asksaveasfile()
    file.write("fileString")
    file.close()
def sendToDocs():
    docsclient = gdata.docs.client.DocsClient(source='planzero-gupload-v0.1')

    # Log into Google Docs
    onSuccess = False
    while(onSuccess == False):
        try:
            username = tkSimpleDialog.askstring("Username", "Enter username:")
            password = tkSimpleDialog.askstring("Password", "Enter password:", show='*')
            fileName = tkSimpleDialog.askstring("FileName?", "Enter password:", show='*')
            docsclient.ClientLogin(username, password, docsclient.source);
        except (gdata.client.BadAuthentication, gdata.client.Error), e:
            sys.exit('ERROR: ' + str(e))
        except:
            sys.exit('ERROR: Unable to login')
        onSuccess = True
        print
        'success!'
    uri = 'https://docs.google.com/feeds/upload/create-session/default/private/full'
    fh = open(fileName, 'w')
    fh.write(fileString)
    fh.close()
    file_size = os.path.getsize(fh.name)
    #file_type = magic.Magic(mime=True).from_file(fh.name)
    uploader = gdata.client.ResumableUploader(docsclient, fh, ".txt", file_size, chunk_size=1048576, desired_class=gdata.data.GDEntry)
    new_entry = uploader.UploadFile(uri, entry=gdata.data.GDEntry(title=atom.data.Title(text=os.path.basename(fh.name))))

def copyClipboard(window, fileString):
    window.clipboard_append(fileString)

class PostGui:
    fileString = ''
    def __init__(self, file):

        global fileString
        self.fileString = file

    window = Tk("Pencil Parser")
    window.maxsize( 150,150)
    window.minsize(150, 150)
    window.resizable(width = False, height = False)
    saveFile = Button(window, text="Save to Local File", command=saveToLocalFile(fileString)).pack()
    saveDocs = Button(window, text="Send to Google Docs", command = sendToDocs).pack()
    clipBoard = Button(window, text="Copy to Clipboard", command =  copyClipboard(window, fileString)).pack()

    window.mainloop()













