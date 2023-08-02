from fastapi import APIRouter

from settings.api import API_CONFIG


v1_router = APIRouter(prefix=f"/v{API_CONFIG.VERSION}")
