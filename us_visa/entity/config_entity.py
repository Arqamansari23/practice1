# this file config_entity specify all paths where thing like raw data train data test data model are stored 


import os
from us_visa.constants import *
from dataclasses import dataclass
from datetime import datetime



TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:
    pipeline_name:str=PIPELINE_NAME
    artifact_dir:str=os.path.join(ARTIFACT_DIR,TIMESTAMP)
    timestamp:str=TIMESTAMP


training_pipeline_config:TrainingPipelineConfig=TrainingPipelineConfig()


# All paths of files important for data Ingestion 
@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)   
    # Full path: artifact/<TIMESTAMP>/data_ingestion
    
    feature_store_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    # Full path: artifact/<TIMESTAMP>/data_ingestion/feature_store/usvisa.csv
    
    training_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    # Full path: artifact/<TIMESTAMP>/data_ingestion/ingested/train.csv
    
    testing_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    # Full path: artifact/<TIMESTAMP>/data_ingestion/ingested/test.csv
    
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    # Train-test split ratio: 0.2
    
    collection_name: str = DATA_INGESTION_COLLECTION_NAME
    # Collection name: visa_data





# All paths of files important for data Validation
@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
    # Full path: artifact/<TIMESTAMP>/data_validation
    
    drift_report_file_path: str = os.path.join(data_validation_dir, DATA_VALIDATION_DRIFT_REPORT_DIR,
                                               DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
    # Full path: artifact/<TIMESTAMP>/data_validation/drift_report/report.yaml





@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)
    # Full path: artifact/<TIMESTAMP>/data_transformation
    
    transformed_train_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                    TRAIN_FILE_NAME.replace("csv", "npy"))
    # Full path: artifact/<TIMESTAMP>/data_transformation/transformed/train.npy
    
    transformed_test_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                   TEST_FILE_NAME.replace("csv", "npy"))
    # Full path: artifact/<TIMESTAMP>/data_transformation/transformed/test.npy
    
    transformed_object_file_path: str = os.path.join(data_transformation_dir,
                                                     DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                     PREPROCSSING_OBJECT_FILE_NAME)
    # Full path: artifact/<TIMESTAMP>/data_transformation/transformed_object/preprocessing.pkl







# All paths of files important for Model Training
@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME)
    # Full path: artifact/<TIMESTAMP>/model_trainer
    
    trained_model_file_path: str = os.path.join(model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR, MODEL_FILE_NAME)
    # Full path: artifact/<TIMESTAMP>/model_trainer/trained_model/model.pkl
    
    expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE
    # Expected accuracy: 0.6
    
    model_config_file_path: str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
    # Full path: config/model.yaml


@dataclass
class ModelEvaluationConfig:
    changed_threshold_score: float = MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE
    # Threshold score for model change evaluation
    
    bucket_name: str = MODEL_BUCKET_NAME
    # S3 Bucket name where the model is stored
    
    s3_model_key_path: str = MODEL_FILE_NAME
    # S3 model key path: model.pkl


@dataclass
class ModelPusherConfig:
    bucket_name: str = MODEL_BUCKET_NAME
    # S3 Bucket name for storing the model after training
    
    s3_model_key_path: str = MODEL_FILE_NAME
    # S3 model key path: model.pkl


@dataclass
class USvisaPredictorConfig:
    model_file_path: str = MODEL_FILE_NAME
    # Local model file path: model.pkl
    
    model_bucket_name: str = MODEL_BUCKET_NAME
    # S3 Bucket name for model storage
