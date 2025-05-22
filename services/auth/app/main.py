from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.core.exceptions import EmailAlreadyRegistered, InvalidCredentials
from app.core.config import settings

app = FastAPI(
    title="InnoTour Auth Service",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

if settings.mode == "development":
    origins = ["*"]
else:
    origins = ["https://privet-stepa.kr"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(EmailAlreadyRegistered)
async def handle_email_registered(request: Request, exc: EmailAlreadyRegistered):
    return JSONResponse(
        status_code=400,
        content={"error": "email_already_registered", "detail": str(exc)},
    )

@app.exception_handler(InvalidCredentials)
async def handle_invalid_credentials(request: Request, exc: InvalidCredentials):
    return JSONResponse(
        status_code=401,
        content={"error": "invalid_credentials", "detail": str(exc)},
    )

@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "detail": "An unexpected error occurred."},
    )

app.include_router(auth_router)

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
