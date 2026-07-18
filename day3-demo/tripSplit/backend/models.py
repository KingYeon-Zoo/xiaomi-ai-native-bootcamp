from pydantic import BaseModel, Field
from typing import Optional


class TripCreate(BaseModel):
    name: str
    startDate: str
    endDate: str


class MemberAdd(BaseModel):
    name: str


class ExpenseCreate(BaseModel):
    name: str
    amount: float
    payer: str
    participants: list[str]
    category: str
    date: str
    note: Optional[str] = ""


class ExpenseUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    payer: Optional[str] = None
    participants: Optional[list[str]] = None
    category: Optional[str] = None
    date: Optional[str] = None
    note: Optional[str] = None
