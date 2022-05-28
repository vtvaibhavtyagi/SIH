
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from bhraman import models, schemas, database, hashing
from bhraman.routers import monument
from ..oauth2 import get_current_user
from ..findfile import find_user


router = APIRouter(
    prefix="/employ",
    tags=['MonumentEmploy -by monument admin']
)

get_db = database.get_db


@router.post('/', response_model=schemas.ShowMonumentEmp)
def createEmp(request1: schemas.MonumentEmp, request2: schemas.User, db: Session = Depends(get_db),current_email: schemas.TokenData = Depends(get_current_user)):
    current_user = find_user(current_email.email)
    new_monumentemp = models.MonumentEmp(fname=request1.fname, lname=request1.lname, designation=request1.designation,
                                         dob=request1.dob, mobile=request1.mobile, timeStamp=request1.timeStamp, monument_id=current_user.ref_id)
    db.add(new_monumentemp)
    db.commit()
    db.refresh(new_monumentemp)
    new_user = models.User(role=request2.role,
                           email=request2.email, password=hashing.Hash.bcrypt(request2.password), ref_id=new_monumentemp.id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_monumentemp


# @router.post('/{id}', status_code=status.HTTP_201_CREATED)
# def create_monument_user(id, request: schemas.User, db: Session = Depends(get_db)):
#     user = db.query(models.MonumentEmp).filter(
#         models.MonumentEmp.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             details=f"Monument with the id {id} is not available")

#     new_user = models.User(role=request.role,
#                            email=request.email, password=hashing.Hash.bcrypt(request.password), ref_id=id)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @router.get('/', response_model=List[schemas.ShowMonumentEmp])
# def all(db: Session = Depends(get_db)):
#     monument = db.query(models.MonumentEmp).all()
#     return monument
