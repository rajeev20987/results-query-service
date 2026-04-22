from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.db.models import TestResult


class ResultsRepository:
    """Handles database operations for test results"""

    def __init__(self, db: Session):
        self.db = db

    def fetch_results(self, filters: Dict[str, Any]) -> List[Dict]:
        """Fetch results from DB based on filters"""

        query = self.db.query(TestResult)

        if filters.get("status"):
            query = query.filter(TestResult.status == filters["status"])

        if filters.get("suite"):
            query = query.filter(TestResult.suite == filters["suite"])

        if filters.get("limit"):
            query = query.limit(filters["limit"])

        results = query.all()

        # Convert ORM objects → dict
        return [
            {
                "id": r.id,
                "name": r.name,
                "status": r.status,
                "suite": r.suite,
                "trace": r.trace,
            }
            for r in results
        ]