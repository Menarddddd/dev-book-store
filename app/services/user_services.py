from app.core import hashing
from app.models.user import User
from ..schemas import user_schemas
from sqlalchemy.orm import Session
from ..core.errors import HTTPError, validateFormInput, run_validations
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from ..core import hashing
from ..core import security
from ..models.seller import Seller



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

