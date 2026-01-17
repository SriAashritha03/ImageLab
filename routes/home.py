from flask import Blueprint, render_template, request, session
import os

home_bp = Blueprint('home', __name__)
UPLOAD_FOLDER = 'static/uploads'


@home_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files.get('image')
        if file:
            save_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(save_path)
            session['filename'] = file.filename

    return render_template('home.html')
