FROM python:3.12-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false && \
		poetry install --only main --no-interaction --no-ansi

COPY . .

CMD ["sh", "-c", "python3 -m alembic upgrade head && \
    exec uvicorn app.main:app --host 0.0.0.0 --port 80"]
