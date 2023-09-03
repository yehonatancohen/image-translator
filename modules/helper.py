import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def add_text_to_image_cv2(image, text, position, contour=None, font=cv2.FONT_HERSHEY_SIMPLEX,
                          font_color=(255, 255, 255), font_thickness=1, background_color=(255, 255, 255)):
    # Copy the input image
    result = image.copy()

    # Convert the image to PIL format
    pil_image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)

    # Create a PIL font object (you can specify the font and size here)
    font_size = 1
    font = ImageFont.truetype("arial.ttf", font_size)
    
    # Calculate the size of the text with the given font
    text_size = draw.textsize(text, font=font)

    # Extract width and height from the position tuple
    x, y, width, height = position

    # Determine the scaling factor to fit the text within the desired size
    scaling_factor = min(width / text_size[0], height / text_size[1])
    font_size = int(font_size * scaling_factor * 2)

    # Create the font with the adjusted size
    font = ImageFont.truetype("arial.ttf", font_size)

    # Calculate the position to place the text
    text_x, text_y = x, y

    # Add the text to the PIL image
    
    left, top, right, bottom = draw.textbbox((text_x, text_y), text, font=font)
    draw.rectangle((left-5, top-5, right+5, bottom+5), fill="white")
    draw.text((text_x, text_y), text, font=font, fill=font_color)

    # Convert the PIL image back to OpenCV format
    result = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    return result

def add_text_to_contour(image, text, contour):
    result = image.copy()
    x, y, w, h = cv2.boundingRect(contour)
    text_x = x 
    text_y = y - h // 2
    font_color = (0, 0, 0)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 4

    result = add_text_to_image_cv2(result, text, (text_x, text_y, w, h), contour, font, font_color, font_thickness)

    return result