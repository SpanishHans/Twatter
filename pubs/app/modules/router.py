import os
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from fastapi.responses import FileResponse

from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shared.db.db_engine import get_db
from shared.auth.auth import get_current_user, CurrentUser
from shared.models.twatt import TwattType, Twatt, Media

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
        )
        db.add(media)
        await db.commit()
        await db.refresh(media)
        
        file_path = f"{UPLOAD_DIR}/{media.id}{file_extension}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
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

        return FileResponse(file_path, media_type=media.media_type)

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")






@router.post("/twatt", response_model=dict)
async def create_twatt(
    twatt_in: TwattCreate,
    session: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    is_quote = (
        twatt_in.twatt_type == TwattType.RETWEET and twatt_in.content is not None
    )

    new_twatt = Twatt(
        content=twatt_in.content,
        twatt_type=twatt_in.twatt_type,
        user_id=current_user.id,
        parent_twatt_id=twatt_in.parent_twatt_id
    )

    session.add(new_twatt)
    await session.commit()
    await session.refresh(new_twatt)
    
    if hasattr(twatt_in, "media_ids") and twatt_in.media_ids:
        await session.execute(
            update(Media)
            .where(Media.id.in_(twatt_in.media_ids))
            .values(twatt_id=new_twatt.id)
        )
        await session.commit()
        await session.refresh(new_twatt)

    return {
        "id": str(new_twatt.id),
        "twatt_type": new_twatt.twatt_type,
        "is_quote": is_quote
    }






@router.get("/twatts/{twatt_id}", response_model=TwattRead)
async def get_twatt_with_media(
    twatt_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    result = await session.execute(
        select(Twatt).options(selectinload(Twatt.media_files)).where(Twatt.id == twatt_id)
    )
    twatt = result.scalar_one_or_none()
    if not twatt:
        raise HTTPException(status_code=404, detail="Twatt not found")

    # Convert media to dict and inject URLs
    media_files = [MediaIO.model_validate(media) for media in twatt.media_files]


    return TwattRead(
        id=twatt.id,
        content=twatt.content,
        twatt_type=twatt.twatt_type,
        user_id=twatt.user_id,
        media_files=media_files
    )






@router.get("/twatts", response_model=List[TwattRead])
async def get_suggested_twats(
    session: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    stmt = (
        select(Twatt)
        .options(selectinload(Twatt.media_files))  # This eagerly loads media_files
        .where(Twatt.user_id != current_user.id)
        .order_by(Twatt.created_at.desc())
        .limit(20)
    )
    result = await session.execute(stmt)
    twatts = result.scalars().unique().all()

    return [
        TwattRead(
            id=twatt.id,
            content=twatt.content,
            twatt_type=twatt.twatt_type,
            user_id=twatt.user_id,
            media_files=[
                MediaIO(id=media.id, media_type=media.media_type)
                for media in twatt.media_files
            ]
        )
        for twatt in twatts
    ]






@router.put("/twatts/{twatt_id}", response_model=TwattRead)
async def update_twatt(
    twatt_id: UUID,
    twatt_in: TwattUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    result = await session.execute(select(Twatt).where(Twatt.id == twatt_id))
    twatt = result.scalar_one_or_none()

    if not twatt:
        raise HTTPException(status_code=404, detail="Twatt not found")

    if twatt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this Twatt")

    # Update content if provided
    if twatt_in.content is not None:
        twatt.content = twatt_in.content

    # Update media if provided
    if twatt_in.media_ids is not None:
        # Unlink existing media
        await session.execute(
            update(Media)
            .where(Media.twatt_id == twatt_id)
            .values(twatt_id=None)
        )

        # Link new media
        await session.execute(
            update(Media)
            .where(Media.id.in_(twatt_in.media_ids))
            .values(twatt_id=twatt_id)
        )

    await session.commit()
    await session.refresh(twatt)

    # Fetch updated media
    await session.refresh(twatt)
    return twatt  # FastAPI will serialize this with your TwattOut schema







@router.delete("/twatts/{twatt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_twatt(
    twatt_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    # Fetch the twatt
    result = await session.execute(
        select(Twatt).where(Twatt.id == twatt_id)
    )
    twatt = result.scalar_one_or_none()

    if not twatt:
        raise HTTPException(status_code=404, detail="Twatt not found")

    # Authorization check
    if twatt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this Twatt")

    # Delete the Twatt
    await session.delete(twatt)
    await session.commit()

    return  