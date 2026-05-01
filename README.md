# 🎯 Digit Recognition System (ML + Flask + AWS ECS)

## 📌 Overview

This project is a digit recognition system powered by a trained CNN model.
Users can upload an image of a handwritten digit, and the system predicts the digit along with a confidence score.

The system includes:

* Modular ML pipeline (training and inference)
* Flask-based web application
* Supabase authentication (OTP / magic link)
* Deployment on AWS ECS with Application Load Balancer and SSL

---

## 🚀 Features

### 🔢 Digit Prediction

* CNN model (`mnist_cnn.keras`)
* Outputs:

  * Predicted digit
  * Confidence score
  * Inversion flag (if preprocessing was applied)

---

### 🔐 Authentication

* Supabase OTP (magic link login)
* Domain-based access control:

  * `csmu.ac.in` → allowed
  * Gmail → restricted to whitelisted users

---

### 🧱 ML Pipeline

```
src/
├── components/
│   ├── data_ingestion.py
│   ├── data_transformation.py
│   └── model_trainer.py
│
├── pipeline/
│   ├── train_pipeline.py
│   └── predict_pipeline.py
```

---

## 🗂️ Project Structure

```
digician/
│
├── artifacts/
│   ├── mnist_cnn.keras
│   └── prediction/
│
├── src/
├── templates/
│   ├── index.html
│   └── home.html
│
├── app.py
├── supabase_client.py
├── Dockerfile
├── requirements.txt
└── .github/workflows/deploy.yml
```

---

## ⚙️ Tech Stack

* Python 3.13
* Flask
* TensorFlow / Keras
* Supabase (Authentication)
* AWS ECS (Fargate)
* Application Load Balancer
* AWS ACM (SSL)
* GitHub Actions (CI/CD)

---

## 🔄 ML Workflow

### 1. Data Ingestion

* Loads dataset
* Splits into training and test sets
* Saves to `artifacts/`

### 2. Data Transformation

* Preprocessing and scaling

### 3. Model Training

* Trains CNN model
* Saves model:

```
artifacts/mnist_cnn.keras
```

---

## 🧪 Running Locally

### 1. Setup Environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### 2. Run Training

```bash
python -m src.components.data_ingestion
```

---

### 3. Start Application

```bash
python app.py
```

---

### 4. Access

```
http://localhost:5000
```

---

## 🌐 API Endpoints

### Health Check

```
GET /health
```

### Login

```
POST /auth/login
```

### Predict

```
POST /predict
```

---

## 🔐 Environment Variables

Required:

```
SUPABASE_KEY
```

* Local: `.env`
* Production: AWS Secrets Manager

---

## 🐳 Docker

```dockerfile
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY artifacts/mnist_cnn.keras /app/artifacts/mnist_cnn.keras

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## ☁️ Deployment

* AWS ECS (Fargate)
* Application Load Balancer
* Health check path: `/health`
* Container port: `5000`

---

## 🔄 CI/CD

GitHub Actions pipeline:

* Builds Docker image
* Pushes to AWS ECR
* Triggers ECS service deployment

---

## ⚠️ Common Issues

| Issue               | Cause                          |
| ------------------- | ------------------------------ |
| Container exits     | Missing environment variables  |
| Health check fails  | curl not installed             |
| 504 Gateway Timeout | App not bound to `0.0.0.0`     |
| Secrets not loading | Network / IAM misconfiguration |
| SSL pending         | DNS not propagated             |

---

## 📈 Future Improvements

* Model versioning
* Batch inference
* Monitoring and logging
* UI enhancements


---