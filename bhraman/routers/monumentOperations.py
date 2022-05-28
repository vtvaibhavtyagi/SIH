from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from bhraman import models, schemas, database, hashing
from ..oauth2 import get_current_user
from ..findfile import find_user

router = APIRouter(
    prefix="/operations",
    tags=['Operations -by monument employ']
)

get_db = database.get_db


@router.post('/Category', response_model=schemas.ShowCategory)
def create_Category(request: schemas.Category, db: Session = Depends(get_db), current_email: schemas.TokenData = Depends(get_current_user)):
    current_user = find_user(current_email.email)
    new_category = models.Category(
        name=request.name, occupancy=request.occupancy, emp_id=current_user.ref_id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# add scanner


@router.post('/{id}/scanner', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowScanner)
def create_scanner(id, request1: schemas.Scanner, request2: schemas.User, db: Session = Depends(get_db), current_email: schemas.TokenData = Depends(get_current_user)):

    user = db.query(models.User).filter(
        models.User.email == request2.email).all()

    if user:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                            details=f"User already Register")

    cat = db.query(models.Category).filter(models.Category.id == id).first()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Category with the id {id} is not available")
    current_user = find_user(current_email.email)
    new_scanner = models.Scanner(
        desc=request1.desc, emp_id=current_user.ref_id, cat_id=id)
    db.add(new_scanner)
    db.commit()
    db.refresh(new_scanner)
    new_user = models.User(role=request2.role,
                           email=request2.email, password=hashing.Hash.bcrypt(request2.password), ref_id=new_scanner.id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_scanner


# @router.post('scanner/{id}', response_model=schemas.ShowUser)
# def create_scanner_user(id, request: schemas.User, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     user = db.query(models.Scanner).filter(
#         models.Scanner.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             details=f"Scanner with the id {id} is not available")

#     new_user = models.User(role=request.role,
#                            email=request.email, password=hashing.Hash.bcrypt(request.password), ref_id=id)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


@router.post('/{id}/ratecard', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowRateCard)
def crate_rateCard(id, request: schemas.RateCard, db: Session = Depends(get_db), current_email: schemas.TokenData = Depends(get_current_user)):
    cat = db.query(models.Category).filter(models.Category.id == id).first()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Category with the id {id} is not available")
    current_user = find_user(current_email.email)
    rate = models.RateCard(
        nation=request.nation, amount=request.amount, emp_id=current_user.ref_id, cat_id=id)
    db.add(rate)
    db.commit()
    db.refresh()
    return rate


@router.post('/web_resources', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowWebResources)
def create_resources(request: schemas.WebResources, db: Session = Depends(get_db), current_email: schemas.TokenData = Depends(get_current_user)):
    current_user = find_user(current_email.email)
    new_web = models.WebResources(
        name=request.name, file=request.file, desc=request.desc, emp_id=current_user.ref_id)

    db.add(new_web)
    db.commit()
    db.refresh()
    return new_web


@router.post('/day', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowDay)
def create_day(request: schemas.Day, db: Session = Depends(get_db), current_email: schemas.TokenData = Depends(get_current_user)):
    current_user = find_user(current_email.email)
    new_day = models.Day(
        name=request.name, status=request.status, emp_id=current_user.ref_id)
    db.add(new_day)
    db.commit()
    db.refresh(new_day)
    return new_day


@router.post('/day/{id}/time', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowTime)
def create_time(request: schemas.Time, db: Session = Depends(get_db), current_email: schemas.TokenData = Depends(get_current_user)):
    current_user = find_user(current_email.email)
    new_time = models.Time(start=request.start, end=request.end,
                           emp_id=current_user.ref_id, day_id=id)
    db.add(new_time)
    db.commit()
    db.refresh(new_time)
