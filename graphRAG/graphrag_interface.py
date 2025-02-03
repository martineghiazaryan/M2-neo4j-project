import openai
from config import OPENAI_API_KEY, OPENAI_MODEL
from database import run_cypher_query

def graphRAG_query(nl_query):
    """
    Converts a natural language query to Cypher, executes it, and formats the output using GPT-4o-mini.
    """
    from llm import generate_cypher_query

    # 🔹 Step 1: Convert NL query to Cypher
    cypher_query = generate_cypher_query(nl_query, context=None)
    if not cypher_query:
        return "❌ Failed to generate a valid Cypher query."

    print(f"DEBUG: Generated Cypher query:\n{cypher_query}\n")

    # 🔹 Step 2: Execute Cypher query in Neo4j
    results = run_cypher_query(cypher_query)

    if not results:
        return "🔍 No results found for this query."

    # 🔹 Step 3: Send results to GPT-4o-mini for formatting
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = f"""
    You are an AI assistant that formats Neo4j query results into **readable text**.
    The user executed the following query:
    ```
    {cypher_query}
    ```

    The results are structured as a list of JSON objects. Each object may contain:
    - `Group`: `group_id`, `group_name`, `num_members`, `category_name`
    - `Member`: `member_id`, `name`
    - `Event`: `event_id`, `name`
    - `Friendship`: Member `FRIEND_OF` another member
    - `Participation`: Member `PARTICIPATES_IN` a group
    - `RSVP`: Member `ATTENDED` an event

    Format the output as **clear, readable text**. Use:
    - 📌 **Bold Titles**
    - ✅ **Bullet Points**
    - 🔗 **Clickable Links (if available)**
    - 🔄 **Emoji-based labels**
    
    **Query Results:** 
    ```json
    {results}
    ```
    """

    try:
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a formatting assistant that formats database results into clear, structured text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0  # Ensure deterministic formatting
        )
        
        formatted_output = response.choices[0].message.content.strip()
        return formatted_output
    
    except Exception as e:
        print(f"ERROR: Failed to format results with GPT-4o-mini: {e}")
        return "⚠️ Error formatting the results."

