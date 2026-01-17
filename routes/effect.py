from flask import Blueprint, render_template, session, send_file
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

effect_bp = Blueprint('effect', __name__)

UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'


@effect_bp.route('/effect/<effect>', methods=['GET'])
def effect_page(effect):
    filename = session.get('filename')

    if not filename:
        return "No image uploaded."

    safe_name = secure_filename(filename)
    name, ext = os.path.splitext(safe_name)

    img_path = os.path.join(UPLOAD_FOLDER, filename)
    img = cv2.imread(img_path)

    if effect == 'gray':
        result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    elif effect == 'bright':
        result = cv2.convertScaleAbs(img, beta=50)

    elif effect == 'dark':
        result = cv2.convertScaleAbs(img, beta=-50)

    elif effect == 'flip':
        result = cv2.flip(img, 1)

    elif effect == 'negative':
        result = 255 - img

    elif effect == 'sepia':
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        result = cv2.transform(img, kernel)

    elif effect == 'sobel':
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sx = cv2.Sobel(g, cv2.CV_64F, 1, 0)
        sy = cv2.Sobel(g, cv2.CV_64F, 0, 1)
        result = cv2.magnitude(sx, sy)

    elif effect == 'sketch':
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        inv = 255 - g
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        result = cv2.divide(g, 255 - blur, scale=256)

    elif effect == 'cartoon':
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(
            g, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 9, 9
        )
        color = cv2.bilateralFilter(img, 9, 250, 250)
        result = cv2.bitwise_and(color, color, mask=edges)

    else:
        return "Invalid effect."

    output_filename = f"{effect}_{name}{ext}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    cv2.imwrite(output_path, result)

    output_url = f"outputs/{output_filename}"

    return render_template(
        'effect.html',
        effect=effect,
        output_image=output_url,
        output_filename=output_filename
    )


@effect_bp.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(file_path, as_attachment=True)
