from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_admin: bool = False
    is_reader: bool = True
    is_editor: bool = False


from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False
    is_editor: bool = False
    is_reader: bool = False


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    is_editor: Optional[bool] = None
    is_reader: Optional[bool] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
