# DuckDB SQL API

A simple SQL API backed by DuckDB.

## Repository Structure

```
├── app.py             # Flask API server
├── requirements.txt   # Python dependencies
├── Dockerfile         # Build instructions for API container
├── .gitignore
└── README.md          # This file
```

## Prerequisites

- Python 3.8+  
- pip  
- Docker (for containerized deployment)  
- (Optional) Docker Compose  

## Environment Variables

This application uses the following environment variables. You can set them in your shell or in a `.env` file at the project root (loaded automatically by `python-dotenv`):

- `DUCKDB_API_KEY` – Secret API key for authenticating requests (required).  
- `DB_FILE` – Filename of the primary `.db` file to open (defaults to `test.db`).

Shell variables take precedence over values in `.env`.

## Database Files

Place all your DuckDB `.db` files in the project root (next to `app.py`).

- The primary DB file is defined by `DB_FILE` (default `test.db`).  
- All other `*.db` files are automatically attached under the alias given by their filename (minus `.db`).

## Local Development

1. **Clone & enter** the repo  
   ```bash
   git clone <repo-url>
   cd <repo-dir>
   ```
2. **Create & activate** a virtual environment  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Configure your API key**  
   - **Option A**: Create a `.env` file:  
     ```bash
     echo "DUCKDB_API_KEY=your-secret-key" > .env
     echo "DB_FILE=test.db" >> .env
     ```
   - **Option B**: Export directly in your shell:  
     ```bash
     export DUCKDB_API_KEY="your-secret-key"
     export DB_FILE="test.db"
     ```

### Running the Flask API

- **Development server** (auto-reload; not for production):
  ```bash
  python app.py
  ```
  Listens on `0.0.0.0:8000`.

- **Production server** with Gunicorn:
  ```bash
  gunicorn app:app     --workers 4     --threads 2     --bind 0.0.0.0:8000
  ```

## API Reference

### Health Check

```
GET /health
```

**Response**  
```json
{"status":"ok"}
```

### Run a Query

```
POST /query
```

**Headers**  
```
X-API-Key: <your-secret-key>
Content-Type: application/json
```

**Body**  
```json
{ "sql": "SELECT * FROM catalog.schema.table LIMIT 10" }
```

**Response**  
```json
{
  "rowcount": 2,
  "columns": ["col1","col2"],
  "results": [
    { "col1": 1, "col2": "foo" },
    { "col1": 2, "col2": "bar" }
  ]
}
```

## Docker Usage

1. **Build** the image  
   ```bash
   docker build -t duckdb-api .
   ```
2. **Create** a `.env` file at the project root (if you haven’t already):  
   ```ini
   DUCKDB_API_KEY=your-super-secret-key
   DB_FILE=test.db
   ```
3. **Run** the container, **mounting** your `.db` files as volumes:  
   ```bash
   docker run -d      -p 8000:8000      --env-file .env      -v "$(pwd)/test.db:/app/test.db"      -v "$(pwd)/test3.db:/app/test3.db"      -v "$(pwd)/test4.db:/app/test4.db"      -v "$(pwd)/tpch.db:/app/tpch.db"      --name duckdb-api      duckdb-api
   ```
4. **Verify**  
   ```bash
   curl -H "X-API-Key: your-super-secret-key" http://localhost:8000/health
   ```

## Docker Compose (Optional)

```yaml
version: "3.8"
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
```

```bash
docker-compose up -d
```