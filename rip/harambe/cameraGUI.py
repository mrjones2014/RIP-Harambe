import os
import threading
import PIL.Image
import PIL.ImageTk
import Tkinter as tk
from tkFileDialog import askopenfilename
import cv2
import imutils
import FaceSwapper
from pygame import mixer


class imageCapture:
    def __init__(self, vs):
        mixer.init()
        mixer.music.load("rick_ross_push_it.ogg")
        # store the video stream object and output path, then initialize
        # the most recently read frame, thread for reading frames, and
        # the thread stop event
        self.vs = vs
        # self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.IsPaused = False

        # initialize the root window and image panel
        self.root = tk.Tk()
        self.panel = None

        self.mode = 0

        # create a button, that when pressed, will take the current
        # frame and save it to file
        btn = tk.Button(self.root, text="Snapshot!", command=self.takeSnapshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        rickrossbutton = tk.Button(self.root, text="Rick Ross", command=self.rickrossmode)
        trumpbutton = tk.Button(self.root, text="Trump", command=self.trumpmode)
        harambebutton = tk.Button(self.root, text="HARAMBE", command=self.harambemode)

        rickrossbutton.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
        trumpbutton.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
        harambebutton.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        # set a callback to handle when the window is closed
        self.root.wm_title("Face Capture")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def rickrossmode(self):
        self.mode = 1

    def trumpmode(self):
        self.mode = 2

    def harambemode(self):
        self.mode = 3

    def nonemode(self):
        self.mode = 0

    def videoLoop(self):
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 600 pixels
                _, self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=800)

                if self.mode == 1:
                    if self.IsPaused:
                        mixer.music.play()
                        self.IsPaused = False
                    FaceSwapper.rickrossface(self.frame)
                elif self.mode == 2:
                    FaceSwapper.trumpface(self.frame)
                elif self.mode == 3:
                    FaceSwapper.harambeface(self.frame)

                if self.mode != 1:
                    if not self.IsPaused:
                        mixer.music.pause()
                        self.IsPaused = True

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
        print "[INFO] saved image"

    def onClose(self):
        # cleanup the camera, and allow the rest of
        # the quit process to continue
        print "[INFO] closing..."
        self.stopEvent.set()
        self.root.destroy()
        self.root.quit()
        cv2.destroyAllWindows()


def test(prevWin):

    tk.Tk().withdraw()              # we don't want a full GUI, so keep the root window from appearing
    userFile = askopenfilename()    # show an "Open" dialog box and return the path to the selected file
    print userFile


def camCapture(prevWin):
    prevWin.destroy()

    vs = cv2.VideoCapture(0)

    picture = imageCapture(vs)
    picture.root.mainloop()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    window = tk.Tk()
    window.wm_title("Welcome to Face Swapper!")

    filePic = tk.PhotoImage(file="folder.png")
    cameraPic = tk.PhotoImage(file="camera.png")

    fileOption = tk.Button(window, text="Import an Image File", image=filePic, compound="top", command=lambda: test(window))
    fileOption.grid(row=0, column=0, padx=10, pady=10)

    cameraOption = tk.Button(window, text="Take a Picture!", image=cameraPic, compound="top", command=lambda: camCapture(window))
    cameraOption.grid(row=0, column=1, padx=10, pady=10)

    label = tk.Message(window, text="Choose a form of input", width=1000).grid(row=1, columnspan=2)

    window.mainloop()



    print "testing after output"    #this doesn't usually print :/
