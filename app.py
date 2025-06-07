from flask import Flask, render_template, request, jsonify
import os
from model import predict_age  # Placeholder for the AI model

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "فایلی انتخاب نشده است."})
        
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "نامعتبر است."})
        
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        
        predicted_age = predict_age(filepath)  # Call AI model
        
        return jsonify({"age": predicted_age, "image": filepath})
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
