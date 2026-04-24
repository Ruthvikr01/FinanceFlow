FROM python:3.12-slim

RUN pip install --no-cache-dir poetry==2.2.1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

RUN pip install --no-cache-dir pdfplumber==0.11.7 plotly==6.7.0 bcrypt==5.0.0

RUN python - <<'PY'
import importlib

for module_name in ("pdfplumber", "bcrypt", "plotly"):
    importlib.import_module(module_name)

print("Verified runtime imports: pdfplumber, bcrypt, plotly")
PY

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8501 8502

ENTRYPOINT ["./entrypoint.sh"]
