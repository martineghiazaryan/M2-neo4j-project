import openai
import gradio as gr
import json
import pandas as pd
from graphrag_interface import graphRAG_query

def query_neo4j(nl_query):
    """
    Takes a natural language query, generates a Cypher query using an LLM,
    executes it in Neo4j, and formats the response for Gradio.
    """
    try:
        response = graphRAG_query(nl_query, return_json=True)  

        if "error" in response:
            return json.dumps(response, indent=2), None  

        structured_results = response["results"]
        cypher_query = response["query"]

        print("DEBUG: Final Structured Results for Gradio:", structured_results)

        json_output = json.dumps(structured_results, indent=2)

        table_data = []
        for entry in structured_results:
            entity_data = list(entry.values())[0] 
            entity_type = list(entry.keys())[0]  

            row = {
                "Type": entity_type.capitalize(),
                "Name": entity_data.get("name", entity_data.get("group_name", "Unnamed")),
                "Members": entity_data.get("num_members", ""),
                "Category": entity_data.get("category_name", ""),
                "ID": entity_data.get("group_id", entity_data.get("member_id", entity_data.get("event_id", "")))
            }
            table_data.append(row)

        df = pd.DataFrame(table_data)

        return json_output, df

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2), None
