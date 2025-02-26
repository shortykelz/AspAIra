from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class ProfileUpdate(BaseModel):
    income_range: str
    financial_goals: List[str]
    risk_tolerance: str
    investment_experience: str
    preferred_investment_types: List[str]

class Token(BaseModel):
    access_token: str
    token_type: str

class UserInDB(UserBase):
    hashed_password: str 