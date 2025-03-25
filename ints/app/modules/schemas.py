from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class LikeCreate(BaseModel):
    user_id: UUID = Field(..., examples=[UUID("e2f96f23-8b9a-4f78-8b4e-91d5cbe98498")])
    twatt_id: UUID = Field(..., examples=[UUID("f981f9cf-081e-47d1-8b3f-d5bbf5fd3400")])

    class Config:
        from_attributes = True

class LikeRead(BaseModel):
    id: UUID
    user_id: UUID
    twatt_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
