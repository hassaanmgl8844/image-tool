from PIL import Image, ImageEnhance
from rembg import remove
import gradio as gr
import subprocess
import os

def enhance_img(img, sharp, bright, cont):
    image = Image.fromarray(img)
    
    # applying enhancements one by one
    image = ImageEnhance.Sharpness(image).enhance(sharp)
    image = ImageEnhance.Brightness(image).enhance(bright)
    image = ImageEnhance.Contrast(image).enhance(cont)
    
    return image


def remove_bg(img):
    image = Image.fromarray(img)
    output = remove(image)
    return output


def crop_img(img, left, top, right, bottom):
    image = Image.fromarray(img)
    
    # pillow crop takes a box tuple
    box = (int(left), int(top), int(right), int(bottom))
    cropped = image.crop(box)
    
    return cropped


def convert_img(img, fmt):
    image = Image.fromarray(img)
    
    fmt = fmt.lower()
    save_path = f"converted_image.{fmt}"
    
    if fmt == "jpg" or fmt == "jpeg":
        image = image.convert("RGB")
    
    image.save(save_path)
    return save_path


def convert_vid(vid_path, fmt):
    fmt = fmt.lower()
    output = f"converted_video.{fmt}"
    
    result = subprocess.run(
        ["ffmpeg", "-i", vid_path, "-y", output],
        capture_output=True
    )
    
    if result.returncode != 0:
        return None
    
    return output