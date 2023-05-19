import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import schemas
from db.database import get_db
from services import transactions_cr

router = APIRouter()


@router.post('/transactions/', response_model=schemas.Transaction)
def create_trans(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return transactions_cr.create_transaction(db=db, transaction=transaction)



