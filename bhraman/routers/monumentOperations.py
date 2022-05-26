from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from bhraman import models, schemas, database, hashing
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/operations",
    tags=['Operations -by monument employ']
)

get_db = database.get_db


@router.post('/Category', response_model=schemas.ShowCategory)
def create_Category(request: schemas.Category, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_category = models.Category(
        name=request.name, occupancy=request.occupancy, emp_id=current_user.ref_id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# add scanner


@router.post('/{id}/scanner', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowScanner)
def create_scanner(id, request: schemas.Scanner, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    cat = db.query(models.Category).filter(models.Category.id == id).first()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Category with the id {id} is not available")
    new_scanner = models.Scanner(
        desc=request.desc, emp_id=current_user.ref_id, cat_id=id)
    db.add(new_scanner)
    db.commit()
    db.refresh(new_scanner)
    return new_scanner


@router.post('scanner/{id}', response_model=schemas.ShowUser)
def create_scanner_user(id, request: schemas.User, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(models.Scanner).filter(
        models.Scanner.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Scanner with the id {id} is not available")

    new_user = models.User(role=request.role,
                           email=request.email, password=hashing.Hash.bcrypt(request.password), ref_id=id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
