import cv2


def overlay(s_img, l_img, x, y):
    x_offset = x
    y_offset = y
    name = s_img

    if s_img == "harambe.png":
        x_offset -= 30
        y_offset -= 70
    elif s_img == "rickross.png":
        x_offset -= 30
        y_offset -= 115
    elif s_img == "trump.png":
        x_offset -= 60
        y_offset -= 105

    s_img = cv2.imread(s_img, -1)
    try:
        for c in range(0, 3):
            l_img[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1], c] = s_img[:, :, c] * (s_img[:, :, 3] / 255.0) + l_img[y_offset:y_offset + s_img.shape[0],
                                                        x_offset:x_offset + s_img.shape[1], c] * (
                                                        1.0 - s_img[:, :, 3] / 255.0)
        return True
    except Exception, e:
        if name == "harambe.png":
            cv2.putText(l_img, "RIP Harambe!", (x_offset, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        else:
            print e.message
        return False


def harambeface(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.putText(img, "RIP Harambe!", (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 2, 0)
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    success = True
    # Draw a harambe on the faces
    for (x, y, w, h) in faces:
        success = overlay("harambe.png", img, x, y)
    return success


def blockface(img, r, g, b):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x - 20, y - 20), (x + w + 20, y + h + 20), (b, g, r), thickness=cv2.cv.CV_FILLED)


def trumpface(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    success = True
    # Draw a harambe on the faces
    for (x, y, w, h) in faces:
        success = overlay("trump.png", img, x, y)
    return success


def rickrossface(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=15,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    success = True
    # Draw a harambe on the faces
    for (x, y, w, h) in faces:
        success = overlay("rickross.png", img, x, y)
    return success

'''
lastFrame = None
camera = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
mixer.init()
mixer.music.load("rick_ross_push_it.ogg")
mixer.music.play()
while True:
    _, img = camera.read()
    success = rickrossface(img)
    if success:
        mixer.music.unpause()
        #cv2.imshow("win", img)
        #lastFrame = img
    else:
        mixer.music.pause();
        #if lastFrame is not None:
         #   cv2.imshow("win", lastFrame)
        #else:
         #   cv2.imshow("win", img)
    cv2.imshow("win", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
'''