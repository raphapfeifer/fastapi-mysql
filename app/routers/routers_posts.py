from fastapi import Depends
from fastapi import APIRouter, HTTPException, status
import app.models.models as models
from app.db.database import engine
from app.db.configuration import db_dependency
from app.depends.depends_auth import token_verifier
from app.schemas.post_schema import PostBase

router = APIRouter(dependencies=[Depends(token_verifier)])
models.Base.metadata.create_all(bind=engine)


@router.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()


@router.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post was not found")
    return post


@router.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post was not found")
    db.delete(db_post)
    db.commit()
