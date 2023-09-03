import cv2
import numpy as np
from modules import morph, helper
import pytesseract
from googletrans import Translator
from bidi.algorithm import get_display


translator = Translator()
 
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def reverse_hebrew_rtl(text):
    # Use the get_display function to convert the text to RTL format
    rtl_text = get_display(text)

    return rtl_text

def show_contours(img, contours):
    # Draw the contours on the contour_img
    contours_img = np.copy(img)
    cv2.drawContours(contours_img, contours, -1, (0, 255, 0), 2)  # Green color, thickness = 2

    # Show the image with the contours
    cv2.imshow('Contours', contours_img)
    cv2.waitKey(0)

def translage_image(image_path, kernel_size):

    img = cv2.imread("input/" + image_path)
    # Convert the image to gray scalse
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    # Blur the image for better result
    blurred = cv2.GaussianBlur(gray, (7, 7), 0) 
    
    # Converting to black and white using OTSU algorithm
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)    

    # Create the kernel
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    
    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Show the image with the contours
    #show_contours(img, contours)
    
    # Creating a copy of image
    im2 = img.copy()
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Open the file in append mode
        file = open("recognized.txt", "a")

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        if text == "":
            continue
        translated = translator.translate(text, src='en',dest='iw').text
        translated = reverse_hebrew_rtl(translated)
        print(text)
        print(translated)
        img = helper.add_text_to_contour(img, translated, cnt)

        file.close

    cv2.imwrite("output/" + image_path, img)
    cv2.imshow("Result",img)
    cv2.waitKey(0)

input_image = "example2.png"
translage_image(input_image, 18)