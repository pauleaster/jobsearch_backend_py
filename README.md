# Jobsearch Backend - Python FastAPI

A FastAPI-based REST API for managing job search data, built with Python and SQLAlchemy, connected to MS SQL Server.

## Project Overview

This is a Python implementation of a job search management system that mirrors the functionality of the .NET backend. It provides endpoints for managing jobs, search terms, and their relationships.

## Features

- ✅ RESTful API with FastAPI
- ✅ MS SQL Server integration with SQLAlchemy
- ✅ Pagination and search functionality
- ✅ CRUD operations for Jobs and Search Terms
- ✅ Interactive API documentation (Swagger UI)
- ✅ Type-safe DTOs with Pydantic
- ✅ Abstract service layer pattern

## Project Structure

```
Jobsearch_backend_py
├── src
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   ├── config                       # Configuration and database setup
│   │   ├── __init__.py
│   │   ├── settings.py             # Environment settings
│   │   └── database.py             # SQLAlchemy database configuration
│   ├── controllers                  # API route handlers
│   │   ├── __init__.py
│   │   ├── job_controller.py       # Job endpoints
│   │   ├── search_term_controller.py  # Search term endpoints
│   │   └── test_controller.py      # Health check endpoints
│   ├── services                     # Business logic layer
│   │   ├── __init__.py
│   │   ├── job_service.py          # Job business logic
│   │   ├── search_term_service.py  # Search term business logic
│   │   └── job_search_term_service.py  # Junction table logic
│   ├── models
│   │   ├── __init__.py
│   │   ├── entities                # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── job.py
│   │   │   ├── search_term.py
│   │   │   └── job_search_term.py
│   │   └── dtos                    # Pydantic DTOs for API
│   │       ├── __init__.py
│   │       ├── job_dto.py
│   │       └── search_term_dto.py
│   ├── exceptions                  # Custom exceptions
│   │   ├── __init__.py
│   │   └── not_found_exception.py
│   ├── data                        # Database context (legacy)
│   │   ├── __init__.py
│   │   └── jobsearch_db_context.py
│   └── views                       # Response models
│       ├── __init__.py
│       └── response_models.py
├── tests                           # Unit tests
│   └── __init__.py
├── .gitignore                      # Git ignore file
├── requirements.txt                # Python dependencies
├── LICENSE                         # MIT License
└── README.md                       # This file

# Not committed to git:
├── .env.local                      # Environment variables (local config)
├── .venv/                          # Virtual environment
└── **/__pycache__/                 # Python cache files
```

## Database Schema

The application connects to a MS SQL Server database with the following tables:

- **jobs** - Main job listings (8,404 records)
- **search_terms** - Search keywords (22 records)
- **job_search_terms** - Many-to-many relationship (22,712 records)
- **job_id_mapping** - Legacy ID mappings
- **search_term_id_mapping** - Legacy ID mappings

## Setup Instructions

### Prerequisites

- Python 3.8+
- MS SQL Server (SQL Server Express or higher)
- ODBC Driver 17 for SQL Server

### Installation

1. **Clone the repository:**
   ```bash
   cd Jobsearch_backend_combined/Jobsearch_backend_py
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   
   Create a `.env.local` file in the root directory:
   ```env
   # Application
   ENVIRONMENT=development
   DEBUG=True

   # Database - MS SQL Server
   DB_SERVER=your_server_name
   DB_NAME=jobsearch_test
   DB_TRUSTED_CONNECTION=True
   
   # For SQL Authentication (if not using Windows Auth):
   # DB_TRUSTED_CONNECTION=False
   # DB_USER=your_username
   # DB_PASSWORD=your_password
   ```

   **Important:** The `.env.local` file is ignored by git and should never be committed. It may contain sensitive credentials if using SQL Authentication.

5. **Run the application:**
   ```bash
   python -m uvicorn src.main:app --reload
   ```

   The API will be available at:
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Authentication & Security

### Database Authentication

The application supports two authentication methods:

1. **Windows Authentication (Trusted Connection)** - Recommended for development
   - Uses your Windows credentials
   - Set `DB_TRUSTED_CONNECTION=True` in `.env.local`
   - No username/password needed
   - **Safe to commit:** Connection strings without credentials

2. **SQL Server Authentication** - For production/deployment
   - Requires username and password
   - Set `DB_TRUSTED_CONNECTION=False` in `.env.local`
   - Add `DB_USER` and `DB_PASSWORD` to `.env.local`
   - **DO NOT commit** credentials to git

### API Authentication

⚠️ **Currently, the API has no authentication.** All endpoints are publicly accessible. For production deployment, consider adding:

- JWT token authentication
- API keys
- OAuth2 integration
- Rate limiting

### Security Checklist

Before committing code, ensure:

- [ ] `.env.local` is in `.gitignore`
- [ ] No hardcoded passwords or connection strings in code
- [ ] No database credentials in committed files
- [ ] `__pycache__` directories are ignored
- [ ] `.venv` directory is ignored
- [ ] Test scripts with sensitive data are not committed

The current codebase uses environment variables and `.env.local` for all sensitive configuration, making it safe for public repositories.

## API Endpoints

### Jobs

- `GET /api/jobs/` - Get all jobs (paginated)
  - Query params: `page` (default: 1), `page_size` (default: 100, max: 1000), `search` (optional)
- `GET /api/jobs/count` - Get total count of jobs
- `GET /api/jobs/{job_id}` - Get a specific job by ID
- `POST /api/jobs/` - Create a new job
- `PUT /api/jobs/{job_id}` - Update a job
- `PATCH /api/jobs/{job_id}` - Partially update a job field
- `DELETE /api/jobs/{job_id}` - Delete a job

### Search Terms

- `GET /api/searchterms/` - Get all search terms
- `GET /api/searchterms/{term_id}` - Get a specific search term
- `POST /api/searchterms/` - Create a new search term
- `DELETE /api/searchterms/{term_id}` - Delete a search term

### Health & Testing

- `GET /api/test/health` - API health check
- `GET /api/test/db-connection` - Database connection test

## Usage Examples

### Get Jobs with Pagination

```bash
# Get first 10 jobs
curl "http://localhost:8000/api/jobs/?page=1&page_size=10"

# Get second page
curl "http://localhost:8000/api/jobs/?page=2&page_size=10"

# Search for Python jobs
curl "http://localhost:8000/api/jobs/?search=python&page_size=20"
```

### Get Total Count

```bash
curl "http://localhost:8000/api/jobs/count"
# Response: {"count": 8404}

curl "http://localhost:8000/api/jobs/count?search=python"
# Response: {"count": 45}  (example)
```

### Get Specific Job

```bash
curl "http://localhost:8000/api/jobs/8379"
```

### Create a Job

```bash
curl -X POST "http://localhost:8000/api/jobs/" \
  -H "Content-Type: application/json" \
  -d '{
    "Url": "https://www.seek.com.au/job/12345",
    "Title": "Python Developer",
    "SearchTerms": ["Python", "FastAPI"]
  }'
```

## Technology Stack

- **Framework**: FastAPI 0.109.0
- **ORM**: SQLAlchemy 2.0.25
- **Database**: MS SQL Server (via pyodbc)
- **Validation**: Pydantic 2.5.3
- **Server**: Uvicorn
- **Documentation**: OpenAPI/Swagger

## Development

### Running Tests

```bash
# Run unit tests (when implemented)
pytest tests/
```

### Database Information

- **Database**: jobsearch_test
- **Authentication**: Windows Authentication (Trusted Connection) for development
- **Total Jobs**: 8,404
- **Total Search Terms**: 22
- **Date Range**: February 2024 (jobs are from 2 years ago)

## Architecture

This application follows a layered architecture:

1. **Controllers** - Handle HTTP requests and responses
2. **Services** - Contain business logic and data validation
3. **Entities** - SQLAlchemy ORM models (database tables)
4. **DTOs** - Pydantic models for API data transfer
5. **Config** - Settings and database configuration
6. **Exceptions** - Custom exception classes

## Configuration Files

### .gitignore

Ensure your `.gitignore` includes:
```
.env.local
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
```

### requirements.txt

All Python dependencies are listed in `requirements.txt`. Install with:
```bash
pip install -r requirements.txt
```

## Contributing

1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Write docstrings for public methods
4. Add tests for new features
5. Update this README for significant changes
6. **Never commit sensitive credentials or `.env.local` files**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.

## Contact

For questions or issues, please contact the development team.