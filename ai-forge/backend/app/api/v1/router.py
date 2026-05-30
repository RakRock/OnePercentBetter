from fastapi import APIRouter

from app.api.v1.routes import auth, evaluation, mentor, projects

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(mentor.router)
api_router.include_router(evaluation.router)
