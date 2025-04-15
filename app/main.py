from fastapi import FastAPI
from app.routers import routers_posts, routers_user

app = FastAPI()

app.include_router(routers_posts.router)
app.include_router(routers_user.router)
