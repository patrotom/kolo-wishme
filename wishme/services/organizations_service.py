from sqlalchemy.orm import Session
from fastapi.security.http import HTTPAuthorizationCredentials

from wishme.models.models import Organization, User
from wishme.schemas.organizations import OrganizationCreate, OrganizationUpdate
from wishme.utils.responses import ResponseHandler
from wishme.core.security import get_current_user


class OrganizationsService:
    @staticmethod
    def get_organization(db: Session, token: HTTPAuthorizationCredentials) -> dict:
        user_id = get_current_user(token)

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            ResponseHandler.not_found_error("User", user_id)

        organization: Organization = user.organization

        if not organization:
            ResponseHandler.not_found_error("Organization")

        return ResponseHandler.get_single_success(organization.name, organization.id, organization)

    @staticmethod
    def create_organization(db: Session, token: HTTPAuthorizationCredentials, organization: OrganizationCreate) -> dict:
        user_id = get_current_user(token)

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            ResponseHandler.not_found_error("User", user_id)

        db_organization: Organization = user.organization

        if db_organization:
            return ResponseHandler.get_single_success(db_organization.name, db_organization.id, db_organization)

        db_organization = Organization(id=None, **organization.model_dump())

        db.add(db_organization)
        db.commit()
        db.refresh(db_organization)

        user.organization_id = db_organization.id

        db.commit()

        return ResponseHandler.create_success(db_organization.name, db_organization.id, db_organization)

    @staticmethod
    def update_organization(
        db: Session, token: HTTPAuthorizationCredentials, updated_organization: OrganizationUpdate
    ) -> dict:
        user_id = get_current_user(token)

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            ResponseHandler.not_found_error("User", user_id)

        organization: Organization = user.organization

        if not organization:
            ResponseHandler.not_found_error("Organization")

        for key, value in updated_organization.model_dump().items():
            setattr(organization, key, value)

        db.commit()
        db.refresh(organization)

        return ResponseHandler.update_success(organization.name, organization.id, organization)
