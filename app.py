from flask import Flask, render_template, request, redirect, url_for
import os
from deepface import DeepFace

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Ensure this folder exists

def to_persian_num(num):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    return ''.join(persian_digits[int(digit)] for digit in str(num))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    try:
        result = DeepFace.analyze(img_path=file_path, actions=['age'], enforce_detection=False)
        age = result[0]['age']  # Assuming one face is detected
    except Exception as e:
        age = "خطا در تشخیص"
    age_persian = to_persian_num(age) if isinstance(age, int) else age
    os.remove(file_path)
    return render_template('result.html', age=age_persian)

if __name__ == '__main__':
    app.run(debug=True)
