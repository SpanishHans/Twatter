from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


from shared.models.twatt import TwattType

class MediaIO(BaseModel):
    id: UUID = Field(..., examples=[UUID("11266cf0-14a1-48f6-9f9c-d6afd17b0555")])
    media_type: str = Field(..., examples=["image/png", "image/jpeg", "video/mp4"])

    class Config:
        from_attributes = True





class TwattCreate(BaseModel):
    content: Optional[str] = Field(None, max_length=280, examples=["This is a twatt."])
    parent_twatt_id: Optional[UUID] = Field(None, examples=["123e4567-e89b-12d3-a456-426614174000"])
    twatt_type: TwattType = Field(..., examples=["original"])
    media_ids: Optional[List[UUID]] = Field(default_factory=list, examples=[["d290f1ee-6c54-4b01-90e6-d701748f0851"]])
    
class TwattUpdate(BaseModel):
    content: Optional[str] = Field(None, max_length=280, examples=["This is a twatt."])
    media_ids: Optional[List[UUID]] = Field(default_factory=list, examples=[["d290f1ee-6c54-4b01-90e6-d701748f0851"]])

class TwattRead(BaseModel):
    id: UUID
    content: Optional[str]
    twatt_type: TwattType
    user_id: UUID
    media_files: List[MediaIO] = []

    class Config:
        from_attributes = True