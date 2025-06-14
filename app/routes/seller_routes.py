from typing import List
from fastapi import APIRouter
from fastapi import Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.services import seller_services
from ..database.database import get_db
from ..schemas import seller_schemas, book_schemas
from ..services import book_services
from ..models.seller import Seller
from ..core.errors import HTTPError
from ..core.security import get_current_user




route = APIRouter(
    tags=["Seller"]
)



@route.post("/create_seller", status_code=status.HTTP_201_CREATED)
def create_seller(formData: seller_schemas.CreateSeller, db: Session = Depends(get_db)):
    return seller_services.create_seller_service(formData, db)


@route.post("/post_books")
def post_books_online(books: List[book_schemas.CreateBook], db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role == "user":
        HTTPError.unauthorized("User is not allowed to post books online")

    seller_id = current_user.id

    for book in books:
        book_services.create_book(book, db, seller_id)

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": "Books created successfully!"}
    )