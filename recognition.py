import cv2
import imutils
import easyocr

def applyFilters(image):
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray=cv2.bilateralFilter(gray,11,17,17)
    edged=cv2.Canny(gray,170,200)
    return edged

def findContours(image, resizeScale):
    resized = imutils.resize(image, width = int(len(image[0]) * resizeScale), height = int(len(image) * resizeScale))
    edged = applyFilters(resized.copy())
    contours, _ = cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:100]
    contours_scaled = []
    for contour in contours:
        contour_scaled = (contour / resizeScale).astype(int)
        contours_scaled.append(contour_scaled)
    return contours_scaled

def findRectangles(image, contours):
    rectangles = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02*perimeter, True)
        if(len(approx) == 4):
            x , y , w , h = cv2.boundingRect(contour)
            croped_image = image[y:y+h,x:x+w]
            rectangles += [croped_image]
    return rectangles

def readPlates(plates):
    reader = easyocr.Reader(['en'])
    texts = []
    for plate in plates[:1]:
        texts += reader.readtext(plate)
    return texts