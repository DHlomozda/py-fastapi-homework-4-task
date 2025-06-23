from datetime import date
from fastapi import UploadFile, Form, File, HTTPException, status
from pydantic import BaseModel, field_validator, HttpUrl
from validation import (
    validate_name,
    validate_image,
    validate_gender,
    validate_birth_date
)


class BaseProfileSchema(BaseModel):
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    info: str


class ProfileResponseSchema(BaseProfileSchema):
    id: int
    avatar: HttpUrl


class ProfileCreateRequestSchema(BaseProfileSchema):
    avatar: UploadFile

    @classmethod
    @field_validator("first_name", "last_name")
    def validate_name_field(cls, name: str) -> str:
        validate_name(name)
        return name.lower()

    @classmethod
    @field_validator("avatar")
    def validate_avatar_field(cls, avatar: UploadFile) -> UploadFile:
        validate_image(avatar)
        return avatar

    @classmethod
    @field_validator("gender")
    def validate_gender_field(cls, gender: str) -> str:
        validate_gender(gender)
        return gender

    @classmethod
    @field_validator("date_of_birth")
    def validate_date_of_birth_field(cls, date_of_birth: date) -> date:
        validate_birth_date(date_of_birth)
        return date_of_birth

    @classmethod
    @field_validator("info")
    def validate_info_field(cls, info: str, info_field) -> str:
        cleaned_info = info.strip()
        if not cleaned_info:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[{
                    "type": "value_error",
                    "loc": [info_field.field_name],
                    "msg": "Info field cannot be empty or contain only spaces.",
                    "input": info
                }]
            )
        return cleaned_info
