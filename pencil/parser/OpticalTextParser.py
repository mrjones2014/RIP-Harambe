try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import cv2
import imutils
import numpy as np


def compute_skew(image):
    image = cv2.bitwise_not(image)
    height, width = image.shape

    edges = cv2.Canny(image, 150, 200, 3, 5)
    lines = cv2.HoughLinesP(edges, 1, cv2.cv.CV_PI/180, 100, minLineLength=width / 2.0, maxLineGap=20)
    if lines is None:
        return 0
    angle = 0.0
    nlines = lines.size
    for x1, y1, x2, y2 in lines[0]:
        angle += np.arctan2(y2 - y1, x2 - x1)
    return angle / nlines


def deskew(image, angle):
    image = cv2.bitwise_not(image)
    non_zero_pixels = cv2.findNonZero(image)
    center, wh, theta = cv2.minAreaRect(non_zero_pixels)

    root_mat = cv2.getRotationMatrix2D(center, angle, 1)
    rows, cols = image.shape
    rotated = cv2.warpAffine(image, root_mat, (cols, rows), flags=cv2.INTER_CUBIC)

    return cv2.getRectSubPix(rotated, (cols, rows), center)


camera = cv2.VideoCapture(0)

while True:
    (grabbed, img) = camera.read()
    img = imutils.resize(img, width=900)
    cv2.imshow("img", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        deskewed = deskew(img_grayscale.copy(), compute_skew(img_grayscale))
        img_gaussian_blurred = cv2.GaussianBlur(deskewed, (5, 5), 0)
        ret, img_thresholded = cv2.threshold(img_grayscale, 90, 255, cv2.THRESH_BINARY_INV)
        cv2_img = Image.fromarray(img_thresholded)
        print(pytesseract.image_to_string(cv2_img))
        cv2.imshow("thresholded image", img_thresholded)
camera.release()
cv2.destroyAllWindows()
cv2.waitKey(1)