from sqlite3 import Timestamp
from typing import List, Optional
from unicodedata import category
from pydantic import BaseModel
from sqlalchemy import null


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
    dob: str
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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
