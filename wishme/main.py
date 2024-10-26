from fastapi import FastAPI


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
        "onComplete": "Ok"
    },
)
