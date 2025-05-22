import secrets
from fastapi import APIRouter, Depends, Header, Response, Cookie, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import ExpiredSignatureError, PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.crud.crud_user import get_user_by_email, create_user
from app.services.security import verify_password, create_access_token, create_refresh_token, decode_token
import app.core.exceptions as api_exceptions
from app.core.config import settings
from app.schemas.error import ErrorResponse
from app.api.dependencies import get_current_user, require_role
from app.models.user import RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
        "/register",
        response_model=UserOut,
        status_code=status.HTTP_201_CREATED,
        responses={
        400: {"model": ErrorResponse, "description": "Email already registered"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.

    Create a new user account with the given email and password.

    Args:
        user_in: UserCreate schema containing email and password.
        db: AsyncSession for database interaction.

    Returns:
        The created UserOut schema.

    Raises:
        EmailAlreadyRegistered: If a user with this email already exists.
    """

    if await get_user_by_email(db, user_in.email):
        raise api_exceptions.EmailAlreadyRegistered(user_in.email)
    return await create_user(db, user_in)

@router.post(
        "/login",
        response_model=Token,
        responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Authenticate a user and set refresh+CSRF cookies.

    Verify the supplied credentials, issue access and refresh tokens,
    and store the refresh token (and a CSRF token) in cookies.

    Args:
        response: FastAPI Response used to set cookies.
        form_data: OAuth2PasswordRequestForm with username and password.
        db: AsyncSession for database interaction.

    Returns:
        A dict containing the access token and token type.

    Raises:
        InvalidCredentials: If the username or password is incorrect.
    """

    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise api_exceptions.InvalidCredentials()

    access_token = create_access_token({"sub": str(user.id), "email": str(user.email), "role": user.role.value})
    refresh_token = create_refresh_token({"sub": str(user.id), "role": user.role.value})
    csrf_token = secrets.token_urlsafe(16)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False, # TODO: Change to True for HTTPS
        samesite="none",
        path="/auth/refresh",
        max_age=settings.refresh_token_expire_minutes * 60,
    )

    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=False, # TODO: Change to True for HTTPS
        samesite="none",
        path="/auth/refresh",
        max_age=settings.refresh_token_expire_minutes * 60,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post(
        "/refresh",
        response_model=Token,
        responses={
        401: {"model": ErrorResponse, "description": "Invalid or expired refresh token"},
        403: {"model": ErrorResponse, "description": "CSRF validation failed"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def refresh(
    response: Response,
    refresh_token: str = Cookie(..., alias="refresh_token"),
    csrf_token_cookie: str = Cookie(..., alias="csrf_token"),
    csrf_token_header: str = Header(..., alias="X-CSRF-Token")
):
    """
    Rotate access and refresh tokens after validating CSRF and refresh token.

    Verify that the CSRF token in the header matches the CSRF cookie,
    decode and validate the refresh token, then issue new tokens.

    Args:
        response: FastAPI Response used to reset cookies.
        refresh_token: The refresh token from the HTTP-only cookie.
        csrf_token_cookie: The CSRF token stored in a JavaScript-readable cookie.
        csrf_token_header: The CSRF token sent in the X-CSRF-Token header.

    Returns:
        A dict containing the new access token and token type.

    Raises:
        CSRFInvalid: If the CSRF tokens do not match.
        TokenExpired: If the refresh token has expired.
        TokenInvalid: If the refresh token is otherwise invalid.
        TokenWrongScope: If the token’s scope is not "refresh_token".
    """

    if csrf_token_cookie != csrf_token_header:
        raise api_exceptions.CSRFInvalid()
    
    try:
        payload = decode_token(refresh_token)
    except ExpiredSignatureError:
        raise api_exceptions.TokenExpired()
    except PyJWTError:
        raise api_exceptions.TokenInvalid()
    
    if payload.get("scope") != "refresh_token":
        raise api_exceptions.TokenWrongScope()
    
    data = {"sub": payload["sub"], "email": payload["email"], "role": payload["role"]}
    new_access_token = create_access_token(data)
    new_refresh_token = create_refresh_token(data)
    new_csrf = secrets.token_urlsafe(16)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False, # TODO: Change to True for HTTPS in production
        samesite="none",
        path="/auth/refresh",
        max_age=settings.refresh_token_expire_minutes * 60,
    )

    response.set_cookie(
        key="csrf_token",
        value=new_csrf,
        httponly=False,
        secure=False, # TODO: Change to True for HTTPS
        samesite="none",
        path="/auth/refresh",
        max_age=settings.refresh_token_expire_minutes * 60,
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.get(
    "/verify",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def verify(user = Depends(get_current_user)) -> UserOut:
    """
    Verify that the request is authenticated and return the current user.

    Args:
        user: The authenticated user injected by the get_current_user dependency.

    Returns:
        The UserOut schema of the current user.
    """
    return user

@router.get(
    "/verify-admin",
    dependencies=[Depends(require_role(RoleEnum.CENTER_ADMIN))],
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        403: {"model": ErrorResponse, "description": "Not enough permission"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def verify_admin(user = Depends(get_current_user)) -> UserOut:
    """
    Verify that the request is authenticated by user with admin role and return the current user.

    Args:
        user: The authenticated user injected by the get_current_user dependency.

    Returns:
        The UserOut schema of the current user.
    """
    return user