import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from models.schemas.balance import Balance
from db.database import get_db
from services import balance_r

router = APIRouter()


@router.get('/{user_uuid}', response_model=Balance)
async def read_user_balance(user_uuid: uuid.UUID, db: Session = Depends(get_db)):
    try:
        return await balance_r.read_user_balance(db=db, user_uuid=user_uuid)
    except NoResultFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="No balance found for this user or the balance has not yet been calculated")
