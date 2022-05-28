
from typing import List
from fastapi import APIRouter, status, HTTPException
from .. import models, schemas, hashing, database
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/admin",
    tags=['Admin -by admin']

)

get_db = database.get_db


@router.post("/")
def create_admin(request1: schemas.Admin, request2: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == request2.email).all()

    if user:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                            details=f"User already Register")

    new_admin = models.Admin(name=request1.name, desig=request1.desig)

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    new_user = models.User(role=request2.role,
                           email=request2.email, password=hashing.Hash.bcrypt(request2.password), ref_id=new_admin.id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_admin


# @router.post("/{id}")
# def create_admin_user(id, request: schemas.User, db: Session = Depends(get_db)):

#     user = db.query(models.Admin).filter(models.Admin.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             details=f"Admin with the id {id} is not available")

#     new_user = models.User(role=request2.role,
#                            email=request2.email, password=hashing.Hash.bcrypt(request2.password), ref_id=id)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


@router.get("/", response_model=List[schemas.ShowAdmin])
def all(db: Session = Depends(get_db)):
    user = db.query(models.Admin).all()
    return user


@router.get("/{id}", response_model=schemas.ShowAdmin)
def show_admin(id, db: Session = Depends(get_db), current_email: schemas.TokenData = Depends(get_current_user)):
    user = db.query(models.Admin).filter(models.Admin.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Admin with the id {id} is not available")
    return user


# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update(id, request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     user = db.query(models.User).filter(models.User.id == id)

#     if not user.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with id {id} not found")
#     user.update(request)
#     db.commit()
#     return 'updated'


# @router.delete('{id}', status_code=status.HTTP_204_NO_CONTENT)
# def remove(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     db.query(models.User).filter(models.User.id ==
#                                  id).delete(synchronize_session=False)
#     db.commit()
#     return 'removed'
