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

   To serve both HTTP and HTTPS simultaneously, open two terminal windows and run:

**HTTP (port 3001):**
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 3001 --reload
```

**HTTPS (port 3002, with self-signed certificate):**
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 3002 --reload --ssl-certfile cert.pem --ssl-keyfile key.pem
```

- The API will be available at:
  - **HTTP:** http://localhost:3001
  - **HTTPS:** https://localhost:3002
- Swagger UI: `/docs`
- ReDoc: `/redoc`

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

### HTTPS Setup (Self-Signed Certificates)

To run the API with HTTPS locally, you need a certificate and key file.

#### Option 1: Using OpenSSL

1. **Install OpenSSL**  
   - [Download OpenSSL for Windows](https://slproweb.com/products/Win32OpenSSL.html)  
   - On Linux/Mac, OpenSSL is usually pre-installed.

2. **Generate certificate and key:**
   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
   ```
   - When prompted, you can enter values or leave them blank.
   - This creates `cert.pem` (certificate) and `key.pem` (private key) in your current directory.

#### Option 2: Using PowerShell (Windows only)

1. **Generate a self-signed certificate:**
   ```powershell
   New-SelfSignedCertificate -DnsName "localhost" -CertStoreLocation "cert:\LocalMachine\My"
   ```
   - Export the certificate and key using the Windows Certificate Manager or PowerShell.

2. **Export certificate and key:**
   - Open `certmgr.msc`, find your certificate under "Personal > Certificates".
   - Right-click, select "Export", and follow the wizard to export as `.pfx`.
   - Convert `.pfx` to `.pem` using OpenSSL:
     ```bash
     openssl pkcs12 -in yourcert.pfx -out cert.pem -nodes
     ```

#### Configure your application

- Place `cert.pem` and `key.pem` in your project root or a secure folder.
- Add these lines to your `.env.local`:
  ```env
  USE_HTTPS=True
  SSL_CERTFILE=cert.pem
  SSL_KEYFILE=key.pem
  ```

#### Run the application

To serve both HTTP and HTTPS simultaneously, open two terminal windows and run:

**HTTP (port 3001):**
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 3001 --reload
```

**HTTPS (port 3002, with self-signed certificate):**
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 3002 --reload --ssl-certfile cert.pem --ssl-keyfile key.pem
```

- The API will be available at:
  - **HTTP:** http://localhost:3001
  - **HTTPS:** https://localhost:3002

> **Note:** Browsers will warn about self-signed certificates. This is expected for local development.


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
curl "http://localhost:3001/api/jobs/?page=1&page_size=10"

# Get second page
curl "http://localhost:3001/api/jobs/?page=2&page_size=10"

# Search for Python jobs
curl "http://localhost:3001/api/jobs/?search=python&page_size=20"
```

### Get Total Count

```bash
curl "http://localhost:3001/api/jobs/count"
# Response: {"count": 8404}

curl "http://localhost:3001/api/jobs/count?search=python"
# Response: {"count": 45}  (example)
```

### Get Specific Job

```bash
curl "http://localhost:3001/api/jobs/8379"
```

### Create a Job

```bash
curl -X POST "http://localhost:3001/api/jobs/" \
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

### Running Integration Tests

From the `Jobsearch_backend_py` directory, activate your virtual environment and run:

```powershell
# Windows PowerShell
$env:PYTHONPATH="."; pytest tests/integration/routes
```

```bash
# Linux/Mac (bash)
PYTHONPATH=. pytest tests/integration/routes
```

> **Note:**  
> Always run tests from the `Jobsearch_backend_py` directory (the project root for the Python backend) so that relative imports work correctly.

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