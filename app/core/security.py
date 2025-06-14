from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
from .settings import settings



def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": int(expire.timestamp())})
    access_token = jwt.encode(to_encode, settings.SECURITY_KEY, settings.ALGORITHM)
    return access_token

