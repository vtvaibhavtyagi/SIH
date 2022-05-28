from datetime import date, datetime
from sqlite3 import Timestamp
from typing import List, Optional
from unicodedata import category
from pydantic import BaseModel


class MonumentBase(BaseModel):
    name: str
    pincode: int


class Monument(MonumentBase):

    class Config():
        orm_mode = True


class AdminBase(BaseModel):
    name: str
    desig: str


class Admin(AdminBase):
    class Config():
        orm_mode = True


class UserBase(BaseModel):
    role: str
    email: str
    password: str


class User(UserBase):
    class Config():
        orm_mode = True


class MonumentEmpBase(BaseModel):
    fname: str
    lname: Optional[str] = None
    designation: str
    dob: date
    mobile: int
    timeStamp: Optional[Timestamp]


class MonumentEmp(MonumentEmpBase):
    class Config():
        orm_mode = True


class CategoryBase(BaseModel):
    name: str
    occupancy: Optional[int] = -1


class Category(CategoryBase):
    class Config():
        orm_mode = True


class ScannerBase(BaseModel):
    desc: Optional[str] = None


class Scanner(ScannerBase):
    class Config():
        orm_mode = True


class RateCardBase(BaseModel):
    naion: str
    amount: int


class RateCard(RateCardBase):
    class Config():
        orm_mode = True


class WebResourcesBase(BaseModel):
    name: str
    desc: str
    file: Optional[str] = None


class WebResources(WebResourcesBase):
    class Config():
        orm_mode = True


class DayBase(BaseModel):
    name: str
    status: Optional[bool] = True


class Day(DayBase):
    class Config():
        orm_mode = True


class TimeBase(BaseModel):
    start: datetime
    end: datetime


class Time(TimeBase):
    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    role: str
    email: str

    class Config():
        orm_mode = True


class ShowMonument(MonumentBase):
    admin_id: int
    creator: Admin
    employ: List[MonumentEmp] = []

    class Config():
        orm_mode = True


class ShowAdmin(AdminBase):
    monument: List[Monument] = []

    class Config():
        orm_mode = True


class ShowMonumentEmp(MonumentEmpBase):
    monument_id: int
    boss: Monument

    class Config():
        orm_mode = True


class ShowCategory(CategoryBase):
    emp_id: int
    madeBy: MonumentEmp

    class Config():
        orm_mode = True


class ShowScanner(ScannerBase):
    emp_id: int
    cat_id: int
    madeBy: MonumentEmp
    category: Category

    class Config():
        orm_mode = True


class ShowRateCard(RateCardBase):
    emp_id: int
    cat_id: int
    madeBy: MonumentEmp
    category: Category

    class Config():
        orm_mode = True


class ShowWebResources(WebResourcesBase):
    emp_id: int
    madeBy: MonumentEmp

    class Config():
        orm_mode = True


class ShowDay(DayBase):
    emp_id: int
    madeBy: MonumentEmp

    class Config():
        orm_mode = True


class ShowTime(TimeBase):
    emp_id: int
    day_id: int
    madeBy: MonumentEmp
    day: Day

    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
