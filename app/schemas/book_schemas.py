from pydantic import BaseModel
from typing import List



class CreateBook(BaseModel):
    title: str
    author: str
    genre: List[str]
    price: int
    available: bool
    

class AllBookReponse(BaseModel):
    id: int
    title: str
    author: str
    genre: List[str]
    price: int
    available: bool
    seller_id: int

    model_config = {
        "from_attributes": True
    }
