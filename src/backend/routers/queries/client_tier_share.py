from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from backend.queries.client_tier_share import get_client_tier_share_report
from backend.schemas.queries.client_tier_share import ClientTierShareReport

router = APIRouter(
    prefix="/api/query",
    tags=["Queries"]
)

@router.get("/client-tier-share", response_model=list[ClientTierShareReport])
def read_client_tier_share(db: Session = Depends(get_db)):
    return get_client_tier_share_report(db)
