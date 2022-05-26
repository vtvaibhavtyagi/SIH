from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database,hashing
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/monument",
    tags=['Monuments -by admin']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_monument(request: schemas.Monument, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_monument = models.Monuments(
        name=request.name, pincode=request.pincode, admin_id=current_user.ref_id)
    db.add(new_monument)
    db.commit()
    db.refresh(new_monument)
    return new_monument


@router.post('/{id}', status_code=status.HTTP_201_CREATED)
def create_monument_user(id, request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.Monuments).filter(models.Monuments.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Monument with the id {id} is not available")

    new_user = models.User(role=request.role,
                           email=request.email, password=hashing.Hash.bcrypt(request.password), ref_id=id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@router.get('/', response_model=List[schemas.ShowMonument])
def all(db: Session = Depends(get_db)):
    monument = db.query(models.Monuments).all()
    return monument


# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update(id, request: schemas.Monument, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     user = db.query(models.Monuments).filter(models.Monuments.id == id)

#     if not user.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Monument with id {id} not found")
#     user.update(request)
#     db.commit()
#     return 'updated'


# @router.delete('{id}', status_code=status.HTTP_204_NO_CONTENT)
# def remove(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     db.query(models.Monuments).filter(models.Monuments.id ==
#                                       id).delete(synchronize_session=False)
#     db.commit()
#     return 'removed'
