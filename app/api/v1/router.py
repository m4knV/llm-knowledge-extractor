from fastapi import APIRouter

from .endpoints import analysis, health, search

api_router = APIRouter()

# Endpoint routers
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
