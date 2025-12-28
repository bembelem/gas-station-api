from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from backend.queries.transport_stats import get_transport_stats
from backend.schemas.queries.transport_stats import TransportStats

router = APIRouter(
    prefix="/api/query",
    tags=["Queries"]
)

@router.get("/transport-stats", response_model=list[TransportStats])
def read_transport_stats(db: Session = Depends(get_db)):
    return get_transport_stats(db)
