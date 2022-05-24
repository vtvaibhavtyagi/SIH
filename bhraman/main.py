from fastapi import FastAPI

from bhraman.routers import authentication, monument,user

from . import models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()


models.Base.metadata.create_all(engine)


app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(monument.router)
