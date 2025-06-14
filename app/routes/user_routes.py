from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.book_schemas import AllBookReponse
from ..schemas import user_schemas
from ..database.database import get_db
from ..services import user_services
from ..models.book import Book
from ..core.security import get_current_user



route = APIRouter(
    tags=["User"]
)


@route.post("/token", status_code=status.HTTP_200_OK)
def login(formData: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return user_services.login_service(formData, db)


@route.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(formData: user_schemas.CreateUser, db: Session = Depends(get_db)):
    return user_services.create_user_service(formData, db)

@route.get("/get_books", status_code=status.HTTP_200_OK, response_model=List[AllBookReponse])
def get_books(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Book).all()
