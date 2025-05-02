from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from decouple import config
from passlib.context import CryptContext
import app.models.models as models
from app.db.database import engine
from app.schemas.user_schema import UserLogin
from app.db.configuration import db_dependency


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
crypt_context = CryptContext(schemes=["sha256_crypt"])
router = APIRouter()
models.Base.metadata.create_all(bind=engine)


@router.post("/login/", status_code=status.HTTP_200_OK)
async def login(
    db: db_dependency, request_form_user: OAuth2PasswordRequestForm = Depends()
):

    user = UserLogin(
        username=request_form_user.username, password=request_form_user.password
    )

    auth_data = create_token(user, db)
    return auth_data


def create_token(user: UserLogin, db: db_dependency, expires_in: int = 30):
    db_user = db.query(models.User).filter_by(username=user.username).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not crypt_context.verify(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    exp = datetime.utcnow() + timedelta(minutes=expires_in)

    payload = {"sub": user.username, "exp": exp}

    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "exp": exp.isoformat()}


def verify_token(access_token):
    try:
        data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid acess token"
        )

    # db_user = db.query(models.User).filter_by(username=data['sub']).first()

    # if db_user is None:
    #  raise HTTPException(
    #      status_code=status.HTTP_401_UNAUTHORIZED,
    #      detail='Invalid acess token'
    #  )
