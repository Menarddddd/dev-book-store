import random
from typing import List
from app.core import hashing
from app.models.book import Book
from app.models.user import User
from ..schemas import user_schemas
from sqlalchemy.orm import Session
from ..core.errors import HTTPError, validateFormInput, run_validations
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from ..core import hashing
from ..core import security
from ..models.seller import Seller
from ..models.order import Order
from datetime import datetime
from .order_services import get_member_discount



#Seller also use these
def check_names_length(name: str):
    return len(name) >= 3

def check_username_length(username: str):
    return len(username) >= 7

def check_password_length(password: str):
    return len(password) >= 7

def check_password_has_int(password: str):
    return any(char.isdigit() for char in password)

def check_age(age: int):
    return isinstance(age, int) and age > 0






# seller also use this
def login_service(formData: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter(User.username == formData.username).first()
    if not user:
        user = db.query(Seller).filter(Seller.username == formData.username).first()

    if not user:
        HTTPError.not_found("User is not found")
        
    result = hashing.verify_password(formData.password, user.password)
    if not result:
        HTTPError.unauthorized("Password is incorrect")

    access_token = security.create_access_token(data={"sub": formData.username})
    return {"access_token": access_token, "token_type": "bearer"}



def create_user_service(formData: user_schemas.CreateUser, db: Session):
    user = db.query(User).filter(User.username == formData.username).first()
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

    new_user = User(
        first_name = formData.first_name,
        last_name = formData.last_name,
        age = formData.age,
        username = formData.username,
        password = hashed_password,
        member_type = formData.member_type,
        role = User.__name__.lower()
    )

    db.add(new_user)
    db.commit()
    
    return JSONResponse(
        status_code=201,
        content={"message": f"User account for {formData.username} created successfully"}
    )


def generate_unique_order_id(db: Session, length=10):
    while True:
        order_id = "".join(random.choices("0123456789", k=length))
        exists = db.query(Order).filter(Order.id == order_id).first()
        if not exists:
            return order_id
        

def get_time_now():
    now = datetime.now()
    formatted = now.strftime("%Y-%m-%d %H:%M")
    return formatted

def get_book(title: str, db:Session):
    book = db.query(Book).filter(Book.title == title).first()
    return book

def order_books_service(orderedBooks: List[user_schemas.OrderedBooks], db: Session, current_user: User):
    books_id = []
    original_price = 0
    discounted_amount = 0
    total_amount = 0
    print(orderedBooks)

    for book in orderedBooks:
        print(original_price)
        print(discounted_amount)
        print(total_amount)
        print(f"book: {book}")
        bookObject = get_book(book.title, db)
        if bookObject is None:
            HTTPError.not_found("Book is not found!")
        books_id.append(bookObject.id)
        result_discount = get_member_discount(current_user.member_type, bookObject.price)
        discounted_amount += result_discount["discounted_amount"]
        total_amount += result_discount["total_amount"]
        original_price += bookObject.price



    order_id = generate_unique_order_id(db)

    new_order = Order(
        id=order_id,
        customer_id=current_user.id,
        books_id=books_id,
        time_order=datetime.now(),
        original_price=original_price,
        discounted_amount=discounted_amount,
        total_amount=total_amount
    )
    db.add(new_order)
    db.commit()
    return "Ordered books placed successfully"
