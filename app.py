from flask import Flask, render_template, request, redirect, url_for, flash
import os
import cv2
import numpy as np
import random

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # حداکثر حجم 16 مگابایت

# ایجاد پوشه آپلود در صورت عدم وجود.
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def dummy_predict_biometrics(image_path):
    """
    تابع شبیه‌سازی جهت پیش‌بینی پارامترهای زیستی و سلامت بر اساس عکس.
    در یک اپلیکیشن واقعی، این تابع با مدل‌های پیش‌بینی جایگزین می‌شود.
    """
    image = cv2.imread(image_path)
    if image is None:
        height, width = 0, 0
    else:
        height, width, _ = image.shape

    age = random.randint(18, 70)
    bmi = round(random.uniform(18.5, 30.0), 1)
    heart_rate = random.randint(60, 100)
    image_quality = random.choice(["عالی", "متوسط", "ضعیف"])

    return {
        "ارتفاع تصویر": f"{height}px" if height > 0 else "نامشخص",
        "عرض تصویر": f"{width}px" if width > 0 else "نامشخص",
        "سن تخمینی": f"{age} سال",
        "شاخص توده بدنی (BMI)": bmi,
        "ضربان قلب": f"{heart_rate} ضربان در دقیقه",
        "کیفیت تصویر": image_quality,
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "photo" not in request.files:
            flash("فایلی در درخواست یافت نشد.")
            return redirect(request.url)
        file = request.files["photo"]
        if file.filename == "":
            flash("فایلی انتخاب نشده است.")
            return redirect(request.url)
        if file:
            filename = file.filename  # در محیط تولید، بهتر است نام فایل‌ها یکتا شود.
            secure_name = os.path.join(app.config["UPLOAD_FOLDER"], os.path.basename(filename))
            file.save(secure_name)
            
            # تولید پیش‌بینی‌های ساختگی
            predictions = dummy_predict_biometrics(secure_name)
            file_url = url_for("static", filename="uploads/" + os.path.basename(filename))
            
            return render_template("result.html", predictions=predictions, file_url=file_url)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
