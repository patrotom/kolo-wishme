from datetime import datetime

from .base_schema import BaseSchema


class OrganizationBase(BaseSchema):
    id: int
    name: str
    ico: str
    registration_number: str | None = None
    registration_office: str | None = None
    creation_date: datetime | None = None
    created_at: datetime


class OrganizationCreate(BaseSchema):
    name: str
    ico: str
    registration_number: str | None = None
    registration_office: str | None = None
    creation_date: datetime | None = None


class OrganizationUpdate(OrganizationCreate): ...


class OrganizationOut(BaseSchema):
    message: str
    data: OrganizationBase
