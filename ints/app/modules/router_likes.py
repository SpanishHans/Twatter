from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

import requests

from shared.db.db_engine import get_db
from shared.auth.auth import get_current_user, CurrentUser
from shared.models.twatt import Twatt, Media
from shared.middleware.cleanup_media import cleanup_orphan_media_background


router = APIRouter(tags=["Interacciones"])

