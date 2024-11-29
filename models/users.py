from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    name: str = Field(..., min_length=3)
    surname: str = Field(..., min_length=3)
    email: EmailStr
    phone: str = Field(..., pattern=r"^[0-9]{10}$")
    password: str = Field(..., min_length=8)

    class Config:
        from_attributes = True
