import os
import threading
import PIL.Image
import PIL.ImageTk
import Tkinter as tk
from Tkinter import *
import cv2
import imutils


class imageCapture:
    def __init__(self, vs):
        # store the video stream object and output path, then initialize
        # the most recently read frame, thread for reading frames, and
        # the thread stop event
        self.vs = vs
        # self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None

        # initialize the root window and image panel
        self.root = tk.Tk()
        self.panel = None

        # create a button, that when pressed, will take the current
        # frame and save it to file
        btn = tk.Button(self.root, text="Snapshot!", command=self.takeSnapshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        # set a callback to handle when the window is closed
        self.root.wm_title("Pencil Parser Capture")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 600 pixels
                _, self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=600)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = PIL.Image.fromarray(image)
                image = PIL.ImageTk.PhotoImage(image)

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)

                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError, e:
            print("[INFO] caught a RuntimeError")


    def takeSnapshot(self):
        filename = "output.png"
        # path = os.path.abspath(self)
        # print path
        # p = os.path.sep.join(filename)

        # save the file
        cv2.imwrite(filename, self.frame.copy())
        print "[INFO] saved test image"

    def onClose(self):
        # cleanup the camera, and allow the rest of
        # the quit process to continue
        print "[INFO] closing..."
        self.stopEvent.set()
        self.root.destroy()
        self.root.quit()
        cv2.destroyAllWindows()


def test(prevWin):
    print "testing file import next"


def camCapture(prevWin):
    prevWin.destroy()

    vs = cv2.VideoCapture(0)

    picture = imageCapture(vs)
    picture.root.mainloop()

    cv2.destroyAllWindows()

window = tk.Tk()
window.wm_title("Welcome to Pencil Parser!")

fileOption = tk.Button(window, text="Import an Image File", command=lambda: test(window))
fileOption.pack(side="left", expand="yes", padx=10, pady=10)

cameraOption = tk.Button(window, text="Take a Picture!", command=lambda: camCapture(window))
cameraOption.pack(side="left", expand="yes", padx=10, pady=10)

window.mainloop()



print "testing after output"
