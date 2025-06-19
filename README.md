# DuckDB SQL API

A simple SQL API backed by DuckDB.

## Repository Structure

```
├── app.py             # Flask API server
├── init.sql           # Optional SQL script run at startup
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

## init.sql

If an `init.sql` file is present at the project root, it will be executed once when the server starts.  
Use this to maintain any `ATTACH` statements for `.db`, `.duckdb`, or `.ducklake` files, as well as to run any other initialization DDL/DML.

Please note that these SQL statements will be executed in a read-only connection and therefore cannot create or modify data.

Example `init.sql`:

```sql
INSTALL ducklake;

ATTACH 'ducklake:ducklake.ducklake';
```

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
4. **Configure environment**  
   - Create a `.env` file:  
     ```bash
     echo "DUCKDB_API_KEY=your-secret-key" > .env
     echo "DB_FILE=test.db" >> .env
     ```
   - Or export directly:  
     ```bash
     export DUCKDB_API_KEY="your-secret-key"
     export DB_FILE="test.db"
     ```

### Running the Flask API

- **Development server**:
  ```bash
  python app.py
  ```
- **Production with Gunicorn**:
  ```bash
  gunicorn app:app --workers 4 --threads 2 --bind 0.0.0.0:8000
  ```

## API Reference

### Health Check

```
GET /health
```
Response:
```json
{"status":"ok"}
```

### Run a Query

```
POST /query
```

Headers:
```
X-API-Key: <your-secret-key>
Content-Type: application/json
```

Body:
```json
{ "sql": "SELECT * FROM schema.table LIMIT 10" }
```

Response:
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
   docker build -t duckdb-http-api .
   ```
2. **Create** a `.env` file:
   ```ini
   DUCKDB_API_KEY=your-secret-key
   DB_FILE=test.db
   ```
3. **Run** the container, mounting your DB files:
   ```bash
   docker run -d \
     -p 8000:8000 \
     --env-file .env \
     -v "$(pwd)/test.db:/app/test.db" \
     --name duckdb-http-api \
     duckdb-http-api
   ```
4. **Verify**  
   ```bash
   curl -H "X-API-Key: your-secret-key" http://localhost:8000/health
   ```

## Docker Compose (Optional)

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - '8000:8000'
    env_file:
      - .env
    volumes:
      - ./test.db:/app/test.db
      - ./analytics.db:/app/analytics.db
```

```bash
docker-compose up -d
```