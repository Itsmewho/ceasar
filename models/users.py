from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    name: str = Field(..., min_length=3)
    surname: str = Field(..., min_length=3)
    email: EmailStr
    phone: str = Field(..., regex=r"^\d{10,15}$")
    password: str = Field(..., min_length=8)

    class Config:
        orm_mode = True
