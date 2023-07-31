from modules import helper
import cv2
image_path = "image.png"
text = "Hello, PIL!"
font_name = "arial.ttf"

im = helper.add_text_with_best_matching_font(image_path, text, font_name)
cv2.imshow("test",im)
cv2.waitKey(0)