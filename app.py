from PIL import Image, ImageEnhance
from rembg import remove
import gradio as gr
import subprocess
import os


def enhance_img(img, sharp, bright, cont):
    image = Image.fromarray(img)
    image = ImageEnhance.Sharpness(image).enhance(sharp)
    image = ImageEnhance.Brightness(image).enhance(bright)
    image = ImageEnhance.Contrast(image).enhance(cont)
    return image


def remove_bg(img):
    image = Image.fromarray(img)
    output = remove(image)
    return output


def crop_img(img, left_pct, top_pct, right_pct, bottom_pct):
    if img is None:
        return None
    image = Image.fromarray(img)
    w, h = image.size

    left   = int(w * left_pct   / 100)
    top    = int(h * top_pct    / 100)
    right  = int(w * right_pct  / 100)
    bottom = int(h * bottom_pct / 100)

    if right <= left or bottom <= top:
        return image

    return image.crop((left, top, right, bottom))


def convert_img(img, fmt):
    if img is None:
        return None
    image = Image.fromarray(img)
    fmt = fmt.lower()
    save_path = f"converted_image.{fmt}"
    if fmt in ("jpg", "jpeg"):
        image = image.convert("RGB")
    image.save(save_path)
    return save_path


def convert_vid(vid_path, fmt):
    if vid_path is None:
        return None
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
.crop-hint { color: #555555; font-size: 12px; margin-bottom: 10px; }
button { background-color: #1e1e1e !important; color: #cccccc !important; border: 1px solid #333 !important; border-radius: 6px !important; }
button:hover { background-color: #2a2a2a !important; border-color: #555 !important; }
footer { display: none !important; }
"""

with gr.Blocks(css=css, theme=gr.themes.Base()) as app:

    gr.Markdown("# QuickEdit")
    gr.Markdown("### image and video tools — all in one place")

    # ── Image Enhancer ──────────────────────────────────────────
    gr.Markdown("<div class='section'>Image Enhancer</div>")
    with gr.Row():
        with gr.Column():
            enh_in  = gr.Image(label="Upload Image")
            sharp   = gr.Slider(0.5, 3.0, value=1.0, step=0.1, label="Sharpness  (1 = original)")
            bright  = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="Brightness  (1 = original)")
            cont    = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="Contrast  (1 = original)")
            enh_btn = gr.Button("Enhance")
        with gr.Column():
            enh_out = gr.Image(label="Result")
    enh_btn.click(fn=enhance_img, inputs=[enh_in, sharp, bright, cont], outputs=enh_out)

    # ── Background Remover ──────────────────────────────────────
    gr.Markdown("<div class='section'>Background Remover</div>")
    with gr.Row():
        with gr.Column():
            bg_in  = gr.Image(label="Upload Image")
            bg_btn = gr.Button("Remove Background")
        with gr.Column():
            bg_out = gr.Image(label="Result")
    bg_btn.click(fn=remove_bg, inputs=bg_in, outputs=bg_out)

    # ── Image Crop ──────────────────────────────────────────────
    gr.Markdown("<div class='section'>Image Crop</div>")
    gr.Markdown("<div class='crop-hint'>💡 All sliders are in % of the image. Left & Top = where crop starts. Right & Bottom = where crop ends. Default = full image.</div>")
    with gr.Row():
        with gr.Column():
            crop_in    = gr.Image(label="Upload Image")
            left_pct   = gr.Slider(0,  100, value=0,   step=1, label="Left — crop start from left (0% = left edge)")
            top_pct    = gr.Slider(0,  100, value=0,   step=1, label="Top — crop start from top (0% = top edge)")
            right_pct  = gr.Slider(0,  100, value=100, step=1, label="Right — crop end from left (100% = right edge)")
            bottom_pct = gr.Slider(0,  100, value=100, step=1, label="Bottom — crop end from top (100% = bottom edge)")
            crop_btn   = gr.Button("Crop")
        with gr.Column():
            crop_out = gr.Image(label="Result")
    crop_btn.click(fn=crop_img, inputs=[crop_in, left_pct, top_pct, right_pct, bottom_pct], outputs=crop_out)

    # ── Image Converter ─────────────────────────────────────────
    gr.Markdown("<div class='section'>Image Converter</div>")
    with gr.Row():
        with gr.Column():
            cimg_in  = gr.Image(label="Upload Image")
            img_fmt  = gr.Dropdown(choices=["PNG", "JPG", "WEBP", "BMP"], value="PNG", label="Convert To")
            cimg_btn = gr.Button("Convert")
        with gr.Column():
            cimg_out = gr.File(label="Download")
    cimg_btn.click(fn=convert_img, inputs=[cimg_in, img_fmt], outputs=cimg_out)

    # ── Video Converter ─────────────────────────────────────────
    gr.Markdown("<div class='section'>Video Converter</div>")
    with gr.Row():
        with gr.Column():
            cvid_in  = gr.Video(label="Upload Video")
            vid_fmt  = gr.Dropdown(choices=["mp4", "avi", "mov", "gif"], value="mp4", label="Convert To")
            cvid_btn = gr.Button("Convert")
        with gr.Column():
            cvid_out = gr.File(label="Download")
    cvid_btn.click(fn=convert_vid, inputs=[cvid_in, vid_fmt], outputs=cvid_out)


if __name__ == "__main__":
    app.launch()