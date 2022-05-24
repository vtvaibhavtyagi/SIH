
from enum import unique
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    email = Column(String)
    password = Column(String)

    monument = relationship('Monuments', back_populates="creator")

# all Users admin, monuments,monumentEmp, scanners


class Monuments(Base):

    __tablename__ = "monument"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    pincode = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="monument")


# class MonumentEmp(Base):

#     __tablename__ = "monumentemp"
#     id = Column(Integer, primary_key=True, index=True)
#     emp_fname = Column(String)
#     emp_lname = Column(String)
#     emp_role = Column(String)
#     emp_dob = Column(Date)
#     emp_email = Column(String, unique=True, index=True)
#     emp_mbno = Column(Integer)
#     emp_timeStamp = Column(datetime)


# class Scanner(Base):
#     __tablename__ = "scanners"
#     id = Column(Integer, primary_key=True, index=True)


# class WebResources(Base):

#     __tablename__ = "webresources"
#     id = Column(Integer, primary_key=True, index=True)
#     wr_name = Column(String)
#     wr_desc = Column(String)
#     wr_file = Column(String)


# class Category(Base):
#     __tablename__ = "category"
#     cat_id = Column(Integer, primary_key=True, index=True)
#     cat_name = Column(String)


# class RateCard(Base):
#     __tablename__ = "ratecard"
#     rc_id = Column(Integer, primary_key=True, index=True)
#     rc_nation = Column(Boolean, default=True)
#     rc_amount = Column(Integer)


# class Day(Base):
#     __tablename__ = "day"
#     id = Column(Integer, primary_key=True, index=True)
#     day_name = Column(String)
#     day_status = Column(Boolean, default=True)
