from flask import Flask, render_template, request, redirect, url_for, flash
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Maximum file size 16 MB

# Ensure the upload directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Try to load the biologic age prediction model
try:
    bio_age_model = load_model("models/biologic_age_model.h5")
    model_loaded = True
    print("مدل سن بیولوژیکی با موفقیت بارگذاری شد.")
except Exception as e:
    print("خطا در بارگذاری مدل:", e)
    model_loaded = False

def preprocess_image(image_path, target_size=(64, 64)):
    """
    Loads and preprocesses the image: resize, normalize, and add batch dimension.
    """
    image = cv2.imread(image_path)
    if image is None:
        return None
    image = cv2.resize(image, target_size)
    image = image.astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def predict_biologic_age(image_path):
    """
    Uses the loaded model (or a dummy alternative) to predict the biologic age from an image.
    """
    preprocessed = preprocess_image(image_path)
    if preprocessed is None:
        return {"خطا": "بارگذاری تصویر با مشکل مواجه شد."}
    
    if model_loaded:
        age_pred = bio_age_model.predict(preprocessed)[0][0]
        bio_age = round(float(age_pred), 1)
        predictions = {"سن بیولوژیکی": f"{bio_age} سال"}
    else:
        # Fallback dummy prediction if the model is not available
        import random
        dummy_age = random.randint(30, 80)
        predictions = {"سن بیولوژیکی": f"{dummy_age} سال (مقدار ساختگی)"}
    return predictions

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "photo" not in request.files:
            flash("فایلی در درخواست یافت نشد.", "warning")
            return redirect(request.url)
        file = request.files["photo"]
        if file.filename == "":
            flash("فایلی انتخاب نشده است.", "warning")
            return redirect(request.url)
        
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        
        # Predict biologic age and generate the file URL for display
        predictions = predict_biologic_age(filepath)
        file_url = url_for("static", filename="uploads/" + filename)
        return render_template("result.html", predictions=predictions, file_url=file_url)
    
    # Render the futuristic index page
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
