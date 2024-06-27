from src.constants import RUNTIME_CONFIG_FILE_PATH
from src.utils.helper_functions import read_yaml_file
from src.entity.config_entity import DatabaseConfig, HuggingFaceModelConfig, OllamaModelConfig


class ConfigurationManager:
    def __init__(self, params_file_path=RUNTIME_CONFIG_FILE_PATH) -> None:
        self.config = read_yaml_file(params_file_path)
        self.flow = self.config.flow.model

    def get_database_config(self) -> DatabaseConfig:
        return DatabaseConfig(
            db_type=self.config.SQLDatabase.db_type,
            domain=self.config.SQLDatabase.domain,
            user_name=self.config.SQLDatabase.user_name,
            password=self.config.SQLDatabase.password,
            db_name=self.config.SQLDatabase.db_name,
            no_sample_records=self.config.SQLDatabase.no_sample_records,
        )

    def get_huggingface_model_config(self) -> HuggingFaceModelConfig:
        return HuggingFaceModelConfig(
            model_name=self.config.LLM.HuggingFace.model_name,
            temperature=self.config.LLM.HuggingFace.temperature,
            top_p=self.config.LLM.HuggingFace.top_p,
            do_sample=self.config.LLM.HuggingFace.do_sample,
            add_inst=self.config.LLM.HuggingFace.add_inst,
            repetition_penalty=self.config.LLM.HuggingFace.repetition_penalty,
        )

    def get_ollama_model_config(self) -> OllamaModelConfig:
        return OllamaModelConfig(
            model_name=self.config.LLM.Ollama.model_name,
            temperature=self.config.LLM.Ollama.temperature,
            top_p=self.config.LLM.Ollama.top_p,
        )
