import uvicorn
import matplotlib
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from src.model.load import LLM
from src.graph.graph import create_graph
from src.config.manager import ConfigurationManager
from src.database.database import PostgresSQLServer

import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*Matplotlib.*")
matplotlib.use('Agg')


class InputSchema(BaseModel):
    question: str


class ResponseModel(BaseModel):
    status: int
    question: str
    query: str
    query_response: str
    response: str
    error_message: str
    num_steps: int
    visualization_type: str
    program: str


app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="SQL Knowledge base retrieval API Server"
)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SQLKnowledgebaseRetrieval(metaclass=SingletonMeta):
    def __init__(self):
        self.config = ConfigurationManager()
        self.flow = self.config.flow
        self.db_config = self.config.get_database_config()
        self.ollama_config = self.config.get_ollama_model_config()
        self.huggingface_config = self.config.get_huggingface_model_config()
        self.model = self.initialize_model()

    def initialize_model(self):
        if self.flow == "Ollama":
            print("Loading Ollama Model :)")
            return LLM.ollama_model(self.ollama_config)
        elif self.flow == "HuggingFace":
            print("Loading Huggingface Model :)")
            return LLM.huggingface_model(self.huggingface_config)


def get_db():
    if not hasattr(get_db, "db_obj"):
        get_db.db_obj = PostgresSQLServer()
        get_db.db = get_db.db_obj.database_connection()
        print("Connected to Database :)")
    return get_db.db


def get_model():
    retrieval = SQLKnowledgebaseRetrieval()
    return retrieval.model


def get_workflow_app(db=Depends(get_db), model=Depends(get_model)):
    if not hasattr(get_workflow_app, "workflow_app"):
        get_workflow_app.workflow_app = create_graph(model, db)
        print("Graph Created :)")
    return get_workflow_app.workflow_app


@app.post('/predict', response_model=ResponseModel)
def knowledge_base_retrieval(data: InputSchema, workflow_app=Depends(get_workflow_app)):
    try:
        result = workflow_app.invoke(
            {
                "question": data.question,
                "num_steps": 0
            },
            {"recursion_limit": 10}
        )
        return ResponseModel(
            status=200,
            question=str(result.get('question', '')),
            query=str(result.get('query', '')),
            query_response=str(result.get('query_response', '')),
            response=str(result.get('response', '')),
            error_message=str(result.get('error_message', '')),
            num_steps=int(result.get('num_steps', 0)),
            visualization_type=str(result.get('visualization_type', '')),
            program=str(result.get('program', '')),
        )
    except Exception as e:
        return ResponseModel(
            status=500,
            question="",
            query="",
            query_response="",
            response="",
            error_message=str(e),
            num_steps=0,
            visualization_type="",
            program="",
        )


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
