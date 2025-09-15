from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role_id: int


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role_id: Optional[int] = None


class UserInDB(UserBase):
    id: int
    password_hash: str
    role_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    role_id: int
    role: Role
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
