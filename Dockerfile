FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# copy model correctly
COPY artifacts/mnist_cnn.keras /app/artifacts/mnist_cnn.keras

EXPOSE 5000

CMD ["python", "app.py"]