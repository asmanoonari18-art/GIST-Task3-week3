# DataFlow — Python Data Processing & Analytics API

**Advanced+ Python-Based Real-World Application**

DataFlow is a production-style backend service that accepts CSV datasets, profiles their structure and quality, stores dataset metadata in a database, cleans common data-quality issues, and exposes everything through a documented REST API.

## Project requirements covered

| Requirement | Implementation |
|---|---|
| Complete Python application | FastAPI backend |
| Data-processing system | Pandas profiling + cleaning pipeline |
| Automation | One-request CSV cleaning workflow |
| Database integration | SQLAlchemy + SQLite |
| API integration | REST API with FastAPI |
| Testing | Pytest unit + API tests |
| Documentation | README + automatic OpenAPI/Swagger docs |
| Deployment | Docker + Docker Compose |
| CI | GitHub Actions test workflow |
| Professional structure | app/services/models/schemas/database + tests |

## Features

- CSV file validation
- Dataset profiling
- Row/column statistics
- Data-type detection
- Missing-value analysis
- Duplicate-row detection
- Numeric statistical summary
- Automatic duplicate removal
- Missing-value imputation
- Dataset metadata persistence
- REST API
- Swagger/OpenAPI documentation
- Automated tests
- Docker deployment
- CI pipeline

## Architecture

```text
Client
  |
  v
FastAPI REST API
  |
  +--> Data Processing Service --> Pandas
  |
  +--> Database Layer ----------> SQLite
  |
  +--> OpenAPI / Swagger
  |
  +--> Tests / CI
```

## 1. Run locally

Create a virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health: `http://127.0.0.1:8000/health`

## 2. Run tests

```bash
pytest -q
```

## 3. API endpoints

### Health
`GET /health`

### Profile CSV
`POST /datasets/profile`

Upload a CSV file. The service calculates:

- number of rows
- number of columns
- column names
- data types
- missing values per column
- duplicate rows
- numeric statistics

The dataset metadata and profile are saved in SQLite.

### List processed datasets
`GET /datasets`

### Get one dataset
`GET /datasets/{dataset_id}`

### Clean CSV
`POST /datasets/clean`

The cleaning pipeline:

1. reads the CSV
2. removes duplicate rows
3. fills numeric missing values with the column median
4. fills text missing values with the column mode
5. returns a cleaned CSV file

## 4. Docker deployment

Build and run:

```bash
docker compose up --build
```

Then visit:

`http://localhost:8000/docs`

Stop:

```bash
docker compose down
```

The SQLite database is persisted in the local `data/` directory.

## 5. Example workflow

Upload:

```text
data/sample_students.csv
```

to:

```text
POST /datasets/profile
```

Then call:

```text
GET /datasets
```

to see the stored dataset record.

Finally, upload the same file to:

```text
POST /datasets/clean
```

to receive a cleaned CSV.

## 6. Example response

```json
{
  "dataset_id": 1,
  "filename": "students.csv",
  "profile": {
    "shape": {
      "rows": 5,
      "columns": 4
    },
    "columns": ["Name", "Math", "Physics", "English"],
    "duplicate_rows": 1
  }
}
```

## 7. Professional development practices

- Separation of API, business logic, database, models, and schemas
- Input validation
- HTTP error handling
- Automated tests
- Dependency pinning
- Dockerized deployment
- Persistent database volume
- CI on push and pull request
- OpenAPI documentation

## 8. Future production upgrades

For a larger production deployment, replace SQLite with PostgreSQL, add authentication/JWT, object storage for large files, background jobs with Celery/RQ, structured logging, rate limiting, monitoring, and a frontend dashboard.

## License

MIT
