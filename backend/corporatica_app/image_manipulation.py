from PIL import Image
import os

def resize_image(image_path, output_path, width, height):
    with Image.open(image_path) as img:
        img = img.resize((width, height))
        img.save(output_path)

def crop_image(image_path, output_path, left, top, right, bottom):
    with Image.open(image_path) as img:
        img = img.crop((left, top, right, bottom))
        img.save(output_path)

def convert_image_format(image_path, output_path, format):
    with Image.open(image_path) as img:
        img.save(output_path, format=format)