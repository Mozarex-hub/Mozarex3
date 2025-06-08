from flask import Flask, render_template, request
from deepface import DeepFace
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "خطا: هیچ فایلی ارسال نشده است."
    
    file = request.files['file']
    if file.filename == '':
        return "خطا: نام فایل نامعتبر است."
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            result = DeepFace.analyze(img_path=filepath, actions=['age'])
            age = result[0]['age']
        except Exception as e:
            age = "خطا در پردازش تصویر"

        return render_template('result.html', age=age, filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
