from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from wishme.db.database import get_db
from wishme.services.wishes_service import WishService
from wishme.schemas.wishes import WishCreate, WishUpdate, WishOut, WishOutDelete, WishesOutList

router = APIRouter(tags=["Wishes"], prefix="/wishes")
auth_scheme = HTTPBearer()


# Get All Wishes
@router.get("/", status_code=status.HTTP_200_OK, response_model=WishesOutList)
def get_all_wishes(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict:
    return WishService.get_all_carts(token, db, page, limit)


# Get Wish By User ID
@router.get("/{wish_id}", status_code=status.HTTP_200_OK, response_model=WishOut)
def get_wish(
    wish_id: int, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> dict:
    return WishService.get_cart(token, db, wish_id)


# Create New Wish
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WishOut)
def create_wish(
    wish: WishCreate, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> dict:
    return WishService.create_wish(token, db, wish)


# Update Existing Wish
@router.put("/{wish_id}", status_code=status.HTTP_200_OK, response_model=WishOut)
def update_wish(
    wish_id: int,
    updated_wish: WishUpdate,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict:
    return WishService.update_wish(token, db, wish_id, updated_wish)


# Delete Wish By User ID
@router.delete("/{wish_id}", status_code=status.HTTP_200_OK, response_model=WishOutDelete)
def delete_wish(
    wish_id: int, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> dict:
    return WishService.delete_wish(token, db, wish_id)
