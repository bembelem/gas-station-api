from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from backend.queries.batch_raw_materials_analysis import get_batch_raw_materials_analysis
from backend.schemas.queries.batch_raw_materials_analysis import BatchRawMaterialsAnalysis

router = APIRouter(
    prefix="/api/query",
    tags=["Queries"]
)

@router.get("/batch-raw-materials-analysis", response_model=List[BatchRawMaterialsAnalysis])
def read_batch_raw_materials_analysis(db: Session = Depends(get_db)):
    return get_batch_raw_materials_analysis(db)
