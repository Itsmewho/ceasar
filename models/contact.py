from pydantic import BaseModel, Field


class ContactModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=15)
    surname: str = Field(..., min_length=3, max_length=15)
    phone: str = Field(..., pattern=r"^\d{10,15}$")
    secure_id: str = Field(
        ...,
    )

    class Config:
        from_attributes = True
