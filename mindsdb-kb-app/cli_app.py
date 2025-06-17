import os
import mindsdb_sdk
from dotenv import load_dotenv

load_dotenv()


def connect_to_mindsdb():
    try:
        con = mindsdb_sdk.connect("http://localhost:47334")
        project = con.get_project()
        print("Connected to MindsDB project:", project.name)
        return project
    except Exception as e:
        print(f"Error connecting to MindsDB: {e}")
        return None


def create_knowledge_base(project):
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if not openai_api_key:
        print(
            "Warning: OPENAI_API_KEY not set in environment. Using default or empty key."
        )
    try:
        project.query(
            f"""
        CREATE KNOWLEDGE_BASE IF NOT EXISTS company_kb
        USING
            embedding_model = {{
                "provider": "openai",
                "model_name": "text-embedding-3-small",
                "api_key": "{openai_api_key}"
            }},
            metadata_columns = ['department', 'doc_type'],
            content_columns = ['content']
        """
        )
        print("Knowledge Base 'company_kb' creation command executed.")
    except Exception as e:
        print(f"Error creating Knowledge Base: {e}")


def check_knowledge_base(project):
    try:
        kbs = project.knowledge_bases.list()
        print("Available Knowledge Bases:", [kb.name for kb in kbs])
        return any(kb.name == "company_kb" for kb in kbs)
    except Exception as e:
        print(f"Error listing Knowledge Bases: {e}")
        return False


def insert_sample_data(project):
    documents = [
        {
            "content": "Employees are entitled to 25 paid vacation days annually.",
            "department": "HR",
            "doc_type": "policy",
        },
        {
            "content": "Marketing department holds weekly syncs every Thursday at 10am.",
            "department": "Marketing",
            "doc_type": "meeting",
        },
        {
            "content": "Technical support operates around the clock for critical problems.",
            "department": "IT",
            "doc_type": "procedure",
        },
        {
            "content": "Sales performance metrics are assessed every month.",
            "department": "Sales",
            "doc_type": "strategy",
        },
        {
            "content": "The finance team oversees all financial planning and expenditure authorization.",
            "department": "Finance",
            "doc_type": "report",
        },
        {
            "content": "All agreements must undergo legal examination prior to execution.",
            "department": "Legal",
            "doc_type": "procedure",
        },
    ]

    try:
        values = ",".join(
            [
                f"('{doc['content']}', '{doc['department']}', '{doc['doc_type']}')"
                for doc in documents
            ]
        )
        project.query(
            f"""
        INSERT INTO company_kb (content, department, doc_type)
        VALUES {values}
        """
        )
        print("Sample data inserted successfully.")
    except Exception as e:
        print(f"Error inserting sample data: {e}")


def create_index(project):
    try:
        project.query(
            "CREATE INDEX IF NOT EXISTS content_index ON company_kb (content)"
        )
        print("Index created on Knowledge Base.")
    except Exception as e:
        print(f"Error creating index: {e}")


def setup_update_job(project):
    try:
        project.query(
            """
        CREATE JOB IF NOT EXISTS update_company_kb AS (
            INSERT INTO company_kb (content, department, doc_type)
            SELECT content, department, doc_type
            FROM files.new_documents
            WHERE id > COALESCE(LAST, 0)
        )
        EVERY day
        """
        )
        print("Update job created for periodic data ingestion.")
    except Exception as e:
        print(f"Error setting up update job: {e}")


def setup_ai_tables(project):
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if not openai_api_key:
        print("Warning: OPENAI_API_KEY not set for AI tables setup.")
    try:
        project.query(
            f"""
        CREATE ML_ENGINE IF NOT EXISTS openai_engine FROM openai
        USING api_key = '{openai_api_key}';
        """
        )
        project.query(
            f"""
        CREATE MODEL IF NOT EXISTS document_summarizer
        PREDICT summary
        USING
            engine = 'openai_engine',
            model_name = 'gpt-3.5-turbo',
            prompt_template = 'Summarize this company document: {{content}}';
        """
        )
        print("AI tables for summarization created.")
    except Exception as e:
        print(f"Error setting up AI tables: {e}")


def semantic_search(project, query, department=None):
    query = query.replace("'", "''")
    base_query = f"""
    SELECT content, department, doc_type
    FROM company_kb
    WHERE content LIKE '%{query}%'
    """
    if department:
        base_query += f" AND department = '{department}'"
    print("Executing semantic search query:", base_query)
    try:
        results = project.query(base_query).fetch()
        processed_results = []
        for _, row in results.iterrows():
            processed_results.append(
                {
                    "content": row["content"],
                    "department": row["department"],
                    "doc_type": row["doc_type"],
                }
            )
        print("Search Results:")
        for result in processed_results:
            print(
                f"- {result['content']} (Dept: {result['department']}, Type: {result['doc_type']})"
            )
        return processed_results
    except Exception as e:
        print(f"Semantic search error: {e}")
        return []


def main():
    project = connect_to_mindsdb()
    if not project:
        return

    while True:
        print("\nCompany Knowledge Base CLI")
        print("1. Setup Knowledge Base and Data")
        print("2. Perform Semantic Search")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            create_knowledge_base(project)
            if check_knowledge_base(project):
                insert_sample_data(project)
                create_index(project)
                setup_update_job(project)
                setup_ai_tables(project)
            else:
                print(
                    "Setup incomplete: Knowledge Base 'company_kb' not found. Please check MindsDB configuration."
                )
        elif choice == "2":
            query = input("Enter search query: ")
            dept = input(
                "Enter department filter (optional, press Enter to skip): "
            ).strip()
            department = dept if dept else None
            semantic_search(project, query, department)
        elif choice == "3":
            print("Exiting CLI.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
