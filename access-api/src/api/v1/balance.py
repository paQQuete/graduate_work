import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from models.schemas.balance import Balance
from models.models import HTTPErrorDetails
from db.database import get_db
from services import balance_r

router = APIRouter()


@router.get('/{user_uuid}', response_model=Balance)
async def read_user_balance(user_uuid: uuid.UUID, db: Session = Depends(get_db)):
    """Read last saved value for user balance"""
    try:
        return await balance_r.read_user_balance(db=db, user_uuid=user_uuid)
    except NoResultFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=HTTPErrorDetails.NOT_FOUND.value)
