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


css = """
.gradio-container {
    background-color: #0d0d0d !important;
    max-width: 920px !important;
    margin: 0 auto !important;
    font-family: 'Segoe UI', sans-serif;
}
h1 { color: #e0e0e0 !important; font-size: 26px !important; font-weight: 600 !important; }
h3 { color: #777777 !important; font-size: 13px !important; font-weight: 400 !important; }
.section { color: #bbbbbb; font-size: 15px; font-weight: 500; border-left: 3px solid #444; padding-left: 10px; margin: 30px 0 12px 0; }
button { background-color: #1e1e1e !important; color: #cccccc !important; border: 1px solid #333 !important; border-radius: 6px !important; }
button:hover { background-color: #2a2a2a !important; border-color: #555 !important; }
footer { display: none !important; }
"""

css = """
.gradio-container {
    background-color: #0d0d0d !important;
    max-width: 920px !important;
    margin: 0 auto !important;
    font-family: 'Segoe UI', sans-serif;
}
h1 { color: #e0e0e0 !important; font-size: 26px !important; font-weight: 600 !important; }
h3 { color: #777777 !important; font-size: 13px !important; font-weight: 400 !important; }
.section { color: #bbbbbb; font-size: 15px; font-weight: 500; border-left: 3px solid #444; padding-left: 10px; margin: 30px 0 12px 0; }
button { background-color: #1e1e1e !important; color: #cccccc !important; border: 1px solid #333 !important; border-radius: 6px !important; }
button:hover { background-color: #2a2a2a !important; border-color: #555 !important; }
footer { display: none !important; }
"""

with gr.Blocks(css=css, theme=gr.themes.Base()) as app:

    gr.Markdown("# QuickEdit")
    gr.Markdown("### image and video tools — all in one place")

    # enhancer
    gr.Markdown("<div class='section'>Image Enhancer</div>")
    with gr.Row():
        with gr.Column():
            enh_in     = gr.Image(label="upload image")
            sharp      = gr.Slider(0.5, 3.0, value=1.0, step=0.1, label="sharpness")
            bright     = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="brightness")
            cont       = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="contrast")
            enh_btn    = gr.Button("enhance")
        with gr.Column():
            enh_out    = gr.Image(label="result")
    enh_btn.click(fn=enhance_img, inputs=[enh_in, sharp, bright, cont], outputs=enh_out)

    # bg remover
    gr.Markdown("<div class='section'>Background Remover</div>")
    with gr.Row():
        with gr.Column():
            bg_in      = gr.Image(label="upload image")
            bg_btn     = gr.Button("remove background")
        with gr.Column():
            bg_out     = gr.Image(label="result")
    bg_btn.click(fn=remove_bg, inputs=bg_in, outputs=bg_out)

    # crop
    gr.Markdown("<div class='section'>Image Crop</div>")
    with gr.Row():
        with gr.Column():
            crop_in    = gr.Image(label="upload image")
            with gr.Row():
                l      = gr.Number(label="left",   value=0)
                t      = gr.Number(label="top",    value=0)
            with gr.Row():
                r      = gr.Number(label="right",  value=500)
                b      = gr.Number(label="bottom", value=500)
            crop_btn   = gr.Button("crop")
        with gr.Column():
            crop_out   = gr.Image(label="result")
    crop_btn.click(fn=crop_img, inputs=[crop_in, l, t, r, b], outputs=crop_out)

    # image converter
    gr.Markdown("<div class='section'>Image Converter</div>")
    with gr.Row():
        with gr.Column():
            cimg_in    = gr.Image(label="upload image")
            img_fmt    = gr.Dropdown(choices=["PNG", "JPG", "WEBP", "BMP"], value="PNG", label="convert to")
            cimg_btn   = gr.Button("convert")
        with gr.Column():
            cimg_out   = gr.File(label="download")
    cimg_btn.click(fn=convert_img, inputs=[cimg_in, img_fmt], outputs=cimg_out)

    # video converter
    gr.Markdown("<div class='section'>Video Converter</div>")
    with gr.Row():
        with gr.Column():
            cvid_in    = gr.Video(label="upload video")
            vid_fmt    = gr.Dropdown(choices=["mp4", "avi", "mov", "gif"], value="mp4", label="convert to")
            cvid_btn   = gr.Button("convert")
        with gr.Column():
            cvid_out   = gr.File(label="download")
    cvid_btn.click(fn=convert_vid, inputs=[cvid_in, vid_fmt], outputs=cvid_out)

if __name__ == "__main__":
    app.launch()