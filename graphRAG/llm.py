import re
import json
import openai
from config import OPENAI_API_KEY, OPENAI_MODEL

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_cypher_query(nl_query, context):
    prompt = f"""
    You are an AI specialized in Neo4j Cypher queries. Generate a valid Cypher query based on the user's request always limiting 10 results while strictly adhering to the Neo4j schema:

    ---
    ### **Database Schema Overview**
    
    #### **Node Labels and Properties**
    - **(m:Member)** → {{ {{ "member_id": STRING, "name": STRING }} }}
    - **(g:Group)** → {{ {{ "group_id": STRING, "category_name": STRING, "category_id": STRING, "group_name": STRING, "organizer_id": STRING, "num_members": INTEGER, "group_urlname": STRING }} }}
    - **(e:Event)** → {{ {{ "event_id": STRING, "name": STRING, "time": STRING }} }}

    #### **Valid Relationship Types**
    - **(m:Member)-[:PARTICIPATES_IN]->(g:Group)**  → Members join groups.
    - **(m:Member)-[:FRIEND_OF]->(m:Member)**  → Members have friendships.
    - **(g:Group)-[:CONNECTED_TO]->(g:Group)**  → Groups are connected.
    - **(m:Member)-[:ATTENDED]->(e:Event)**  → Members attend events.
    - **(g:Group)-[:SIMILAR]->(g:Group)**  → Groups with similar topics.

    ---
    ### **Query Generation Rules**
    1. **Only use labels and properties from the schema above.** Avoid non-existent properties like `location`, `city`, or `members`.
    2. **Ensure relationships exist in the schema** (e.g., do not assume a direct `ATTENDED` relationship between `Group` and `Event`).
    3. **Use precise property names**:
       - `num_members` (not `members`)
       - `group_name` (not `name` for groups)
       - `category_name` (for filtering by category)
       - `event_id`, `time` (for events)
    4. **Only return the Cypher query** – do not include explanations or Markdown formatting.

    ---
    **Context:** {context}

    **User Query:**  
    "{nl_query}"

    **Generated Cypher Query:**
    """

    try:
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert in writing Neo4j Cypher queries. Only output the valid Cypher query with no explanation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0 
        )
        
        cypher_query = response.choices[0].message.content.strip()

        # Strip Markdown formatting (` ```cypher ... ``` `)
        cypher_query = re.sub(r"```(?:cypher)?\n(.*?)\n```", r"\1", cypher_query, flags=re.DOTALL).strip()

        # Ensure the output looks like a valid Cypher query
        if not cypher_query.startswith("MATCH") and not cypher_query.startswith("CREATE"):
            raise ValueError(f"Generated response does not look like a valid Cypher query: {cypher_query}")

        return cypher_query
    except Exception as e:
        print(f"ERROR: Failed to generate Cypher query: {e}")
        return None


def generate_results_summary(results):
    try:
        results_str = json.dumps(results, indent=2)
        prompt = f"Provide a short, concise summary and/or assumptions within the nashville meetup topic (not including summary or assumptions about the repetetive names or ids, its interesting to explain why that result is interesting) for the following Neo4j query results:\n\n{results_str}\n\nSummary:"
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert data summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"ERROR generating summary: {e}")
        return "No summary available."
