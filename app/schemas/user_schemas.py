from pydantic import BaseModel



class CreateUser(BaseModel):
    first_name: str
    last_name: str
    age: int
    username: str
    password: str
    member_type: str
