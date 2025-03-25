import uuid
from sqlalchemy import delete

from shared.db.db_engine import SessionLocal  # Your sessionmaker
from shared.models.twatt import Media

async def cleanup_orphan_media_background(user_id: uuid.UUID):
    async with SessionLocal() as db:  # Reuse your shared session factory
        await db.execute(
            delete(Media)
            .where(Media.user_id == user_id)
            .where(Media.twatt_id.is_(None))
        )
        await db.commit()
