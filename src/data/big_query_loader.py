from google.cloud import bigquery
import pandas as pd
from src.config import Config
from pathlib import Path


class BigQueryLoader:

    @staticmethod
    def load_data(
        query=None, query_file=None, parquet_file=None, query_parameters_map={}
    ):

        if Path(f"{Config.TEMP_DATA_PATH}/{parquet_file}").exists():
            print("DATA EXIST, IS LOADING FROM LOCAL ...")
            return pd.read_parquet(f"{Config.TEMP_DATA_PATH}/{parquet_file}")
        print("LOADING FROM SOURCE .... ")

        client = bigquery.Client(project=Config.PROJECT_ID)

        if query_file:
            with open(f"{Config.QUERY_FORLDER}/{query_file}", "r") as qfile:
                query = qfile.read()
        job_config = bigquery.QueryJobConfig(
            query_parameters=BigQueryLoader.get_query_parameter(query_parameters_map)
        )
        job = client.query_and_wait(query, job_config=job_config)
        data = job.to_dataframe()

        if parquet_file:
            data.to_parquet(f"{Config.TEMP_DATA_PATH}/{parquet_file}")
        return data

    @staticmethod
    def get_query_parameter(query_parameters_map):
        query_parameters = []
        for param_name in query_parameters_map:
            param_type, param_value = query_parameters_map[param_name]
            query_parameters.append(
                bigquery.ScalarQueryParameter(param_name, param_type, param_value)
            )
        return query_parameters
