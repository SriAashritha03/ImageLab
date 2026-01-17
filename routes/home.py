from flask import Blueprint, render_template, request, session
import os
import time
from werkzeug.utils import secure_filename

home_bp = Blueprint('home', __name__)
UPLOAD_FOLDER = 'static/uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files.get('image')
        if file:
            safe_name = secure_filename(file.filename)

            # 🔥 make filename unique every time
            unique_name = f"{int(time.time())}_{safe_name}"

            save_path = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(save_path)

            # store unique filename in session
            session['filename'] = unique_name

    return render_template('home.html')
