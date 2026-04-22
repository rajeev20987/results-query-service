from typing import List, Dict, Any
from app.db.repository import ResultsRepository


class ResultsService:
    """Service layer for handling test result operations"""

    def __init__(self, repository: ResultsRepository):
        self.repository = repository

    def get_test_results(self, filters: Dict[str, Any]) -> List[Dict]:
        """Fetch test results using filters and apply business logic"""

        results = self.repository.fetch_results(filters)

        # Example business logic: normalize status
        for r in results:
            r["status"] = r["status"].lower()

        return results