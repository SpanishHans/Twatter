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



@router.post("/twatt", response_model=TwattRead)
async def create_twatt(
    twatt_in: TwattCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    # Step 1: Validate media files if provided
    if twatt_in.media_ids:
        # Fetch all media by IDs
        result = await session.execute(
            select(Media).where(Media.id.in_(twatt_in.media_ids))
        )
        media_list = result.scalars().all()

        # Check for missing media
        if len(media_list) != len(twatt_in.media_ids):
            found_ids = {media.id for media in media_list}
            missing_ids = set(twatt_in.media_ids) - found_ids
            raise HTTPException(
                status_code=404,
                detail=f"The following media IDs were not found: {list(missing_ids)}"
            )

        # Check for media already linked to another Twatt
        conflicted_ids = [str(media.id) for media in media_list if media.twatt_id is not None]

        if conflicted_ids:
            raise HTTPException(
                status_code=409,
                detail=f"The following media files are already linked to another Twatt: {conflicted_ids}"
            )

    # Step 2: Create the Twatt
    new_twatt = Twatt(
        content=twatt_in.content,
        twatt_type=twatt_in.twatt_type,
        user_id=current_user.id,
        parent_twatt_id=twatt_in.parent_twatt_id
    )

    session.add(new_twatt)
    await session.commit()
    await session.refresh(new_twatt)

    # Step 3: Link media files to the new Twatt (now we have new_twatt.id)
    if twatt_in.media_ids:
        await session.execute(
            update(Media)
            .where(Media.id.in_(twatt_in.media_ids))
            .values(twatt_id=new_twatt.id)
        )
        await session.commit()

    # Step 4: Fetch Twatt with media_files using selectinload
    result = await session.execute(
        select(Twatt).options(selectinload(Twatt.media_files)).where(Twatt.id == new_twatt.id)
    )
    twatt_with_media = result.scalar_one_or_none()

    if not twatt_with_media:
        raise HTTPException(status_code=500, detail="Failed to fetch created Twatt with media.")

    background_tasks.add_task(cleanup_orphan_media_background, current_user.id)
    # Step 5: Return TwattRead
    return TwattRead(
        id=twatt_with_media.id,
        content=twatt_with_media.content,
        twatt_type=twatt_with_media.twatt_type,
        user_id=twatt_with_media.user_id,
        parent_twatt_id=twatt_with_media.parent_twatt_id,
        media_files=[
            MediaIO(id=media.id, media_type=media.media_type)
            for media in twatt_with_media.media_files
        ]
    )








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
async def get_suggested_twatts(
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
    # Step 1: Fetch the Twatt
    result = await session.execute(
        select(Twatt).options(selectinload(Twatt.media_files)).where(Twatt.id == twatt_id)
    )
    twatt = result.scalar_one_or_none()

    if not twatt:
        raise HTTPException(status_code=404, detail="Twatt not found")

    if twatt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this Twatt")

    # Step 2: Update content if provided
    if twatt_in.content is not None:
        twatt.content = twatt_in.content

    # Step 3: Update media if provided
    if twatt_in.media_ids is not None:
        # Fetch new media by IDs
        result = await session.execute(
            select(Media).where(Media.id.in_(twatt_in.media_ids))
        )
        media_list = result.scalars().all()

        # Check for missing media
        if len(media_list) != len(twatt_in.media_ids):
            found_ids = {media.id for media in media_list}
            missing_ids = set(twatt_in.media_ids) - found_ids
            raise HTTPException(
                status_code=404,
                detail=f"The following media IDs were not found: {list(missing_ids)}"
            )

        # Check for conflicts: media linked to another Twatt
        conflicted_ids = [
            str(media.id)
            for media in media_list
            if media.twatt_id is not None and media.twatt_id != twatt_id
        ]

        if conflicted_ids:
            raise HTTPException(
                status_code=409,
                detail=f"The following media files are already linked to another Twatt: {conflicted_ids}"
            )

        # Unlink all current media from this Twatt
        await session.execute(
            update(Media)
            .where(Media.twatt_id == twatt_id)
            .values(twatt_id=None)
        )

        # Link new media to this Twatt
        await session.execute(
            update(Media)
            .where(Media.id.in_(twatt_in.media_ids))
            .values(twatt_id=twatt_id)
        )

    await session.commit()

    # Step 4: Fetch updated Twatt with media files again to return accurate data
    result = await session.execute(
        select(Twatt).options(selectinload(Twatt.media_files)).where(Twatt.id == twatt_id)
    )
    updated_twatt = result.scalar_one_or_none()

    if not updated_twatt:
        raise HTTPException(status_code=500, detail="Failed to fetch updated Twatt.")

    return TwattRead(
        id=updated_twatt.id,
        content=updated_twatt.content,
        twatt_type=updated_twatt.twatt_type,
        user_id=updated_twatt.user_id,
        media_files=[
            MediaIO(id=media.id, media_type=media.media_type)
            for media in updated_twatt.media_files
        ]
    )








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
