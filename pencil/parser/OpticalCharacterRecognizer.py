from files import ImageFile
from segmentation import ContourSegmenter, draw_segments
from feature_extraction import SimpleFeatureExtractor
from classification import KNNClassifier
from ocr import OCR, accuracy, show_differences, reconstruct_chars
import cv2

segmenter =  ContourSegmenter( blur_y=5, blur_x=5, block_size=11, c=10)
extractor =  SimpleFeatureExtractor( feature_size=10, stretch=False )
classifier = KNNClassifier()
ocr = OCR( segmenter, extractor, classifier )

ocr.train(ImageFile('letters1'))
'''
camera = cv2.VideoCapture(0)
captured_img = None
while True:
    (ret, captured_img) = camera.read()
    cv2.imshow("captured image", captured_img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        break

cv2.imwrite("data/captured.png", captured_img)
cv2.destroyAllWindows()
camera.release()
'''
test_image = ImageFile('captured')
test_classes, test_segments = ocr.ocr(test_image)

print "accuracy:", accuracy(test_image.ground.classes, test_classes)
print "OCRed text:\n", reconstruct_chars(test_classes)
show_differences(test_image.image, test_segments, test_image.ground.classes, test_classes)

