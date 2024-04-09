import base64
import pyvips
import glob
import os

def convert_svg_to_png(svg_file, png_file):
    image = pyvips.Image.new_from_file(svg_file, dpi=100)
    image.write_to_file(png_file)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def delete_files_in_folder(folder_path):
    files = glob.glob(folder_path + '/*')
    for f in files:
        os.remove(f)
