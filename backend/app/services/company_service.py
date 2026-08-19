from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Organization, OrganizationMembership, User
from app.schemas.company import CompanyProfileRead, CompanyProfileUpdate


class CompanyService:
    """Perfil empresarial único vinculado al acceso de la compañía."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _organization_for(self, user: User) -> Organization | None:
        stmt = (
            select(Organization)
            .join(
                OrganizationMembership,
                OrganizationMembership.organization_id == Organization.id,
            )
            .where(OrganizationMembership.user_id == user.id)
            .order_by(Organization.id)
        )
        return (await self.session.execute(stmt)).scalars().first()

    @staticmethod
    def _read(organization: Organization) -> CompanyProfileRead:
        metadata = organization.metadata_ or {}
        important = [
            organization.name,
            organization.legal_name,
            organization.tax_id,
            metadata.get("industry"),
            metadata.get("fiscal_address"),
            metadata.get("worker_count"),
            metadata.get("representative_name"),
            metadata.get("study_lead_name"),
            metadata.get("contact_email"),
            metadata.get("locations"),
        ]
        completeness = round(sum(bool(value) for value in important) / len(important) * 100)
        return CompanyProfileRead(
            id=organization.id,
            public_id=organization.public_id,
            name=organization.name,
            legal_name=organization.legal_name,
            tax_id=organization.tax_id,
            organization_type=organization.organization_type,
            status=organization.status,
            industry=metadata.get("industry"),
            ciiu_code=metadata.get("ciiu_code"),
            fiscal_address=metadata.get("fiscal_address"),
            worker_count=metadata.get("worker_count"),
            representative_name=metadata.get("representative_name"),
            study_lead_name=metadata.get("study_lead_name"),
            contact_email=metadata.get("contact_email"),
            contact_phone=metadata.get("contact_phone"),
            brand_color=metadata.get("brand_color", "#D59B27"),
            locations=metadata.get("locations") or [],
            signatories=metadata.get("signatories") or [],
            completeness_pct=completeness,
            created_at=organization.created_at,
            updated_at=organization.updated_at,
        )

    async def get(self, user: User) -> CompanyProfileRead | None:
        organization = await self._organization_for(user)
        return self._read(organization) if organization is not None else None

    async def upsert(self, user: User, payload: CompanyProfileUpdate) -> CompanyProfileRead:
        organization = await self._organization_for(user)
        if organization is None:
            organization = Organization(
                name=payload.name,
                legal_name=payload.legal_name,
                tax_id=payload.tax_id,
                organization_type=payload.organization_type,
                status="ACTIVE",
            )
            self.session.add(organization)
            await self.session.flush()
            self.session.add(
                OrganizationMembership(
                    organization_id=organization.id,
                    user_id=user.id,
                    role_code="COMPANY_OWNER",
                    permissions={"company_access": True},
                )
            )
        organization.name = payload.name
        organization.legal_name = payload.legal_name
        organization.tax_id = payload.tax_id
        organization.organization_type = payload.organization_type
        organization.metadata_ = {
            **(organization.metadata_ or {}),
            "industry": payload.industry,
            "ciiu_code": payload.ciiu_code,
            "fiscal_address": payload.fiscal_address,
            "worker_count": payload.worker_count,
            "representative_name": payload.representative_name,
            "study_lead_name": payload.study_lead_name,
            "contact_email": payload.contact_email,
            "contact_phone": payload.contact_phone,
            "brand_color": payload.brand_color,
            "locations": [item.model_dump() for item in payload.locations],
            "signatories": [item.model_dump() for item in payload.signatories],
        }
        await self.session.commit()
        await self.session.refresh(organization)
        return self._read(organization)
