from fastapi import APIRouter
from routes.napa import router as napa_router

router = APIRouter()

router.include_router(router=napa_router, prefix="/napa")
