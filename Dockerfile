FROM python:3.12-slim

RUN pip install --no-cache-dir poetry==2.2.1

WORKDIR /app

COPY pyproject.toml poetry.lock requirements.txt ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

RUN pip install --no-cache-dir -r requirements.txt

RUN python - <<'PY'
import importlib

for module_name in ("pdfplumber", "bcrypt", "plotly", "sentry_sdk"):
    importlib.import_module(module_name)

print("Verified runtime imports: pdfplumber, bcrypt, plotly, sentry_sdk")
PY

COPY . .

RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

EXPOSE 8501 8502

ENTRYPOINT ["./entrypoint.sh"]
