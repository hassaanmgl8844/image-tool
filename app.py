from PIL import Image, ImageEnhance
from rembg import remove
import gradio as gr
import subprocess
import os

def enhance_image(image, sharpness, brightness, contrast):
    img = Image.fromarray(image)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    return img

def remove_background(image):
    img = Image.fromarray(image)
    result = remove(img)
    return result

def crop_image(image, left, top, right, bottom):
    img = Image.fromarray(image)
    cropped = img.crop((left, top, right, bottom))
    return cropped

def convert_image(image, format):
    img = Image.fromarray(image)
    output_path = f"output.{format.lower()}"
    img.save(output_path)
    return output_path

def convert_video(video_path, format):
    output_path = f"output.{format.lower()}"
    subprocess.run([
        "ffmpeg", "-i", video_path,
        "-y", output_path
    ])
    return output_path