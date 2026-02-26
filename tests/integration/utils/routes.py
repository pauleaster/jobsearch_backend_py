import os
print("Current working directory:", os.getcwd())
print("Directory contents:", os.listdir(os.getcwd()))


from fastapi.testclient import TestClient
from src.main import app # pylint: disable=import-error

client = TestClient(app)

# # Import all test modules to ensure pytest discovers and runs them
# from tests.integration.routes import test_job_controller