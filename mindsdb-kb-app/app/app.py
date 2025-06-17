import os
import json
from dotenv import load_dotenv
import mindsdb_sdk
from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
import nest_asyncio

nest_asyncio.apply()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")
load_dotenv()

# Initialize MindsDB connection
try:
    con = mindsdb_sdk.connect("http://localhost:47334")
    project = con.get_project()
    print("Connected to MindsDB project:", project.name)
    kb = None
except Exception as e:
    print(f"Error connecting to MindsDB: {e}")
    con = None
    project = None


def create_knowledge_base():
    global kb
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
        kbs = project.knowledge_bases.list()
        print("Available Knowledge Bases:", [kb.name for kb in kbs])
        for kb_item in kbs:
            if kb_item.name == "company_kb":
                kb = kb_item
                print("Knowledge Base 'company_kb' found or created successfully")
                break
        if kb is None:
            print(
                "Knowledge Base 'company_kb' not found in list, might not be created yet"
            )
    except Exception as e:
        print(f"Knowledge Base error: {e}")


def setup_ai_tables():
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
        print("AI tables created")
    except Exception as e:
        print(f"Error setting up AI tables: {e}")


def insert_sample_data():
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
        # Check if Knowledge Base exists before inserting
        kbs = project.knowledge_bases.list()
        if any(kb_item.name == "company_kb" for kb_item in kbs):
            # Batch insert using raw SQL
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
            print("Sample FAQs & policies inserted successfully")
        else:
            print("Cannot insert data: Knowledge Base 'company_kb' not found")
    except Exception as e:
        print(f"Insert error: {e}")


def create_index():
    try:
        project.query(
            "CREATE INDEX IF NOT EXISTS content_index ON company_kb (content)"
        )
        print("Index created")
    except Exception as e:
        print(f"Error creating index: {e}")


def setup_update_job():
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
        print("Update job created")
    except Exception as e:
        print(f"Error setting up update job: {e}")


def semantic_search(query, department=None):
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
        print("Processed results:", processed_results)
        return processed_results
    except Exception as e:
        print("Semantic search error:", str(e))
        return []


def get_summarized_results(query):
    summaries = []
    if query:
        try:
            summary = project.query(
                f"""
            SELECT summary FROM document_summarizer
            WHERE content = '{query.replace("'", "''")}'
            """
            ).fetch()
            if summary is not None and not summary.empty:
                summaries.append(
                    {"original": query, "summary": summary.iloc[0]["summary"]}
                )
        except Exception as e:
            print(f"Error getting summary: {e}")
    return summaries


@app.route("/search", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form["query"]
        department = request.form.get("department")

        # Basic input validation
        if not query.strip():
            return render_template("search.html", error="Please enter a search query")

        results = semantic_search(query, department)
        return render_template(
            "results.html", results=results, query=query, department=department
        )

    return render_template("search.html")


@app.route("/")
def about():
    return render_template("about.html")


@app.route("/browse")
def browse():
    department = request.args.get("department", "")
    try:
        results = project.query(
            "SELECT content, department, doc_type FROM company_kb"
        ).fetch()
        processed = results.to_dict(orient="records")
        if department:
            processed = [r for r in processed if r["department"] == department]
        return render_template("browse.html", results=processed, department=department)
    except Exception as e:
        print(f"Error browsing documents: {e}")
        return render_template(
            "browse.html",
            results=[],
            department=department,
            error="Error loading documents",
        )


@app.route("/add", methods=["GET", "POST"])
def add_document():
    if request.method == "POST":
        content = request.form["content"]
        department = request.form["department"]
        doc_type = request.form["doc_type"]
        sql = f"""
        INSERT INTO company_kb (content, department, doc_type)
        VALUES ('{content.replace("'", "''")}', '{department}', '{doc_type}')
        """
        print("Executing SQL:", sql)
        try:
            project.query(sql)
            print("Insert query executed")
        except Exception as e:
            print("Insert error:", repr(e))
        return redirect(url_for("browse"))
    return render_template("add.html")


@app.route("/summarize", methods=["GET", "POST"])
def summarize():
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            summaries = get_summarized_results(query)
            return render_template("summarize.html", summaries=summaries, query=query)
    # GET: Show the form
    return render_template("summarize.html", summaries=None, query=None)


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            # Add user message
            session["chat_history"].append({"sender": "user", "text": user_input})

            # Use semantic search to find relevant docs
            results = semantic_search(user_input)
            if results:
                # Summarize top result as bot response
                top_content = results[0]["content"]
                summary = get_summarized_results(top_content)
                if summary:
                    bot_response = summary[0]["summary"]
                else:
                    bot_response = "Sorry, I couldn't find a summary."
            else:
                bot_response = "Sorry, I couldn't find any relevant information."

            # Add bot response
            session["chat_history"].append({"sender": "bot", "text": bot_response})

    return render_template("chat.html", chat_history=session.get("chat_history", []))


if __name__ == "__main__":
    if project:
        create_knowledge_base()
        setup_ai_tables()
        insert_sample_data()
        create_index()
        setup_update_job()
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        print("Cannot start application: No connection to MindsDB")
