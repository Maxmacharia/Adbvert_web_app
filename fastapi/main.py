from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import adverts, user, auth, polygon, feedback
from app.config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(adverts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(polygon.router)
app.include_router(feedback.router)

app.get("/")
def message():
    return {"message":"Hello world"}