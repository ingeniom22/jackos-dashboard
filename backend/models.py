from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class TransactionBase(SQLModel):
    timestamp: datetime
    customer_id: int
    price: int


class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int


class TransactionUpdate(SQLModel):
    timestamp: Optional[datetime] = None
    customer_id: Optional[int] = None
    price: Optional[int] = None
