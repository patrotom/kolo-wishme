import uvicorn

from alembic.config import Config
from alembic import command


if __name__ == "__main__":
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
