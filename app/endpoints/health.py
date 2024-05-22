from fastapi import APIRouter, Security

from utils.auth import auth

router = APIRouter(prefix='/health', tags=['Health'])


@router.get('')
async def health_check() -> dict[str, str]:
    return {'result': 'ok'}
