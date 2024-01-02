import cv2
import imutils   # to resize our images
import pytesseract
from recognition import *

image = cv2.imread('real.jpeg')
contours = findContours(image, 0.5)
rectangles = findRectangles(image, contours)
texts = readPlates(rectangles)
print(texts)
exit()

cnts,new=cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
image1 = image.copy()
cv2.drawContours(image1,cnts,-1,(0,255,0),3)

cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:10]
NumberPlateCount=None
image2=image.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),3)
cv2.imshow("Top 30 Contours",image2)
cv2.waitKey(0)

quadrilaterals = list()
for i in cnts:
    perimeter=cv2.arcLength(i,True)
    approx=cv2.approxPolyDP(i,0.02*perimeter,True)
    
    if(len(approx)>=4):
        #now we will crop that rectangle part
        x , y , w , h = cv2.boundingRect(i)
        crp_img=image[y:y+h,x:x+w]
        quadrilaterals += [crp_img]

texts = list()
for i in quadrilaterals:
    texts += [pytesseract.image_to_string(i,lang='eng')]
    cv2.imshow("",i)
    cv2.waitKey(0)


print("Texts: ", texts)