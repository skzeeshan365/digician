import os

from flask import Flask, request, render_template, send_from_directory
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from werkzeug.utils import secure_filename

from src.pipeline.predict_pipeline import PredictPipeline

application=Flask(__name__)

app=application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')

    else:
        file = request.files['file']

        if file.filename == '':
            return "No file selected"

        # save uploaded file
        upload_dir = "artifacts/prediction"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, secure_filename(file.filename))
        file.save(file_path)

        clean_path = file_path.replace("\\", "/")
        image_url = f"/{clean_path}"

        print("File saved at:", file_path)

        pipeline = PredictPipeline()

        digit, confidence, inverted = pipeline.predict(file_path)

        results = {
            "digit": digit,
            "confidence": round(confidence, 2),
            "inverted": inverted
        }

        return render_template(
            'home.html',
            results=results, image_url=image_url
        )


@app.route('/artifacts/prediction/<filename>')
def uploaded_file(filename):
    return send_from_directory('artifacts/prediction', filename)


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)        


