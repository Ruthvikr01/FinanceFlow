FROM python:3.11-slim   

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.2

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8501 8502

ENTRYPOINT ["./entrypoint.sh"]
