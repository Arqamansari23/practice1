import json
import sys

import pandas as pd

from evidently.model_profile import Profile

from evidently.model_profile.sections import DataDriftProfileSection

from pandas import DataFrame

from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.entity.artifact_entity import DataIngestionReturnType, DataValidationReturnType
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH






# This class takes Artifacts (output of ) Data Ingestion for path of train and test file 

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionReturnType, data_validation_config: DataValidationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_validation_config: configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact      # Loading artifacts of Data ingestion 
            self.data_validation_config = data_validation_config          # Loading All the files necessary for data validation 



            # reading Schema.yaml file in to which we can validate our data 
            self._schema_config =read_yaml_file(file_path=SCHEMA_FILE_PATH)  # read_yaml_file Function defined in main.utils 
        except Exception as e:
            raise USvisaException(e,sys)
        







    # validating the total number of columns 
    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        """
        Method Name :   validate_number_of_columns
        Description :   This method validates the number of columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])    # lengh of data frame k columns and lenght of columns defined in schema .yaml must be equal  values is in true or false 
            logging.info(f"Is required column present: [{status}]")    # logging status 
            return status    # returning status 
        except Exception as e:
            raise USvisaException(e, sys)
        








   # This method Accepts Dataframe and  validates the existence of a numerical and categorical columns

    def Checking_Catagorical_And_Numerical_Columns(self, df: DataFrame) -> bool:
        """
        Method Name :   Checking_Catagorical_And_Numerical_Columns
        Description :   This method validates the existence of a numerical and categorical columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            dataframe_columns = df.columns   # loading all the columns in a data frame 
            missing_numerical_columns = []      # list of all missing numerical columns  
            missing_categorical_columns = []     # list of all missing catagorical columns 


            # All the Numerical columns in  Schema.yaml file 
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column) # jo sschema me he or data me nai he numeric feature us ko list me dal do 

            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical column: {missing_numerical_columns}")  # agar  missing_numerical_columns = [] ki lenght 0 se zada ho matlab kuch he list ke andar jo missing he 




            # same Check for Catagorical columns 
            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_categorical_columns)>0:
                logging.info(f"Missing categorical column: {missing_categorical_columns}")





             # false return karega ye function agar dono list ki lenght 0 se zada hogi    

            return False if len(missing_categorical_columns)>0 or len(missing_numerical_columns)>0 else True
        except Exception as e:
            raise USvisaException(e, sys) from e
        












    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e, sys)
        





    # Detecting Data Drift 

    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame, ) -> bool:
        """
        Method Name :   detect_dataset_drift
        Description :   This method validates if drift is detected
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])

            data_drift_profile.calculate(reference_df, current_df)

            report = data_drift_profile.json()    # generating report in json format 
            json_report = json.loads(report)   # loading the content of json data 


             #Writing the content into report .yaml file  
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)



            # Extracting Total Numbers Of features From the report.yaml file 
            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]

            # Extracting Drifter features from the report.yaaml file 
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]



            #  Calculating ratio of drifted features and logging it 
            logging.info(f"{n_drifted_features}/{n_features} drift detected.")


            # it will give Drift detected in True or False 
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            return drift_status
        except Exception as e:
            raise USvisaException(e, sys) from e
        










        # Now we initializing data validation 

    def initiate_data_validation(self) -> DataValidationReturnType:
        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """

        try:

            # Error message appended here
            validation_error_msg = ""




            logging.info("Starting data validation")




            # First we need to read The Train and Test data from the ingestion  folder inside artifact folder  
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))
            



            # Checking  number of column in Train data 
            status = self.validate_number_of_columns(dataframe=train_df)
            logging.info(f"All required columns present in training dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."




            #  Checking  number of column in Test data 
            status = self.validate_number_of_columns(dataframe=test_df)

            logging.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."





            # Check if all catagorical and numerical features are present in Train data 
            status = self.Checking_Catagorical_And_Numerical_Columns(df=train_df)

            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."




            # Check if all catagorical and numerical features are present in Test data  
            status = self.Checking_Catagorical_And_Numerical_Columns(df=test_df)

            if not status:
                validation_error_msg += f"columns are missing in test dataframe."







            # Checking validation status if error message lenght is == 0 meas no message and return TRUE outher wise status will be false      

            validation_status = len(validation_error_msg) == 0



            # If validation status is true Then we proceeed with data drift detection 
            if validation_status:
                # detect drift will return true or false 
                drift_status = self.detect_dataset_drift(train_df, test_df)

                # if Drift status is true Then Drift is detected else if drift status is false then drift not detected 
                if drift_status:
                    logging.info(f"Drift detected.")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "Drift not detected"
            else:
                logging.info(f"Validation_error: {validation_error_msg}")




                
            # combining all things to that function return This variable os of return type 
            data_validation_artifact = DataValidationReturnType(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e