from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfig:
    """Database related configurations"""
    db_type: str
    domain: str
    user_name: str
    password: str
    db_name: str
    no_sample_records: int


@dataclass(frozen=True)
class HuggingFaceModelConfig:
    """Huggingface model configurations"""
    model_name: str
    temperature: float
    top_p: float
    do_sample: bool
    add_inst: bool
    repetition_penalty: float


@dataclass(frozen=True)
class OllamaModelConfig:
    """Ollama model configurations"""
    model_name: str
    temperature: float
    top_p: float
