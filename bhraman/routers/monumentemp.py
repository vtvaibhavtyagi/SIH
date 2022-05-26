
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from bhraman import models, schemas, database, hashing
from bhraman.routers import monument
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/employ",
    tags=['MonumentEmploy -by monument admin']
)

get_db = database.get_db


@router.post('/', response_model=schemas.ShowMonumentEmp)
def createEmp(request: schemas.MonumentEmp, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_monumentemp = models.MonumentEmp(fname=request.fname, lname=request.lname, designation=request.designation,
                                         dob=request.dob, mobile=request.mobile, timeStamp=request.timeStamp, monument_id=current_user.ref_id)
    db.add(new_monumentemp)
    db.commit()
    db.refresh(new_monumentemp)
    return new_monumentemp


@router.post('/{id}', status_code=status.HTTP_201_CREATED)
def create_monument_user(id, request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.MonumentEmp).filter(
        models.MonumentEmp.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Monument with the id {id} is not available")

    new_user = models.User(role=request.role,
                           email=request.email, password=hashing.Hash.bcrypt(request.password), ref_id=id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# @router.get('/', response_model=List[schemas.ShowMonumentEmp])
# def all(db: Session = Depends(get_db)):
#     monument = db.query(models.MonumentEmp).all()
#     return monument
