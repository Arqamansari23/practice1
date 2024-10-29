import os
from datetime import date





# Defining All the Constants 

DATABASE_NAME = "US_VISA"     # Data base name in mongo db 

COLLECTION_NAME = "visa_data"     #    Collection name is data base 

MONGODB_URL_KEY = "MONGODB_URL"       # Mongo db URL 

PIPELINE_NAME: str = "usvisa"        # Pipeline name 
ARTIFACT_DIR: str = "artifact"        # Artifact folder to save all outputs 


TRAIN_FILE_NAME: str = "train.csv"     # training file name 
TEST_FILE_NAME: str = "test.csv"     # Testing file name 

FILE_NAME: str = "usvisa.csv"     # Raw file before spliting 
MODEL_FILE_NAME = "model.pkl"       # Model name after training we can store with that name 


TARGET_COLUMN = "case_status"     # Name of target variable 
CURRENT_YEAR = date.today().year     # Fetching Current Year of date 
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"     #  data preprocessor pipe line will be stored in this 
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")    


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "visa_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"   # Feature store folder inside artifacts folder   to hold raw data before train test split 
DATA_INGESTION_INGESTED_DIR: str = "ingested"      # ingested folder inside artifact folder responsible to hold train and test data 
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2    # Train test ratio 


"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"   # for creating data_validation folder 
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"  # for Creating folder that keeps reports  inside 
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"   #drift reports




"""
Data Transformation ralated constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"   # Transformed data sorage directory
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"    # directory name that holds preprocessor.pkl file 


"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")




"""
MODEL EVALUATION related constant 
"""
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_BUCKET_NAME = "usvisa-model200"
MODEL_PUSHER_S3_KEY = "model-registry"


APP_HOST = "0.0.0.0"
APP_PORT = 8080



# Aws Credentials for accessing s3 Bucket 
AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
REGION_NAME = "us-east-1"