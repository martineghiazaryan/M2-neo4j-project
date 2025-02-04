import gradio as gr
import openai
import pandas as pd
from database import run_cypher_query
from llm import generate_cypher_query, generate_results_summary

css = """
    body { background-color: #1e1e1e; color: white; }
    .gradio-container { font-family: Arial, sans-serif; }
"""

handshake_logo = "img/handshake.jpg"

def graphRAG_query(nl_query):
    cypher_query = generate_cypher_query(nl_query, context=None)
    if not cypher_query:
        return {"error": "Failed to generate a valid Cypher query."}, None, None

    results = run_cypher_query(cypher_query)
    if not results:
        return {"message": "No results found."}, None, cypher_query

    structured_results, df = process_query_results(results)

    return structured_results, df, cypher_query

def flatten_result(record):
    flattened = {}
    for key, value in record.items():
        if isinstance(value, dict):  
            for sub_key, sub_value in value.items():
                flattened[f"{key}.{sub_key}"] = sub_value 
        else:
            flattened[key] = value 
    return flattened



def format_query_results(nl_query):
    structured_results, df, cypher_query = graphRAG_query(nl_query)

    if structured_results is None:
        return {"error": "No valid results found."}, None, cypher_query, "No summary available."

    summary = generate_results_summary(structured_results)

    return structured_results, df, cypher_query, summary


def build_interface():
    with gr.Blocks(css=css, theme=gr.themes.Base()) as demo:
        with gr.Row():
            gr.Image(handshake_logo, label="Integration", show_label=False, width=200, height=100)
        
        gr.Markdown("# 🤖 GraphRAG-powered Neo4j Query System")
        gr.Markdown("Enter a question about the meetup network, and get structured data from Neo4j!")
        
        query_input = gr.Textbox(label="Enter your natural language query")
        submit_btn = gr.Button("Submit", variant="primary")
        
        with gr.Row():
            json_output = gr.JSON(label="Structured JSON Output")
        with gr.Row():
            query_output = gr.Textbox(label="Generated Cypher Query", interactive=False)
        with gr.Row():
            table_output = gr.DataFrame(label="Query Results", interactive=False)
        with gr.Row():
            summary_output = gr.Textbox(label="Summary", interactive=False)

        submit_btn.click(format_query_results, inputs=[query_input], outputs=[json_output, table_output, query_output, summary_output])

    return demo


def process_query_results(results):
    structured_results = [flatten_result(record) for record in results]

    if not structured_results:
        return "No results found.", None  
    df = pd.DataFrame(structured_results)

    return structured_results, df

app = build_interface()
app.launch()