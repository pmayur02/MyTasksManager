from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends,HTTPException, status
from app.utilities.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user import TokenData


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str= Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verifyToken(token,credentials_exception)


def verifyToken(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            raise credentials_exception
        token_data = TokenData(email=payload.get("email"),id=payload.get("id"))
    except JWTError:
        raise credentials_exception


    return token_data