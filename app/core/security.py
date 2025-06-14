from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt

from app.models.seller import Seller
from .settings import settings
from .errors import HTTPError
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database.database import get_db
from ..models.user import User
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")



def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": int(expire.timestamp())})
    access_token = jwt.encode(to_encode, settings.SECURITY_KEY, settings.ALGORITHM)
    return access_token


def get_current_user(token = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECURITY_KEY, algorithms=settings.ALGORITHM)
        username = payload.get("sub")
        exp = payload.get("exp")
        role = payload.get("role")

        if username is None or exp is None:
            HTTPError.unauthorized("You are not authorized")
        
        now = datetime.now(timezone.utc).timestamp()
        if now > exp:
            HTTPError.unauthorized("Your token is expired")

        user = db.query(User).filter(User.username == username).first()
        if not user:
            user = db.query(Seller).filter(Seller.username == username).first()

        if not user:
            HTTPError.not_found("User is not found!")
        
        return user
    except JWTError:
        HTTPError.bad_request("Bad request, something went wrong!")

