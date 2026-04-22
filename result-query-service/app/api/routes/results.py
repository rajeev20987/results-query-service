from fastapi import APIRouter, Depends, Query
from typing import Optional, List

from app.services.results_service import ResultsService
from app.schemas.results_schema import ResultResponse
from app.db.repository import ResultsRepository
from app.db.connection import get_db

router = APIRouter(prefix="/results", tags=["Results"])


@router.get("/", response_model=List[ResultResponse])
def fetch_results(
    status: Optional[str] = Query(None),
    suite: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    db=Depends(get_db)
):
    # ✅ Build filters from query params
    filters = {
        "status": status,
        "suite": suite,
        "name": name
    }

    # remove None values
    filters = {k: v for k, v in filters.items() if v is not None}

    repo = ResultsRepository(db)
    service = ResultsService(repo)

    # ✅ Call service with filters
    return service.get_test_results(filters)