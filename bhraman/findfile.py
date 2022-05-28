
from sqlalchemy.orm import Session
from . import database, schemas, models


get_db = database.get_db


def find_user(email, db: Session = next(get_db())):

    user = db.query(models.User).filter(models.User.email == email).first()
    return user


