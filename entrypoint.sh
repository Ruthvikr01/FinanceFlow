#!/bin/bash
# Entrypoint script to run both Streamlit and health check server

set -e

echo "=== FinanceFlow startup ==="
python --version
python -m pip --version
python - <<'PY'
from importlib import metadata

packages = [
	"streamlit",
	"sqlalchemy",
	"psycopg2-binary",
	"python-dotenv",
	"pandas",
	"plotly",
	"reportlab",
	"pdfplumber",
	"bcrypt",
	"sentry-sdk",
]

for package_name in packages:
	try:
		print(f"{package_name}={metadata.version(package_name)}")
	except metadata.PackageNotFoundError:
		print(f"{package_name}=NOT INSTALLED")
PY

trap 'kill "$HEALTH_PID" 2>/dev/null || true' EXIT

# Start health check server in background
python src/health_check.py &
HEALTH_PID=$!

# Start Streamlit app in foreground
streamlit run main.py --server.port=8501 --server.address=0.0.0.0
