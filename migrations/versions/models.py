from datetime import datetime
from typing import List, Optional


from pydantic import BaseModel

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: str


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = None

class Trade(BaseModel):
    id: int
    user_id: int
    currency: str
    side: str
    price: float
    amount: float