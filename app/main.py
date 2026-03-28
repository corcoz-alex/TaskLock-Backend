# tasklock-backend/app/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.api import auth, users, tasks

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(tasks.router, prefix = f"{settings.API_V1_STR}/tasks", tags=["Tasks"])

@app.get("/health", tags=["System"])
def health_check():
    """Provides a quick endpoint to verify the API is running."""
    return {"status": "ok", "project": settings.PROJECT_NAME}