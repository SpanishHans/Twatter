import os
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks

from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shared.db.db_engine import get_db
from shared.auth.auth import get_current_user, CurrentUser
from shared.models.twatt import Twatt, Media
from shared.middleware.cleanup_media import cleanup_orphan_media_background

from modules.schemas import MediaIO, TwattCreate, TwattRead, TwattUpdate
from modules.mime import get_file_extension

router = APIRouter(tags=["Publicaciones"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/app/uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=MediaIO)
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    # Validate file type
    allowed_types = ["image/png", "image/jpeg", "video/mp4"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is missing.")

    try:
        file_extension = get_file_extension(file.content_type)

        media = Media(
            media_type=file.content_type,
            user_id=current_user.id  # Pass user_id here
        )
        db.add(media)
        await db.commit()
        await db.refresh(media)

        file_path = f"{UPLOAD_DIR}/{media.id}{file_extension}"
        with open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                f.write(chunk)

        return MediaIO(id=media.id, media_type=media.media_type)

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")






@router.get("/media/{media_id}")
async def get_media(
    media_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    try:

        result = await db.execute(select(Media).where(Media.id == media_id))
        media = result.scalar_one_or_none()

        if not media:
            raise HTTPException(status_code=404, detail="Media not found")

        file_extension = get_file_extension(media.media_type)
        file_path = os.path.join(UPLOAD_DIR, f"{media.id}{file_extension}")

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(
            file_path,
            media_type=media.media_type,
            filename=f"{media.id}{file_extension}"
        )

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
