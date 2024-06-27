from src.utils.helper_functions import read_yaml_file
from langchain_community.utilities.sql_database import SQLDatabase


class PostgresSQLServer:
    def __init__(self):
        db_config = read_yaml_file("params/runtime.yml")
        self.db_config_data = db_config.SQLDatabase

    def database_connection(self) -> SQLDatabase:
        return SQLDatabase.from_uri(
            sample_rows_in_table_info=self.db_config_data.no_sample_records,
            database_uri=f"postgresql+psycopg2://{self.db_config_data.user_name}:{self.db_config_data.password}@{self.db_config_data.domain}/{self.db_config_data.db_name}"
        )
