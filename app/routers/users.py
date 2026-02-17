from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.user import user,userResponse,userUpdate,Token
from app.database.db import get_db
from app.models.models import User
from sqlalchemy.orm import Session
from app.utilities.utils import hash_password, verify_password
from app.utilities.authentication import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


userRouter = APIRouter(
    prefix="/users"
)

@userRouter.post("/register-user", response_model=Token)
def registerUser(user: user, db: Session = Depends(get_db)):
    try:
        existingUser = db.query(User).filter(
            User.email == user.email,
            User.status == "active" 
        ).first()

        if existingUser:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashPassword = hash_password(user.password)
        user.password = hashPassword
        newUser = User(
            name=user.name,
            email=user.email,
            password=user.password,
            status=user.status.value
        )
        db.add(newUser) 
        db.commit() 
        db.refresh(newUser) 
        access_token = create_access_token(data={"sub": newUser.email})
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong: {str(e)}"
        )


@userRouter.get("/", response_model=List[userResponse])
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).filter(User.status == "active").all()
        return users

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch users: {str(e)}"
        )
    

@userRouter.get("/{user_id}", response_model=userResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(
            User.id == user_id,
            User.status == "active"
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return user

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user: {str(e)}"
        )
    

@userRouter.put("/update/{user_id}")
def update_user(
    user_id: int,
    user_data: userUpdate,
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.id == user_id, User.status == "active").first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )

        # Update fields if provided
        if user_data.name is not None:
            user.name = user_data.name
        if user_data.email is not None:
            # Check for duplicate email
            existing_user = db.query(User).filter(
                User.email == user_data.email, User.id != user_id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            user.email = user_data.email
        if user_data.password is not None:
            user.password = hash_password(user_data.password)
        if user_data.status is not None:
            user.status = user_data.status

        db.commit()
        db.refresh(user)
        return {
            "message": "User updated successfully!",
            "status": 200
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )


@userRouter.delete("/delete/{user_id}")
def deleteUser(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(
            User.id == user_id,
            User.status == "active"                             
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )

        user.status = "inactive"
        db.commit()
        db.refresh(user)
        return {
            "status": status.HTTP_204_NO_CONTENT,
            "message": "User deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to deactivate user: {str(e)}"
        )
    

@userRouter.post("/login", response_model=Token)
def login(login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        existEmail = db.query(User).filter(
            User.email == login.username,
            User.status == "active"
        ).first()

        if not existEmail: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No User found"
            )

        isValid = verify_password(login.password, existEmail.password)
        if not isValid:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid credentials"
            )

        access_token = create_access_token(data={"email": existEmail.email, "id": existEmail.id})
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to Login: {str(e)}"
        )
