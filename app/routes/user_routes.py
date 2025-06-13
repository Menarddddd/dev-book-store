from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..schemas import user_schemas
from ..database.database import get_db
from ..services import user_services



route = APIRouter(
    tags=["User"]
)


@route.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(formData: user_schemas.CreateUser, db: Session = Depends(get_db)):
    return user_services.create_user_service(formData, db)
