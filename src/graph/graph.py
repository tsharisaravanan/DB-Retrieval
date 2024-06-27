from langgraph.graph import END, StateGraph
from src.states.state import GraphResponseState
from src.graph.nodes import GraphNode


def create_graph(model, db):

    graph = StateGraph(GraphResponseState)
    node = GraphNode(model, db)

    graph.add_node("SQL Query Generation", node.query_generation)
    graph.add_node("Execute SQL Query", node.execute_query)
    graph.add_node("SQL Error Fixing", node.query_error_fixing)
    graph.add_node("Generate Natural Response", node.natural_response)
    graph.add_node("Visualization Type Check", node.visualization_type_check)
    graph.add_node("Program Generator", node.program_generator)
    graph.add_node("Execute Program", node.execute_program)
    graph.add_node("Program Error Fixing", node.program_error_fixing)

    graph.set_entry_point("SQL Query Generation")
    graph.add_edge("SQL Query Generation", "Execute SQL Query")
    graph.add_conditional_edges(
        "Execute SQL Query",
        node.should_continue,
        {
            "good_response": "Generate Natural Response",
            "error": "SQL Error Fixing"
        }
    )
    graph.add_edge("SQL Error Fixing", "Execute SQL Query")
    graph.add_edge("Generate Natural Response", "Visualization Type Check")
    graph.add_edge("Visualization Type Check", "Program Generator")
    graph.add_edge("Program Generator", "Execute Program")
    graph.add_conditional_edges(
        "Execute Program",
        node.should_continue,
        {
            "good_response": END,
            "error": "Program Error Fixing"
        }
    )
    graph.add_edge("Program Error Fixing", "Execute Program")

    workflow = graph.compile()

    return workflow
