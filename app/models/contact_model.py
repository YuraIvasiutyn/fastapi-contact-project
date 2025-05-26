from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr


class ResponseMessageModel(BaseModel):
    message: str


class PostRequestModel(BaseModel):
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    email: EmailStr = Field(..., description="Address Email")
    phone_number: str = Field(..., description="Phone number")
    birthday: date = Field(..., description="Birthday format DD.MM.YYYY")


class PutRequestModel(BaseModel):
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    email: Optional[EmailStr] = Field(None, description="Address Email")
    phone_number: Optional[str] = Field(None, description="Phone number")
    birthday: Optional[date] = Field(None, description="Birthday format DD.MM.YYYY")


class DBModel(PostRequestModel):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GetAllResponseModel(BaseModel):
    contacts: List[DBModel]
    skip: int
    limit: int
