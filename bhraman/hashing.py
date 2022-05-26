
from urllib import request
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import database

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)

    # def verifyUser(username:str,password:str, db: Session = Depends(database.get_db)):
