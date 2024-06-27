from typing_extensions import TypedDict


class GraphResponseState(TypedDict):
    question: str
    query: str
    query_response: str
    response: str
    error_message: str
    num_steps: int
    visualization_type: str
    program: str
