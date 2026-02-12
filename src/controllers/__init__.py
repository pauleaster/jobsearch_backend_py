# Jobsearch_backend_py\src\controllers\__init__.py

from .job_controller import router as job_router
from .search_term_controller import router as search_term_router
from .test_controller import router as test_router

__all__ = ["job_router", "search_term_router", "test_router"]

class UserController:
    def create_user(self, user_dto):
        pass

    def get_user(self, user_id):
        pass