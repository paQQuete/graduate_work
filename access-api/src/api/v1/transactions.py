import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.schemas.transaction import TransactionCreate, Transaction
from db.database import get_db
from services import transactions_cr

router = APIRouter()


@router.post('/', response_model=Transaction)
async def create_trans(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        return await transactions_cr.create_transaction(db=db, transaction=transaction)
    finally:
        db.commit()


@router.get('/{user_uuid}/pagination', response_model=list[Transaction])
async def read_trans_by_user_pagination(user_uuid: uuid.UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = await transactions_cr.read_by_user(db=db, user_uuid=user_uuid, skip=skip, limit=limit)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="No transactions found for this user")


@router.get('/{user_uuid}', response_model=list[Transaction])
async def read_trans_by_user_all(user_uuid: uuid.UUID, db: Session = Depends(get_db)):
    result = await transactions_cr.read_all_by_user(db=db, user_uuid=user_uuid)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="No transactions found for this user")



