from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.routes import (
    combined_job_search_controller,
    job_controller,
    search_term_controller,
    test_controller,
    valid_job_search_terms_controller,
)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Job Search Backend API - Python version",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(job_controller.router)
app.include_router(search_term_controller.router)
app.include_router(test_controller.router)
app.include_router(valid_job_search_terms_controller.router)
app.include_router(combined_job_search_controller.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Jobsearch Backend API",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    print(
        "Please run the application using:\n"
        "  python -m uvicorn src.main:app --host 0.0.0.0 --port 3001 --reload\n"
        "for HTTP, or:\n"
        "  python -m uvicorn src.main:app --host 0.0.0.0 --port 3002 --reload --ssl-certfile cert.pem --ssl-keyfile key.pem\n"
        "for HTTPS.\n"
        "See the README for details."
    )
