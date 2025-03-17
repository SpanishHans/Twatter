from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr = Field(
        json_schema_extra={'examples': ['juan@example.com']}
    )
    profile_picture: Optional[str] = Field(
        None, json_schema_extra={'examples': ['https://example.com/profile.jpg']}
    )
    biography: Optional[str] = Field(
        None, json_schema_extra={'examples': ['Passionate about technology and innovation.']}
    )

class UserCredentials(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30,
        json_schema_extra={'examples': ['juanjo23']}
    )
    password: SecretStr = Field(
        min_length=3,
        max_length=30,
        json_schema_extra={'examples': ['SecureP@ssw0rd']}
    )

class NewUser(UserBase, UserCredentials):
    pass

class UserLogin(UserCredentials):
    pass
