from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

def get_neo4j_driver():
    """Initializes and returns a Neo4j driver instance."""
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def run_cypher_query(query, parameters=None):
    """Executes a Cypher query and returns the results."""
    driver = get_neo4j_driver()
    results = []
    
    with driver.session() as session:
        try:
            query_result = session.run(query, parameters or {})
            for record in query_result:
                results.append(record.data())  # Extracting dictionary format
        except Exception as e:
            print(f"❌ ERROR: Failed to execute Cypher query: {e}")
    
    driver.close()
    return results

def test_connection():
    """Tests the connection to Neo4j and prints total node count."""
    driver = get_neo4j_driver()
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) AS total_nodes")
        for record in result:
            print("✅ Total nodes:", record["total_nodes"])
    driver.close()
