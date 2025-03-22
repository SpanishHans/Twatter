from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import Optional
from datetime import datetime
from uuid import UUID

# --- Minimal user for internal stuff ---
class UserBase(BaseModel):
    id: UUID = Field(..., examples=["123e4567-e89b-12d3-a456-426614174000"])

    model_config = {
        "from_attributes": True
    }


# --- Register ---
class RegisterUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, examples=["cooluser"])
    email: EmailStr = Field(..., examples=["user@example.com"])
    password: SecretStr = Field(..., min_length=3, max_length=30, examples=["strongpassword123"])


# --- Login ---
class LoginUser(BaseModel):
    username: str = Field(..., examples=["cooluser"])
    password: SecretStr = Field(..., examples=["strongpassword123"])


# --- Profile Update (can change email + username) ---
class UserProfileUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=30, examples=["newusername"])
    email: Optional[EmailStr] = Field(None, examples=["newemail@example.com"])
    profile_picture: Optional[str] = Field(None, examples=["https://cdn.example.com/avatar.png"])
    biography: Optional[str] = Field(None, examples=["Lover of code, coffee, and cats."])


# --- What the client sees (GET /user/:id) ---
class UserPublic(UserBase):
    username: str = Field(..., examples=["cooluser"])
    email: EmailStr = Field(..., examples=["user@example.com"])
    profile_picture: Optional[str] = Field(None, examples=["https://cdn.example.com/avatar.png"])
    biography: Optional[str] = Field(None, examples=["Lover of code, coffee, and cats."])
    created_at: datetime = Field(..., examples=["2024-03-21T15:30:00Z"])

    model_config = {
        "from_attributes": True
    }
