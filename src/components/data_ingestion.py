# Data ingestion file
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer
@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"mninst_train.csv")
    test_data_path: str=os.path.join('artifacts',"mninst_test.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered data ingestion")

        try:
            train_df = pd.read_csv('notebook/data/mnist_train.csv')
            test_df = pd.read_csv('notebook/data/mnist_test.csv')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            train_df.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_df.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data ingestion completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    X_train, X_test, y_train, y_test = data_transformation.initiate_data_transformation(train_data, test_data)

    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(X_train, X_test, y_train, y_test))