from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.agency import router as agency_router
from app.core.exceptions import AgencyAlreadyRegistered, AgencyNotFound, PermissionRequired
from app.core.config import settings

app = FastAPI(
    title="InnoTour Agency Service",
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

@app.exception_handler(AgencyAlreadyRegistered)
async def handle_agency_registered(request: Request, exc: AgencyAlreadyRegistered):
    return JSONResponse(
        status_code=400,
        content={"error": "agency_already_registered", "detail": str(exc)},
    )

@app.exception_handler(AgencyNotFound)
async def handle_agency_not_found(request: Request, exc: AgencyNotFound):
    return JSONResponse(
        status_code=404,
        content={"error": "agency_not_found", "detail": str(exc)},
    )

@app.exception_handler(PermissionRequired)
async def handle_permission_req(request: Request, exc: AgencyNotFound):
    return JSONResponse(
        status_code=403,
        content={"error": "not_enough_permission", "detail": str(exc)},
    )

@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "detail": "An unexpected error occurred."},
    )

app.include_router(agency_router)

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
