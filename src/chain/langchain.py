from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser


class LangChain:

    @staticmethod
    def sql_query_generate(model, user_question, tables_schema):
        _template = load_prompt("prompt/query_generate.yaml")
        query_generator_chain = _template | model | StrOutputParser()
        return query_generator_chain.invoke(
            {
                "tables_schema": tables_schema,
                "user_question": user_question,
            }
        )

    @staticmethod
    def sql_query_regenerate(model, user_question, query, tables_schema, error_message):
        _template = load_prompt("prompt/query_regenerate.yaml")
        query_regenerator_chain = _template | model | StrOutputParser()
        return query_regenerator_chain.invoke(
            {
                "query": query,
                "tables_schema": tables_schema,
                "user_question": user_question,
                "error_message": error_message
            }
        )

    @staticmethod
    def naturel_response_generate(model, user_question, query, tables_schema, sql_response):
        _template = load_prompt("prompt/naturel_response_generate.yaml")
        nlp_response_generator_chain = _template | model | StrOutputParser()
        return nlp_response_generator_chain.invoke(
            {
                "query": query,
                "tables_schema": tables_schema,
                "user_question": user_question,
                "sql_response": sql_response
            }
        )

    @staticmethod
    def finding_chart_type(model, user_question, sql_response):
        _template = load_prompt("prompt/chart_type.yaml")
        visualization_chart_identifying_chain = _template | model | StrOutputParser()
        return visualization_chart_identifying_chain.invoke(
            {
                "question": user_question,
                "query_response": sql_response,
            }
        )

    @staticmethod
    def program_generation(model, user_question, natural_response, chart_type, sql_response):
        _template = load_prompt("prompt/program_generate.yaml")
        visualization_program_generate_chain = _template | model | StrOutputParser()
        return visualization_program_generate_chain.invoke(
            {
                "question": user_question,
                "response": natural_response,
                "chart_type": chart_type,
            }
        )

    @staticmethod
    def program_regeneration(model, program, error_message):
        _template = load_prompt("prompt/program_regenerate.yaml")
        program_regenerator_chain = _template | model | StrOutputParser()
        return program_regenerator_chain.invoke(
            {
                "program": program,
                "error_message": error_message
            }
        )
