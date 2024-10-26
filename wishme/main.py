from fastapi import FastAPI

from wishme.api.routers import (
    auth_router,
    accounts_router,
    products_router,
    wishes_router,
    users_router,
    organizations_router,
)


app = FastAPI(
    description="WishMe API",
    title="WishMe",
    version="0.1.0",
    contact={"name": "Tomas Patro", "email": "tomas.patro@gmail.com"},
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "layout": "BaseLayout",
        "filter": True,
        "tryItOutEnabled": True,
        "onComplete": "Ok",
    },
)

app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(products_router)
app.include_router(wishes_router)
app.include_router(users_router)
app.include_router(organizations_router)
