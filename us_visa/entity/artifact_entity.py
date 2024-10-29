# this file defines the output types of all Pipelines 
from dataclasses import dataclass


# The Data Ingestion Pipeline returns the path of train and test data  
@dataclass
class DataIngestionReturnType:
    trained_file_path:str
    test_file_path:str





@dataclass
class DataValidationReturnType:
    validation_status:bool
    message: str
    drift_report_file_path: str





@dataclass
class DataTransformationArtifact:
    transformed_object_file_path:str 
    transformed_train_file_path:str
    transformed_test_file_path:str


@dataclass
class ClassificationMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float



@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str 
    metric_artifact:ClassificationMetricArtifact



@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    changed_accuracy:float
    s3_model_path:str 
    trained_model_path:str



@dataclass
class ModelPusherArtifact:
    bucket_name:str
    s3_model_path:str