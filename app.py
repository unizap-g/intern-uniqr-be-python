# app.py

from flask import Flask, request, jsonify
from logoqr import add_logo, generate_plain_qr
from shape import apply_circular_shape, apply_hexagon_shape
import re
import requests
import base64
import io

app = Flask(__name__)

# Regex for URL validation as per your requirement
URL_REGEX = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
MAX_URL_LENGTH = 2000 # Set a reasonable limit for QR code data

@app.route('/generate-qr', methods=['POST'])
def generate_qr_code():
    """
    API endpoint to generate a QR code based on a JSON payload.
    """
    # --- 1. Input Validation ---
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "Invalid JSON payload provided."}), 400
    except Exception:
        return jsonify({"error": "Could not parse JSON payload."}), 400

    # Validate QRName
    qr_name = payload.get("QRName")
    if not qr_name or not isinstance(qr_name, str):
        return jsonify({"error": "QRName is required and must be a string."}), 400

    # Validate BasicInfo and website URL
    basic_info = payload.get("BasicInfo")
    if not isinstance(basic_info, list) or len(basic_info) == 0:
        return jsonify({"error": "BasicInfo is required and must be a non-empty list."}), 400
    
    website_url = basic_info[0].get("website")
    if not website_url or not isinstance(website_url, str):
        return jsonify({"error": "website is required in BasicInfo and must be a string."}), 400

    if len(website_url) > MAX_URL_LENGTH:
        return jsonify({"error": f"URL length exceeds the maximum limit of {MAX_URL_LENGTH} characters."}), 413

    if not re.match(URL_REGEX, website_url):
        return jsonify({"error": "The provided website URL is not in a valid format."}), 400
    
    # Get Shape and Logo (optional fields)
    shape_list = payload.get("Shape", [])
    logo_url = payload.get("Logo", "")

    # --- 2. Core QR Generation Logic ---
    try:
        # Step A: Handle Logo
        logo_stream = None
        if logo_url and isinstance(logo_url, str):
            try:
                response = requests.get(logo_url, timeout=10)
                response.raise_for_status()
                logo_stream = io.BytesIO(response.content)
            except requests.exceptions.RequestException as e:
                return jsonify({"error": f"Failed to download logo from URL: {e}"}), 500
        
        # Step B: Generate Base QR
        if logo_stream:
            base_qr = add_logo(website_url, logo_stream)
        else:
            base_qr = generate_plain_qr(website_url)
        
        if not base_qr:
            return jsonify({"error": "Failed to generate the base QR code."}), 500

        # Step C: Apply Shape
        final_qr = base_qr
        if isinstance(shape_list, list) and len(shape_list) > 0:
            shape_choice = shape_list[0].lower() if isinstance(shape_list[0], str) else ""
            if shape_choice == 'circle':
                final_qr = apply_circular_shape(base_qr)
            elif shape_choice == 'hexagon':
                final_qr = apply_hexagon_shape(base_qr)
        
        if not final_qr:
            return jsonify({"error": "Failed to apply shape to the QR code."}), 500

        # Step D: Convert final image to Base64
        buffered = io.BytesIO()
        final_qr.save(buffered, format="PNG")
        base64_img_string = base64.b64encode(buffered.getvalue()).decode('utf-8')

    except Exception as e:
        return jsonify({"error": f"An internal error occurred during QR generation: {e}"}), 500

    # --- 3. Format and Return Response ---
    response_data = {
        "name": qr_name,
        "img": base64_img_string
    }
    
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
