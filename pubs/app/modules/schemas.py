from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from uuid import UUID


from shared.models.twatt import TwattType

class MediaIO(BaseModel):
    id: UUID = Field(..., examples=[UUID("11266cf0-14a1-48f6-9f9c-d6afd17b0555")])
    media_type: str = Field(..., examples=["image/png", "image/jpeg", "video/mp4"])

    class Config:
        from_attributes = True







class TwattCreate(BaseModel):
    content: Optional[str] = Field(None, max_length=280)
    parent_twatt_id: Optional[UUID] = None
    twatt_type: TwattType
    media_ids: Optional[List[UUID]] = Field(default_factory=list)

    @model_validator(mode='after')
    def validate_twatt(self):
        has_content = bool(self.content and self.content.strip())
        has_media = bool(self.media_ids)

        # no parent an both
        if self.twatt_type == TwattType.ORIGINAL:
            if self.parent_twatt_id:
                raise ValueError("Original twatts must not have a parent_twatt_id")
            if not has_content and not has_media:
                raise ValueError("Original twatts must have content or media (or both)")
        
        # parent an both
        elif self.twatt_type == TwattType.REPLY:
            if not self.parent_twatt_id:
                raise ValueError("Reply twatts must have a parent_twatt_id")
            if not has_content and not has_media:
                raise ValueError("Reply twatts must have content or media (or both)")

        # parent and none
        elif self.twatt_type == TwattType.RETWEET:
            if not self.parent_twatt_id:
                raise ValueError("Retweets must have a parent_twatt_id")
            if has_content or has_media:
                raise ValueError("Retweets cannot have content or media")

        # parent an both
        elif self.twatt_type == TwattType.QUOTE:
            if not self.parent_twatt_id:
                raise ValueError("Quote twatts must have a parent_twatt_id")
            if not has_content and not has_media:
                raise ValueError("Quote twatts must have content or media (or both)")

        else:
            raise ValueError(f"Unknown twatt_type: {self.twatt_type}")

        return self
    
class TwattUpdate(BaseModel):
    content: Optional[str] = Field(None, max_length=280, examples=["This is a twatt."])
    media_ids: Optional[List[UUID]] = Field(default_factory=list, examples=[["d290f1ee-6c54-4b01-90e6-d701748f0851"]])

class TwattRead(BaseModel):
    id: UUID
    content: Optional[str]
    twatt_type: TwattType
    user_id: UUID
    parent_twatt_id: Optional[UUID] = None
    media_files: List[MediaIO] = []

    class Config:
        from_attributes = True
