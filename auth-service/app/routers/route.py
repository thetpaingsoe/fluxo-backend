from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, auth, schemas
from ..database import get_db

router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=schemas.TokenResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    hashed_pw = auth.hash_password(user.password)
    db_user = crud.create_user(db, user.username, user.email, hashed_pw)
    token = auth.create_access_token({"sub": str(db_user.id), "username": db_user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.TokenResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth.create_access_token({"sub": str(db_user.id), "username": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
