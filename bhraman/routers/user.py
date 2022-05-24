from http.client import HTTPException
from pyexpat import model
from typing import List
from fastapi import APIRouter, status

from bhraman.oauth2 import get_current_user
from .. import database, schemas, models, hashing
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status


router = APIRouter(
    prefix="/user",
    tags=['User']

)

get_db = database.get_db


@router.post("/", response_model=schemas.ShowUser)
def create(request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    new_user = models.User(role=request.role,
                           email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# @router.get("/", response_model=List[schemas.ShowUser])
# def all(db: Session = Depends(get_db)):
#     user = db.query(models.User).all()
#     return user


@router.get("/{id}", response_model=schemas.ShowUser)
def show(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"User with the id {id} is not available")
    return user


@router.delete('{id}', status_code=status.HTTP_204_NO_CONTENT)
def remove(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db.query(models.User).filter(models.User.id ==
                                 id).delete(synchronize_session=False)
    db.commit()
    return 'removed'


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    user.update(request)
    db.commit()
    return 'updated'
