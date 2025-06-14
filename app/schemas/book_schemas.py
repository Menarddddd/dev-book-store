from pydantic import BaseModel
from typing import List



class CreateBook(BaseModel):
    title: str
    author: str
    genre: List[str]
    price: int
    available: bool
    