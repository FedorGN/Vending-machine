from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import SessionLocal
from app.db.init_db import init_db

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    init_db(db)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    html_content = """
    <html>
        <body>
            <h3>Swagger documentation is avaliable on the address <a href="http://localhost:8000/docs">http://localhost:8000/docs</a></h3>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
