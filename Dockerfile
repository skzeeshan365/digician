FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# copy model correctly
COPY artifacts/mnist_cnn.h5 /app/artifacts/mnist_cnn.h5

EXPOSE 5000

CMD ["python", "app.py"]