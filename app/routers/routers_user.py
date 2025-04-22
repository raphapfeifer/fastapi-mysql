from typing import List
from fastapi import APIRouter, HTTPException, status
import app.models.models as models
from app.db.database import engine
from app.db.configuration import db_dependency
from app.schemas.user_schema import UserBase
from passlib.context import CryptContext

router = APIRouter()
models.Base.metadata.create_all(bind=engine)
user: UserBase
users: List[UserBase]

cypt_context = CryptContext(schemes=["sha256_crypt"])


@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db_user.password = cypt_context.hash(db_user.password)
    db.add(db_user)
    db.commit()


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserBase)
async def read_user(user_id: int, db: db_dependency) -> UserBase:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, details="User not found")
    return user


@router.get("/users", status_code=status.HTTP_200_OK, response_model=List[UserBase])
async def read_all_users(db: db_dependency) -> List[UserBase]:
    users = db.query(models.User).all()
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return users
