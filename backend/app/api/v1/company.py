from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.company import CompanyProfileRead, CompanyProfileUpdate
from app.services.company_service import CompanyService

router = APIRouter(prefix="/company", tags=["company"])


@router.get("/profile", response_model=CompanyProfileRead | None)
async def get_company_profile(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await CompanyService(session).get(current_user)


@router.put("/profile", response_model=CompanyProfileRead)
async def upsert_company_profile(
    payload: CompanyProfileUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await CompanyService(session).upsert(current_user, payload)
