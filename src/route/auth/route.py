from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import service
from src import schema
from src.models import User
from .schema import SignupSchema
from ..dependencies import acquire_session
from .dependencies import validate_signup_schema, validate_signin_schema

router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=schema.Token, operation_id="auth.signup")
async def signup(
    body: SignupSchema = Depends(validate_signup_schema),
    session: AsyncSession = Depends(acquire_session),
):
    user = await service.create_user(session, body)

    return await service.create_token(session, user)


@router.post("/signin", response_model=schema.Token, operation_id="auth.signin")
async def login(
    user: User = Depends(validate_signin_schema),
    session: AsyncSession = Depends(acquire_session),
):
    return await service.create_token(session, user)
