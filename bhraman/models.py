
from datetime import datetime
from enum import unique
from turtle import back
from typing import Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from bhraman.routers import monument

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    ref_id = Column(Integer)

# all Users admin, monuments,monumentEmp, scanners


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    desig = Column(String)

    monument = relationship("Monuments", back_populates="creator")


class Monuments(Base):

    __tablename__ = "monument"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    pincode = Column(Integer)

    admin_id = Column(Integer, ForeignKey('admin.id'))
    creator = relationship("Admin", back_populates="monument")
    employ = relationship("MonumentEmp", back_populates="boss")


class MonumentEmp(Base):

    __tablename__ = "monumentemp"
    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String)
    lname = Column(String)
    designation = Column(String)
    dob = Column(String)
    mobile = Column(Integer)
    timeStamp = Column(String)
    monument_id = Column(Integer, ForeignKey('monument.id'))
    boss = relationship("Monuments", back_populates='employ')
    
    category = relationship("Category", back_populates="madeBy")
    scanner = relationship("Scanner", back_populates='madeBy')


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    occupancy = Column(Integer)
    emp_id = Column(Integer, ForeignKey('monumentemp.id'))
    madeBy = relationship("MonumentEmp", back_populates='category')
    scanner = relationship("Scanner", back_populates='category')


class Scanner(Base):
    __tablename__ = "scanners"
    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String)
    emp_id = Column(Integer, ForeignKey('monumentemp.id'))
    cat_id = Column(Integer, ForeignKey('category.id'))
    madeBy = relationship("MonumentEmp", back_populates='scanner')
    category = relationship("Category", back_populates='scanner')

# class WebResources(Base):

#     __tablename__ = "webresources"
#     id = Column(Integer, primary_key=True, index=True)
#     wr_name = Column(String)
#     wr_desc = Column(String)
#     wr_file = Column(String)


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
