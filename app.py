import os
from pathlib import Path
import duckdb
from flask import Flask, request, jsonify, g, abort

# Load .env if present
from dotenv import load_dotenv
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

API_KEY = os.environ.get("DUCKDB_API_KEY")
if not API_KEY:
    raise RuntimeError("DUCKDB_API_KEY must be set in your environment or in a .env file")

# Allow overriding the primary file via env var
DB_FILE = os.environ.get("DB_FILE", "test.db")

def get_db():
    if "db" not in g:
        # Open primary DB in read‐only mode
        g.db = duckdb.connect(database=DB_FILE, read_only=True)

        # Run init.sql if present
        init_path = Path("init.sql")
        if init_path.exists():
            g.db.execute(init_path.read_text())

    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db:
        db.close()

def require_api_key():
    token = request.headers.get("X-API-Key", "")
    if token != API_KEY:
        abort(401, "Invalid API key")

@app.route("/query", methods=["POST"])
def query():
    require_api_key()
    data = request.get_json() or {}
    sql = data.get("sql", "").strip()
    con = get_db()
    try:
        result = con.execute(sql)
        rows = result.fetchall()
        cols = [col[0] for col in result.description]
    except Exception as e:
        abort(400, f"Query error: {e}")

    results = [dict(zip(cols, row)) for row in rows]
    return jsonify(rowcount=len(results), columns=cols, results=results)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
