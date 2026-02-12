# Jobsearch_backend_py\src\config\settings.py

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Jobsearch Backend"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Database settings - MS SQL Server
    DB_DRIVER: str = "ODBC Driver 17 for SQL Server"
    DB_SERVER: str = "PAULEWINDOWS"
    DB_NAME: str = "jobsearch_test"
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_TRUSTED_CONNECTION: bool = True
    
    @property
    def DATABASE_URL(self) -> str:
        if self.DB_TRUSTED_CONNECTION:
            return (
                f"mssql+pyodbc://{self.DB_SERVER}/{self.DB_NAME}"
                f"?driver={self.DB_DRIVER}"
                f"&Trusted_Connection=yes"
                f"&Encrypt=yes"
                f"&TrustServerCertificate=yes"
            )
        else:
            return (
                f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}/{self.DB_NAME}"
                f"?driver={self.DB_DRIVER}"
                f"&Encrypt=yes"
                f"&TrustServerCertificate=yes"
            )
    
    class Config:
        env_file = ".env.local"  # Changed from ".env"
        case_sensitive = True

settings = Settings()