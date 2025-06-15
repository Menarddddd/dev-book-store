from typing import List
from fastapi import APIRouter
from fastapi import Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas.order_schemas import OrderResponse
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
    return seller_services.post_books_online_service(books, db, current_user)


@route.get("/get_orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return seller_services.get_orders_service(db, current_user)

