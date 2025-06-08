import os
# Force CPU-only processing and reduce TensorFlow logging verbosity
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import logging
from flask import Flask, render_template, request
from deepface import DeepFace
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Health-check route to confirm the server is running
@app.route("/ping")
def ping():
    return "pong", 200

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    image_path = None
    try:
        if 'image' not in request.files:
            logging.error("No image part in the request.")
            return "لطفاً یک تصویر آپلود کنید", 400

        file = request.files['image']
        if file.filename == '':
            logging.error("Empty filename detected.")
            return "نام فایل معتبر نیست", 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
            logging.info(f"File saved to {image_path}")

            try:
                # Analyze the image with DeepFace while using robust detection settings.
                analysis = DeepFace.analyze(
                    img_path=image_path,
                    actions=["age"],
                    enforce_detection=False,
                    detector_backend="retinaface"
                )
                if isinstance(analysis, list):
                    analysis = analysis[0]
                age = analysis.get("age", None)
                if age is None:
                    raise ValueError("سن تشخیص داده نشد")
                age = int(round(age))
                logging.info(f"Predicted age: {age}")
            except Exception as e:
                logging.error(f"Error during DeepFace analysis: {e}")
                return f"خطا در پردازش تصویر: {str(e)}", 500

            return render_template("result.html", age=age)
        else:
            logging.error("File format not supported.")
            return "فرمت فایل پشتیبانی نمی‌شود", 400
    finally:
        if image_path is not None and os.path.exists(image_path):
            try:
                os.remove(image_path)
                logging.info(f"Removed file: {image_path}")
            except Exception as e:
                logging.error(f"Error removing file: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
