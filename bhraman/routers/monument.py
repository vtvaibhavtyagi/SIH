from pyexpat import model
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from bhraman import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/monument",
    tags=['Monuments']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowMonument])
def all(db: Session = Depends(get_db)):
    monument = db.query(models.Monuments).all()
    return monument


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Monument, db: Session = Depends(get_db)):
    new_monument = models.Monuments(
        name=request.name, pincode=request.pincode, user_id=1)
    db.add(new_monument)
    db.commit()
    db.refresh(new_monument)
    return new_monument