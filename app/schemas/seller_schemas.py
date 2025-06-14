from pydantic import BaseModel


class CreateSeller(BaseModel):
    first_name: str
    last_name: str
    age: int
    username: str
    password: str


class SellBooks(BaseModel):
    pass

