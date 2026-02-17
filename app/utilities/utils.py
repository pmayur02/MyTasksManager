from passlib.context import CryptContext
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str):

    try:
        return pwd_context.hash(password)
    except Exception as e:
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password hashing failed: {str(e)}"
        )


def verify_password(plain_password: str, hashed_password: str):

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password verification failed: {str(e)}"
        )
