import os
from PIL import Image, ImageOps


def change_ext(path, new_ext):
    root, _ = os.path.splitext(path)
    new_ext = new_ext if new_ext.startswith('.') else '.' + new_ext
    return root + new_ext 

def pad_image_by_size(input_image, output_image, target_size, color):
    if isinstance(target_size, int):
        new_w = target_size
        new_h = target_size
    elif isinstance(target_size, tuple):
        new_w = target_size[0]
        new_h = target_size[1]
    else:
        raise TypeError('Border is not an integer or tuple!')
    
    with Image.open(input_image) as img:
        img = img.convert('RGB')
        w, h = img.size
        left = (new_w - w) // 2
        top = (new_h - h) // 2
        right = new_w - w - left
        bottom = new_h - h - top
        new_img = ImageOps.expand(img, border=(left, top, right, bottom), fill=color)
        new_img.save(output_image, 'PNG')

def pad_images_by_size(input_dir, output_dir, target_size, color, output_ext):
    files = os.listdir(input_dir)
    for f in files:
        in_path = os.path.join(input_dir, f)
        out_path = change_ext(os.path.join(output_dir, f), output_ext)
        pad_image_by_size(in_path, out_path, target_size, color) 
