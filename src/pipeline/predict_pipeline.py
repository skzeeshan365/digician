import os
import sys
import numpy as np
from PIL import Image
import keras
from src.exception import CustomException


class PredictPipeline:
    def __init__(self):
        self.model_path = os.path.join("artifacts", "mnist_cnn.keras")

    def preprocess_image(self, image_path):
        img = Image.open(image_path).convert('L')
        img = img.resize((28, 28))

        img = np.array(img)
        img = img / 255.0
        img = img.reshape(1, 28, 28, 1)

        return img

    def predict(self, image_path):
        try:
            model = keras.models.load_model(self.model_path, compile=False)

            img = self.preprocess_image(image_path)

            # try both normal + inverted
            pred1 = model.predict(img, verbose=0)
            conf1 = np.max(pred1)

            img_inv = 1.0 - img
            pred2 = model.predict(img_inv, verbose=0)
            conf2 = np.max(pred2)

            if conf2 > conf1:
                return int(np.argmax(pred2)), float(conf2), True
            else:
                return int(np.argmax(pred1)), float(conf1), False

        except Exception as e:
            raise CustomException(e, sys)