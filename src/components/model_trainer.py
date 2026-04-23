import os
import sys
from dataclasses import dataclass

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

from src.exception import CustomException
from src.logger import logging


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "mnist_cnn.keras")


class ModelTrainer:
    def __init__(self):
        self.config = ModelTrainerConfig()

    def initiate_model_trainer(self, X_train, X_test, y_train, y_test):
        try:
            logging.info("Building CNN model")

            model = Sequential([
                Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
                MaxPooling2D((2,2)),

                Conv2D(64, (3,3), activation='relu'),
                MaxPooling2D((2,2)),

                Flatten(),
                Dense(128, activation='relu'),
                Dropout(0.3),
                Dense(10, activation='softmax')
            ])

            logging.info("Compiling model")

            model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )

            logging.info("Training model")

            model.fit(
                X_train,
                y_train,
                epochs=10,
                batch_size=64,
                validation_split=0.1
            )

            logging.info("Evaluating model")

            loss, acc = model.evaluate(X_test, y_test)
            logging.info(f"Test Accuracy: {acc}")

            os.makedirs(os.path.dirname(self.config.trained_model_file_path), exist_ok=True)

            logging.info("Saving model")

            model.save("artifacts/mnist_cnn.h5")

            return acc

        except Exception as e:
            raise CustomException(e, sys)
