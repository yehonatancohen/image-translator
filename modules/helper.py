import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def find_best_matching_font_size(image_path, text, font_name="arial.ttf"):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    best_font_size = 1
    best_score = float('inf')

    for font_size in range(1, 100):
        font = ImageFont.truetype(font_name, size=font_size)
        text_width, text_height = draw.textsize(text, font=font)

        # Calculate the score based on the difference in text height between the image and the rendered text
        score = abs(text_height - image.height)

        if score < best_score:
            best_score = score
            best_font_size = font_size

    return best_font_size, best_score

def add_text_with_best_matching_font(image_path, text, font_name="arial.ttf"):
    best_font_size, _ = find_best_matching_font_size(image_path, text, font_name)

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_name, size=best_font_size)

    # Calculate the position to center the text in the image
    text_width, text_height = draw.textsize(text, font=font)
    image_width, image_height = image.size
    x = (image_width - text_width) // 2
    y = (image_height - text_height) // 2

    draw.text((x, y), text, fill=(0, 0, 0), font=font)

    # Convert PIL image to OpenCV format
    cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    return cv2_image
