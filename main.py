from fastapi import FastAPI
from my_project.app import models
from my_project.app.database import engine
from my_project.app.routers import adverts, user, auth, polygon, feedback
from my_project.app.config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="advert app")

# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(adverts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(polygon.router)
app.include_router(feedback.router)

app.get("/")
def message():
    return {"message":"Hello world"}