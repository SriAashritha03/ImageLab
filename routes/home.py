from flask import Blueprint, render_template, request, session
import os

os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/outputs", exist_ok=True)

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
