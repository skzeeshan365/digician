FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# copy model correctly
COPY artifacts/mnist_cnn.keras /app/artifacts/mnist_cnn.keras

EXPOSE 5000

CMD ["python", "app.py"]