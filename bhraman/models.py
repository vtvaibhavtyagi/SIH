
from enum import unique
from time import time
from turtle import back
from typing import Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date,DateTime
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
    dob = Column(Date)
    mobile = Column(Integer)
    timeStamp = Column(String)
    monument_id = Column(Integer, ForeignKey('monument.id'))
    boss = relationship("Monuments", back_populates='employ')

    category = relationship("Category", back_populates="madeBy")
    scanner = relationship("Scanner", back_populates='madeBy')
    rate = relationship("RateCard", back_populates='madeBy')
    web = relationship("WebResources", back_populates='modeBy')
    day = relationship("Day", back_populates='modeBy')
    time = relationship("Time", back_populates='modeBy')


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    occupancy = Column(Integer)
    emp_id = Column(Integer, ForeignKey('monumentemp.id'))
    madeBy = relationship("MonumentEmp", back_populates='category')
    scanner = relationship("Scanner", back_populates='category')
    rate = relationship("RateCard", back_populates='category')


class Scanner(Base):
    __tablename__ = "scanners"
    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String)
    emp_id = Column(Integer, ForeignKey('monumentemp.id'))
    cat_id = Column(Integer, ForeignKey('category.id'))
    madeBy = relationship("MonumentEmp", back_populates='scanner')
    category = relationship("Category", back_populates='scanner')


class RateCard(Base):
    __tablename__ = "ratecard"
    id = Column(Integer, primary_key=True, index=True)
    nation = Column(String, default="Indian")
    amount = Column(Integer)
    emp_id = Column(Integer, ForeignKey('monumentemp.id'))
    cat_id = Column(Integer, ForeignKey('category.id'))
    madeBy = relationship("MonumentEmp", back_populates='rate')
    category = relationship("Category", back_populates='rate')


class WebResources(Base):

    __tablename__ = "webresources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    file = Column(String)
    desc = Column(String)
    emp_id = Column(Integer, ForeignKey('monumentemp.id'))
    madeBy = relationship("MonumentEmp", back_populates='web')


class Day(Base):
    __tablename__ = "day"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(Boolean, default=True)
    emp_id = Column(Integer, ForeignKey('monumentemp.id'))
    madeBy = relationship("MonumentEmp", back_populates='day')
    day = relationship("Time", back_populates='time')
    
class Time(Base):
    __tablename__ = "time"
    id = Column(Integer, primary_key=True, index=True)
    start = Column(DateTime)
    end = Column(DateTime)
    emp_id = Column(Integer, ForeignKey('monumentemp.id'))
    day_id = Column(Integer,ForeignKey('day.id'))
    madeBy = relationship("MonumentEmp", back_populates='time')
    day = relationship("Daystart", back_populates='time')
    
    
