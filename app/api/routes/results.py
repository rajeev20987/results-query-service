from fastapi import APIRouter, Depends, Query
from typing import Optional, List

from app.services.results_service import ResultsService
from app.schemas.results_schema import ResultResponse
from app.db.repository import ResultsRepository
from app.db.connection import get_db

router = APIRouter(prefix="/results", tags=["Results"])


@router.get("/results", response_model=List[ResultResponse])
def fetch_results(db=Depends(get_db)):
    filters = {}  # add query params if needed
    repo = ResultsRepository(db)
    service = ResultsService(repo)
    return service.get_test_results(filters)