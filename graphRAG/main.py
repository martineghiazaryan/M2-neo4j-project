from graphrag_interface import graphRAG_query

def main():
    while True:
        nl_query = input("\nEnter your query (or type 'exit' to quit): ")
        if nl_query.lower() == "exit":
            break

        formatted_results = graphRAG_query(nl_query)

        print("\n📌 Query Results:\n")
        print(formatted_results)

if __name__ == "__main__":
    main()
