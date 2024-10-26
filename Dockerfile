FROM python:3.11-slim

WORKDIR /wishme

RUN pip install --upgrade pip
RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction

COPY . .

LABEL name=kolo-wishme

CMD ["python", "run.py"]
