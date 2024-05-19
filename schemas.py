# schema.py

from pydantic import BaseModel
from typing import List

class Policy(BaseModel):
    policy_number: str
    company_name: str
    coverage: str
    premium_amount: float
    expiration_date: str
    active: bool

    class Config:
        orm_mode = True
