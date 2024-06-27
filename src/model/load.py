from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
    pipeline,
    BitsAndBytesConfig,
)
from langchain_community.llms import Ollama
from langchain_huggingface.llms import HuggingFacePipeline
from src.entity.config_entity import HuggingFaceModelConfig, OllamaModelConfig


class LLM:
    @staticmethod
    def ollama_model(ollama_config: OllamaModelConfig) -> Ollama:
        return Ollama(
            model=ollama_config.model_name,
            temperature=ollama_config.temperature,
            top_p=ollama_config.top_p,
        )

    @staticmethod
    def huggingface_model(huggingface_config: HuggingFaceModelConfig):

        quantization_config = BitsAndBytesConfig(
            load_in_8bit=True,
        )
        tokenizer = AutoTokenizer.from_pretrained(
            huggingface_config.model_name,
            use_fast=True,
            cache_dir="hf_cache"
        )
        model = AutoModelForCausalLM.from_pretrained(
            huggingface_config.model_name,
            device_map="auto",
            quantization_config=quantization_config,
            trust_remote_code=True,
            cache_dir="hf_cache"
        )

        generation_config = GenerationConfig.from_pretrained(
            huggingface_config.model_name
        )
        generation_config.temperature = huggingface_config.temperature
        generation_config.top_p = huggingface_config.top_p
        generation_config.do_sample = huggingface_config.do_sample
        generation_config.add_inst = huggingface_config.add_inst
        generation_config.repetition_penalty = huggingface_config.repetition_penalty

        text_pipeline = pipeline(
            "text-generation",
            model=model,
            return_full_text=False,
            tokenizer=tokenizer,
            generation_config=generation_config,
        )

        return HuggingFacePipeline(pipeline=text_pipeline)
