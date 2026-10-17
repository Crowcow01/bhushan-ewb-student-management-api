# EWB Student Management API

A REST API for managing student records using Python, FastAPI, SQLAlchemy, and SQLite, with an optional local AI assistant powered by Ollama.

## Features

- Create, list, search, retrieve, update, and delete student records
- SQLite database for persistent storage
- Input validation using Pydantic
- Unique email address enforcement
- Appropriate HTTP status codes and error responses
- Interactive API documentation with Swagger UI
- Optional AI assistant for asking natural-language questions about student records
- Automated tests using pytest

## Technology Stack

- Python 3.12 or compatible Python version
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- pytest
- Ollama with `llama3.2:3b` (optional AI feature)

## Requirements

- Python and pip
- Git (for cloning or contributing to the repository)
- Ollama only if you want to use the AI assistant

## Setup

### 1. Clone the repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ewb-student-management-api
```

Alternatively, open the project folder directly in VS Code if you already have the source code.

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If Python 3.12 is not installed, use an installed compatible Python version.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the API

```powershell
uvicorn main:app --reload
```

The API will be available at:

- API base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/students/` | Create a student |
| GET | `/students/` | List students |
| GET | `/students/{student_id}` | Retrieve a student |
| PUT | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |
| POST | `/ai/ask` | Ask the optional AI assistant |
| GET | `/health` | Check API health |

Use Swagger UI at `/docs` to inspect endpoint parameters, submit requests, and view responses.

## Example: Create a Student

Send a `POST` request to `/students/` with a JSON body such as:

```json
{
  "name": "Rahul Sharma",
  "email": "rahul.sharma@example.com",
  "age": 21,
  "course": "Civil Engineering"
}
```

The API validates the submitted data and returns the created student record.

## Optional AI Assistant

The AI assistant uses a local Ollama model to answer natural-language questions using context retrieved from the student database.

### 1. Install Ollama

Install Ollama from its official website:

https://ollama.com/

### 2. Download the configured model

Open a separate terminal and run:

```powershell
ollama pull llama3.2:3b
```

Ensure Ollama is running before using the AI endpoint.

### 3. Ask a question

Send a `POST` request to `/ai/ask`:

```json
{
  "question": "How many students are currently in the database?"
}
```

Example questions:

- How many students are currently in the database?
- Tell me the details of all students in the database.
- Are there any students named Rahul Sharma?

The AI assistant is optional. The student CRUD endpoints do not require Ollama.

## Running Tests

With the virtual environment activated, run:

```powershell
python -m pytest -v
```

The tests cover student operations and input validation. Review the test output to confirm the results in your environment.

## Database

The application uses SQLite with SQLAlchemy for database operations. Student records are stored locally, allowing them to persist between API requests.

The database file is generated locally by the application. Do not commit local database files containing student records to the public repository.

## Project Structure

```text
ewb-student-management-api/
├── app/
│   ├── routes/
│   │   ├── students.py
│   │   └── ai_query.py
│   ├── services/
│   │   ├── student_service.py
│   │   └── ai_service.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   ├── conftest.py
│   └── test_students.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Notes

- Keep the virtual environment and local database files out of version control.
- The AI assistant requires Ollama and the configured model to be installed locally.
- API documentation is available through Swagger UI while the application is running.
