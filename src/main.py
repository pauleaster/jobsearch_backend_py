from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.routes import job_controller, search_term_controller, test_controller, valid_job_search_terms_controller

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Job Search Backend API - Python version"
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
app.include_router(valid_job_search_terms_controller.router)  # ADD THIS LINE

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Jobsearch Backend API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)