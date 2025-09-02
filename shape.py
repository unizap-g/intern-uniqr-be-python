# shape.py
# This module places the QR code on a shaped background filled with a dummy QR pattern.

from PIL import Image, ImageDraw
import qrcode
import random
import string
import math

def apply_circular_shape(qr_image):
    """
    Creates a circular QR code.
    """
    if qr_image is None:
        return None

    qr_width, qr_height = qr_image.size
    
    border_to_crop = 38
    crop_box = (border_to_crop, border_to_crop, qr_width - border_to_crop, qr_height - border_to_crop)
    cropped_qr = qr_image.crop(crop_box)
    
    zoomed_qr = cropped_qr.resize((qr_width, qr_height), Image.Resampling.NEAREST)

    border_size = 120
    dummy_qr_size = qr_width + border_size * 2
    
    dummy_data = ''.join(random.choices(string.ascii_uppercase + string.digits, k=256))
    
    dummy_qr_gen = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    
    dummy_qr_gen.add_data(dummy_data)
    dummy_qr_gen.make(fit=True)
    dummy_qr_img = dummy_qr_gen.make_image(fill_color="black", back_color="white").convert('RGBA')
    dummy_qr_img = dummy_qr_img.resize((dummy_qr_size, dummy_qr_size), Image.Resampling.LANCZOS)

    paste_position = ((dummy_qr_size - qr_width) // 2, (dummy_qr_size - qr_height) // 2)
    dummy_qr_img.paste(zoomed_qr, paste_position, zoomed_qr if zoomed_qr.mode == 'RGBA' else None)

    mask = Image.new('L', (dummy_qr_size, dummy_qr_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, dummy_qr_size, dummy_qr_size), fill=255)

    final_img = Image.new('RGBA', (dummy_qr_size, dummy_qr_size), (255, 255, 255, 0))
    final_img.paste(dummy_qr_img, (0, 0), mask)
    return final_img


def apply_hexagon_shape(qr_image):
    """
    Creates a hexagon-shaped QR code.
    """
    if qr_image is None:
        return None

    qr_width, qr_height = qr_image.size
    
    border_to_crop = 38
    crop_box = (border_to_crop, border_to_crop, qr_width - border_to_crop, qr_height - border_to_crop)
    cropped_qr = qr_image.crop(crop_box)
    zoomed_qr = cropped_qr.resize((qr_width, qr_height), Image.Resampling.NEAREST)

    scale_down_factor = 0.8
    scaled_qr_width = int(qr_width * scale_down_factor)
    scaled_qr_height = int(qr_height * scale_down_factor)
    scaled_qr = zoomed_qr.resize((scaled_qr_width, scaled_qr_height), Image.Resampling.NEAREST)

    border_size = 80
    dummy_qr_size = qr_width + border_size * 2
    dummy_data = ''.join(random.choices(string.ascii_uppercase + string.digits, k=256))
    
    dummy_qr_gen = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    dummy_qr_gen.add_data(dummy_data)
    dummy_qr_gen.make(fit=True)
    dummy_qr_img = dummy_qr_gen.make_image(fill_color="black", back_color="white").convert('RGBA')
    dummy_qr_img = dummy_qr_img.resize((dummy_qr_size, dummy_qr_size), Image.Resampling.LANCZOS)

    paste_position = ((dummy_qr_size - scaled_qr_width) // 2, (dummy_qr_size - scaled_qr_height) // 2)
    dummy_qr_img.paste(scaled_qr, paste_position, scaled_qr if scaled_qr.mode == 'RGBA' else None)

    mask = Image.new('L', (dummy_qr_size, dummy_qr_size), 0)
    draw = ImageDraw.Draw(mask)
    
    center_x, center_y = dummy_qr_size / 2, dummy_qr_size / 2
    radius = dummy_qr_size / 2
    hexagon_points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        x = center_x + radius * math.cos(angle_rad)
        y = center_y + radius * math.sin(angle_rad)
        hexagon_points.append((x, y))
    
    draw.polygon(hexagon_points, fill=255)

    final_img = Image.new('RGBA', (dummy_qr_size, dummy_qr_size), (255, 255, 255, 0))
    final_img.paste(dummy_qr_img, (0, 0), mask)
    return final_img

# This function definition was missing and has been added.
