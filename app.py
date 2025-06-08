from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
from deepface import DeepFace

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'photo' not in request.files:
            # اگر فایل پیدا نشد، صفحه را مجدداً بارگذاری می‌کنیم
            return redirect(request.url)
        file = request.files["photo"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            # ایجاد یک نام فایل یکتا برای ذخیره عکس
            file_ext = os.path.splitext(file.filename)[1]
            filename = str(uuid.uuid4()) + file_ext
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            try:
                # استفاده از DeepFace برای تحلیل عکس و استخراج سن
                analysis = DeepFace.analyze(img_path=file_path, actions=['age'])
                prediction = analysis.get("age", "نامشخص")
            except Exception as e:
                prediction = "خطا در پیش‌بینی"
            return render_template("result.html", prediction=prediction)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
