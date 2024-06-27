from src.chain.langchain import LangChain
from src.states.state import GraphResponseState
from src.utils.helper_functions import printer

class GraphNode:

    def __init__(self, model, db):
        self.db = db
        self.model = model

    def query_generation(self, state: GraphResponseState):
        num_steps = int(state['num_steps']) + 1
        query = LangChain.sql_query_generate(
            model=self.model,
            user_question=state['question'],
            tables_schema=self.db.table_info
        )
        printer(
            function="Query Generate",
            step_count=num_steps,
            value=query
        )
        return {"query": query, "num_steps": num_steps}

    def execute_query(self, state: GraphResponseState):
        num_steps = int(state['num_steps']) + 1
        try:
            response = self.db.run(
                command=state['query'],
                include_columns=True
            )
            printer(
                function="Query Execution",
                step_count=num_steps,
                value=response
            )
            return {"query_response": response, "num_steps": num_steps}
        except Exception as e:
            printer(
                function="Query Execution",
                step_count=num_steps,
                value=str(e)
            )
            return {"error_message": e, "num_steps": num_steps}

    def query_error_fixing(self, state: GraphResponseState):
        num_steps = int(state['num_steps']) + 1
        new_query = LangChain.sql_query_regenerate(
            model=self.model,
            query=state['query'],
            user_question=state['question'],
            tables_schema=self.db.table_info,
            error_message=state['error_message']
        )
        printer(
            function="Query Error Fixing",
            step_count=num_steps,
            value=new_query
        )
        return {"query": new_query, "num_steps": num_steps, "error_message": None}

    @staticmethod
    def should_continue(state: GraphResponseState):
        num_steps = int(state['num_steps']) + 1
        val = state.get("error_message")
        if val is None:
            printer(
                function="Decision Making",
                step_count=num_steps,
                value="Routing to response creation"
            )
            return "good_response"
        else:
            printer(
                function="Decision Making",
                step_count=num_steps,
                value="Routing to re-generation activity"
            )
            return "error"

    def natural_response(self, state: GraphResponseState):
        num_steps = int(state['num_steps']) + 1
        nlp_response = LangChain.naturel_response_generate(
            model=self.model,
            query=state['query'],
            user_question=state['question'],
            tables_schema=self.db.table_info,
            sql_response=state['query_response'],
        )
        printer(
            function="Natural Response",
            step_count=num_steps,
            value=nlp_response
        )
        return {"response": nlp_response, "num_steps": num_steps}

    def visualization_type_check(self, state: GraphResponseState):
        num_steps = int(state['num_steps']) + 1
        visualization_type = LangChain.finding_chart_type(
            model=self.model,
            user_question=state['question'],
            sql_response=state['query_response']
        )
        printer(
            function="Chart Type",
            step_count=num_steps,
            value=visualization_type
        )
        return {"visualization_type": visualization_type, "num_steps": num_steps}

    def program_generator(self, state: GraphResponseState):
        num_steps = int(state['num_steps']) + 1
        program = LangChain.program_generation(
            model=self.model,
            user_question=state['question'],
            natural_response=state['response'],
            chart_type=state['visualization_type'],
            sql_response=state['query_response']
        )
        printer(
            function="Program Generate",
            step_count=num_steps,
            value=program
        )
        return {"program": program, "num_steps": num_steps}

    @staticmethod
    def execute_program(state: GraphResponseState):
        num_steps = int(state['num_steps']) + 1
        try:
            program = state["program"].strip()
            exec(program)
            printer(
                function="Program Execution",
                step_count=num_steps,
                value="Above generated program execution completed"
            )
            return {"program": program, "num_steps": num_steps}
        except Exception as e:
            printer(
                function="Program Regenerate",
                step_count=num_steps,
                value=str(e)
            )
            return {"error_message": e, "num_steps": num_steps}

    def program_error_fixing(self, state: GraphResponseState):
        num_steps = int(state['num_steps']) + 1
        new_program = LangChain.program_regeneration(
            model=self.model,
            program=state["program"],
            error_message=state['error_message']
        )
        printer(
            function="Program Error Fixing",
            step_count=num_steps,
            value=new_program
        )
        return {"program": new_program, "num_steps": num_steps, "error_message": None}
