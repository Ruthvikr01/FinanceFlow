FROM python:3.12-slim

RUN pip install --no-cache-dir poetry==2.3.1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8501 8502

ENTRYPOINT ["./entrypoint.sh"]
