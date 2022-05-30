from fastapi import FastAPI
import uvicorn

from bhraman.routers import admin, monument, monumentOperations, monumentemp, authentication, visitor

from . import models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()


models.Base.metadata.create_all(engine)


app.include_router(admin.router)
app.include_router(authentication.router)
app.include_router(monument.router)
app.include_router(monumentemp.router)
app.include_router(monumentOperations.router)
app.include_router(visitor.router)



if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
