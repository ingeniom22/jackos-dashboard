from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Session, select
from backend.models import (
    Transaction,
    TransactionCreate,
    TransactionRead,
    TransactionUpdate,
)
from backend.database import create_db_and_tables, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:3000", "localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


@app.get("/api/get_all_transactions", response_model=list[TransactionRead])
def get_all_transactions():
    with Session(engine) as session:
        transactions = session.exec(select(Transaction)).all()
        return transactions


@app.get("/api/get_transaction/{id}", response_model=TransactionRead)
def get_transaction(id: int):
    with Session(engine) as session:
        # statement = select(Transaction).where(Transaction.id == id)
        transaction = session.get(Transaction, id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction


@app.post("/api/create_transaction", response_model=TransactionRead)
def create_transaction(transaction: TransactionCreate):
    with Session(engine) as session:
        transaction = Transaction(
            customer_id=transaction.customer_id,
            timestamp=transaction.timestamp,
            price=transaction.price,
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction


@app.patch("/api/update_transaction/{id}", response_model=TransactionRead)
def update_transaction(transaction_id: int, transaction: TransactionUpdate):
    with Session(engine) as session:
        db_transaction = session.get(Transaction, transaction_id)
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        transaction_data = transaction.dict(exclude_unset=True)
        for k, v in transaction_data.items():
            setattr(db_transaction, k, v)
        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction)
        return db_transaction


@app.delete("/api/delete_transaction/{id}")
def delete_transaction(transaction_id: int):
    with Session(engine) as session:
        transaction = session.get(Transaction, transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        session.delete(transaction)
        session.commit()
        return {"success": True}


@app.get("/api/forecast")
def forecast_revenue(interval: int):
    return {"graph": f"test-{interval}"}
