import os
import re
import requests

from flask import Flask, request, render_template, send_from_directory, jsonify, redirect
from werkzeug.utils import secure_filename

from src.pipeline.predict_pipeline import PredictPipeline
from supabase_client import supabase

application = Flask(__name__)
app = application


# ---------------- CONFIG ----------------
SUPABASE_URL = "https://bpcvatwasmuunonabhuo.supabase.co"


# ---------------- AUTH VERIFY ----------------
def get_user_from_token():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]

    try:
        res = requests.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        if res.status_code != 200:
            return None

        return res.json()

    except Exception:
        return None


def require_auth():
    user = get_user_from_token()
    if not user:
        return False
    return True


# ---------------- ROUTES ----------------

@app.route('/')
def index():
    # frontend will send token via header (if exists)
    user = get_user_from_token()

    if user:
        return redirect("/predict")

    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    if not require_auth():
        return redirect("/")

    if request.method == 'GET':
        return render_template('home.html')

    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    upload_dir = "artifacts/prediction"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, secure_filename(file.filename))
    file.save(file_path)

    clean_path = file_path.replace("\\", "/")
    image_url = f"/{clean_path}"

    pipeline = PredictPipeline()
    digit, confidence, inverted = pipeline.predict(file_path)

    results = {
        "digit": digit,
        "confidence": round(confidence, 2),
        "inverted": inverted
    }

    return render_template(
        'home.html',
        results=results,
        image_url=image_url
    )


@app.route('/artifacts/prediction/<filename>')
def uploaded_file(filename):
    return send_from_directory('artifacts/prediction', filename)


# ---------------- LOGIN ----------------

ALLOWED_DOMAINS = {"gmail.com", "yourcompany.com"}

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email required"}), 400

    match = re.match(r"[^@]+@([^@]+)", email)
    if not match:
        return jsonify({"message": "Invalid email"}), 400

    domain = match.group(1)

    if domain not in ALLOWED_DOMAINS:
        return jsonify({"message": "Unauthorized email domain"}), 403

    try:
        supabase.auth.sign_in_with_otp({
            "email": email,
            "options": {
                "email_redirect_to": request.host_url
            }
        })

        return jsonify({"message": "Magic link sent"})

    except Exception as e:
        return jsonify({"message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)