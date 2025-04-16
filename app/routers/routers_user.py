from fastapi import APIRouter, HTTPException, status
import app.models.models as models
from app.db.database import engine
from app.db.configuration import db_dependency
from app.models.models import UserBase
from passlib.context import CryptContext

router = APIRouter()
models.Base.metadata.create_all(bind=engine)

cypt_context = CryptContext(schemes=["sha256_crypt"])


@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db_user.password = cypt_context.hash(db_user.password)
    db.add(db_user)
    db.commit()


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, details="User not found")
    return user
