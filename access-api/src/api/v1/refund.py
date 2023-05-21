import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from services import balance_check

router = APIRouter()


@router.post('/request')
def refund_availability(user_uuid: uuid.UUID, amount: int, db: Session = Depends(get_db)):
    if balance_check.aggregate(db=db, user_uuid=user_uuid) >= amount:
        return {'message': 'Refund available'}
    else:
        raise HTTPException(status_code=406, detail="Refund is not available")
