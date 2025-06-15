from typing import List
from fastapi.responses import JSONResponse
from fastapi import status
from app.core import hashing
from app.schemas import book_schemas
from app.services import book_services
from app.services.user_services import check_age, check_names_length, check_password_has_int, check_password_length, check_username_length
from ..schemas.seller_schemas import CreateSeller
from sqlalchemy.orm import Session
from ..models.seller import Seller
from ..models.order import Order
from ..core.errors import HTTPError, run_validations



def create_seller_service(formData: CreateSeller, db: Session):
    user = db.query(Seller).filter(Seller.username == formData.username).first()
    if user:
        HTTPError.bad_request("Username is already taken!")

    run_validations([
        (check_names_length(formData.first_name), "First name must be atleast 3 characters long"),
        (check_names_length(formData.last_name), "Last name must be atleasat 3 characters long"),
        (check_age(formData.age), "Age cannot be zero and must be a number"),
        (check_username_length(formData.username), "Username must be atleast 7 characters long"),
        (check_password_length(formData.password), "Password must be atleast 7 characters long"),
        (check_password_has_int(formData.password), "Password must contain atleast any number")
    ])

    hashed_password = hashing.get_hash_password(formData.password)

    new_user = Seller(
        first_name = formData.first_name,
        last_name = formData.last_name,
        age = formData.age,
        username = formData.username,
        password = hashed_password,
        role = Seller.__name__.lower()
    )

    db.add(new_user)
    db.commit()
    
    return JSONResponse(
        status_code=201,
        content={"message": f"Seller account for {formData.username} created successfully"}
    )


def validate_seller(role):
    return role == "seller"


def post_books_online_service(books: List[book_schemas.CreateBook], db: Session, current_user: Seller):

    validate_result = validate_seller(current_user.role)
    if not validate_result:
        HTTPError.unauthorized("User is not allowed to post books online")

    seller_id = current_user.id

    for book in books:
        book_services.create_book(book, db, seller_id)

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": "Books created successfully!"}
    )


def get_orders_service(db: Session, current_user: Seller):
    validate_result = validate_seller(current_user.role)
    if not validate_result:
        HTTPError.unauthorized("User is not allowed to see all orders")

    orders = db.query(Order).all()
    return orders
