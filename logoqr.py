# logoqr.py

from PIL import Image
import qrcode

def generate_plain_qr(data):
    """
    Generates a plain QR code without a logo.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    return qr_img

def add_logo(data, logo_path_or_stream): # Renamed for clarity
    """
    Generates a QR code and embeds a logo in its center.
    Now accepts either a file path or an in-memory file stream.
    """
    qr_img = generate_plain_qr(data)

    try:
        # This line now works for both file paths and file-like objects
        logo_img = Image.open(logo_path_or_stream)
    except Exception as e:
        # Catch generic exceptions for file/stream reading errors
        print(f"Error opening logo image: {e}")
        return None

    # --- Resize and position the logo (logic is unchanged) ---
    qr_width, qr_height = qr_img.size
    max_logo_size = int(qr_width / 4)
    logo_img.thumbnail((max_logo_size, max_logo_size))

    logo_pos = (
        (qr_width - logo_img.size[0]) // 2,
        (qr_height - logo_img.size[1]) // 2
    )
    
    if logo_img.mode == 'RGBA':
        logo_mask = logo_img.split()[3]
        qr_img.paste(logo_img, logo_pos, mask=logo_mask)
    else:
        qr_img.paste(logo_img, logo_pos)

    return qr_img