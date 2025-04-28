from fastapi import FastAPI
from app.routers import routers_posts, routers_user, routers_login

app = FastAPI()

app.include_router(routers_login.router)
app.include_router(routers_posts.router)
app.include_router(routers_user.router)
