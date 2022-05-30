
from cgitb import html
from typing import List
from fastapi import APIRouter, status, HTTPException,Request
from .. import models, schemas, hashing, database,JWToken
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from ..oauth2 import get_current_user,get_current_visitor
from ..hashing import Hash
from ..crypto import crypto_code
import razorpay
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates 


router = APIRouter(
    prefix="/visitor",
    tags=['visitor']

)

get_db = database.get_db

templates = Jinja2Templates(directory="bhraman/templates")

@router.post("/register")
def visitor_regist(request: schemas.Visitor, db: Session = Depends(get_db)):
    new_visitor = models.Visitor(vs_fname=request.vs_fname,vs_mname=request.vs_mname, vs_lname=request.vs_lname, vs_dob=request.vs_dob, vs_mbno=request.vs_mbno,vs_doctype=request.vs_doctype,vs_docno=request.vs_docno,vs_email=request.vs_email,vs_pass=hashing.Hash.bcrypt(request.vs_pass) )
    db.add(new_visitor)
    db.commit()
    db.refresh(new_visitor)
    return new_visitor

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    vs_user = db.query(models.Visitor).filter(
        models.Visitor.vs_email == request.username).first()

    if not vs_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not Hash.verify(vs_user.vs_pass, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    access_token = JWToken.create_access_token(data={"sub": vs_user.vs_email})

    return {"access_token": access_token, "token_type": "bearer"}




@router.post("/booking",response_class=HTMLResponse)
def booking(razor: Request, request: schemas.booking, db: Session = Depends(get_db),current_email: schemas.TokenData = Depends(get_current_visitor)):
    
    book_vsid=db.query(models.Visitor.vs_id).filter(models.Visitor.vs_email==current_email.email)
    rate_amount=db.query(models.RateCard.amount).filter(models.RateCard.id==request.rt_id)
    new_booking = models.booking(vs_id=book_vsid,ts_id=request.ts_id,rt_id=request.rt_id,bk_nop=request.bk_nop,bk_status=request.bk_status)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    client = razorpay.Client(auth=("rzp_test_2US1VhY6axic4K", "KKNn04uCaO48kXhN4dp7KYeA"))
    data = { "amount": rate_amount, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    
    return templates.TemplateResponse("payment.html",{"request": razor, "payment":payment})





# @router.get("/pay",response_class=HTMLResponse)
# def pay(request: Request):
    
#     client = razorpay.Client(auth=("rzp_test_2US1VhY6axic4K", "KKNn04uCaO48kXhN4dp7KYeA"))
#     data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
#     payment = client.order.create(data=data)
    
#     return templates.TemplateResponse("payment.html",{"request": request, "payment":payment})


@router.post("/pay_success_data")
def pay_success_data(request: schemas.payment, db: Session = Depends(get_db),current_email: schemas.TokenData = Depends(get_current_visitor)):
        new_payment = models.payment(vs_id=request.vs_id,bk_id=request.bk_id,pay_amount=request.pay_amount,pay_oid=request.pay_oid,pay_payid=request.pay_payid)
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)

        cipher_text=crypto_code.encrypt(request.bk_id)
        return(cipher_text)


@router.post("/scanner")
def scanner(request: schemas.scanner_verify, db: Session = Depends(get_db)):

    plain_text=crypto_code.decrypt(request.cipher_txt)
    return plain_text
    # scanner_verify=db.query(models.booking).filter(models.booking.bk_id=)


