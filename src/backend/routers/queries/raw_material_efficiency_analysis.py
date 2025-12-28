from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from backend.queries.raw_material_efficiency_analysis import get_raw_material_efficiency_analysis
from backend.schemas.queries.raw_material_efficiency_analysis import RawMaterialEfficiencyAnalysis

router = APIRouter(
    prefix="/api/query",
    tags=["Queries"]
)

@router.get("/raw-material-efficiency", response_model=List[RawMaterialEfficiencyAnalysis])
def read_raw_material_efficiency_analysis(db: Session = Depends(get_db)):
    return get_raw_material_efficiency_analysis(db)