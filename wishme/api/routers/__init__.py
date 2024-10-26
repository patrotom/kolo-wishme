from .auth_router import router as auth_router
from .accounts_router import router as accounts_router
from .products_router import router as products_router
from .wishes_router import router as wishes_router
from .users_router import router as users_router
from .organizations_router import router as organizations_router


__all__ = ["auth_router", "accounts_router", "products_router", "wishes_router", "users_router", "organizations_router"]
