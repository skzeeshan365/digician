import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from tensorflow.keras.utils import to_categorical

from src.exception import CustomException
from src.logger import logging


@dataclass
class DataTransformationConfig:
    # No preprocessor.pkl needed anymore
    pass


class DataTransformation:
    def __init__(self):
        self.config = DataTransformationConfig()

    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info("Reading train and test data")

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Splitting features and labels")

            # First column = label
            X_train = train_df.iloc[:, 1:].values
            y_train = train_df.iloc[:, 0].values

            X_test = test_df.iloc[:, 1:].values
            y_test = test_df.iloc[:, 0].values

            logging.info("Applying normalization")

            X_train = X_train / 255.0
            X_test = X_test / 255.0

            logging.info("Reshaping into 28x28 images")

            X_train = X_train.reshape(-1, 28, 28, 1)
            X_test = X_test.reshape(-1, 28, 28, 1)

            logging.info("One-hot encoding labels")

            y_train = to_categorical(y_train, 10)
            y_test = to_categorical(y_test, 10)

            logging.info("Data transformation completed")

            return (
                X_train,
                X_test,
                y_train,
                y_test
            )

        except Exception as e:
            raise CustomException(e, sys)