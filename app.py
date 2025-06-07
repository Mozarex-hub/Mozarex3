from flask import Flask, render_template, request, redirect, url_for
import os
import random
import string
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")

# ایجاد پوشه آپلود در صورت عدم وجود
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_age_from_image(image_path):
    """
    تابع جایگزین برای پیش‌بینی سن بیولوژیکی.
    اینجا می‌توانید مدل یادگیری ماشین یا الگوریتم پیشرفته خود را جایگزین کنید.
    در این نمونه، یک عدد تصادفی بین 20 تا 70 را برگردانیم.
    """
    return random.randint(20, 70)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'photo' not in request.files:
        return redirect(request.url)
    
    file = request.files['photo']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # ایجاد یک نام یکتا برای فایل
        name, ext = os.path.splitext(filename)
        unique_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        filename = f"{name}_{unique_suffix}{ext}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        
        predicted_age = predict_age_from_image(filepath)
        return render_template('result.html', predicted_age=predicted_age, filename=filename)
    
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
