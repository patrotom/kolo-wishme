from fastapi import APIRouter, Depends, status
from wishme.db.database import get_db
from wishme.services.organizations_service import OrganizationsService
from sqlalchemy.orm import Session
from fastapi.security.http import HTTPAuthorizationCredentials
from wishme.schemas.organizations import OrganizationCreate, OrganizationOut, OrganizationUpdate
from wishme.core.security import auth_scheme


router = APIRouter(tags=["Organizations"], prefix="/users/organizations")


@router.get("/get", status_code=status.HTTP_200_OK, response_model=OrganizationOut)
def get_organization(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict:
    return OrganizationsService.get_organization(db, token)


# Create New Organization
@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=OrganizationOut)
def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict:
    return OrganizationsService.create_organization(db, token, organization)


# Update Existing organization
@router.put("/update", status_code=status.HTTP_200_OK, response_model=OrganizationOut)
def update_organization(
    updated_organization: OrganizationUpdate,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict:
    return OrganizationsService.update_organization(db, token, updated_organization)
