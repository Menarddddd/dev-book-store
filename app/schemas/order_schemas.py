from typing import List
from pydantic import BaseModel
from datetime import datetime



class OrderResponse(BaseModel):
    id: int
    customer_id: int
    books_id: List[int]
    time_order: datetime
    original_price: int
    discounted_amount: int
    total_amount: int

    model_config = {"from_attributes": True}

