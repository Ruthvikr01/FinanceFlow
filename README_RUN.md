# Running PersonalFinanceAnalyzer (using Poetry)

Prerequisites:
- Python 3.9+
- Poetry (https://python-poetry.org/)
- PostgreSQL reachable via `DATABASE_URL` in `.env`

Quickstart using Poetry:

1. Install Poetry (if not already installed):

   - macOS / Linux: `curl -sSL https://install.python-poetry.org | python3 -`
   - Windows: follow the Windows installer instructions on the Poetry website.

2. Initialize a Poetry project (if the repository does not already contain `pyproject.toml`):

   ```bash
   poetry init --no-interaction
   ```

3. Add runtime dependencies using Poetry:

   ```bash
   poetry add streamlit SQLAlchemy psycopg2-binary python-dotenv pandas
   ```

4. Install dependencies and spawn a virtual environment shell:

   ```bash
   poetry install
   poetry shell
   ```

5. Ensure `.env` contains the `DATABASE_URL` connection string (this repo already includes a sample `.env`).

6. Initialize the local database (optional):

   - Use `db/schema.sql` to create tables and `db/seed.sql` to populate sample data in your Postgres instance.

7. Run the Streamlit app via Poetry:

   ```bash
   poetry run streamlit run main.py
   ```

8. Optional: run via Docker image:

   ```bash
   docker build -t personalfinanceanalyzer:latest .
   docker run --env-file .env -p 8501:8501 -p 8502:8502 personalfinanceanalyzer:latest
   ```

9. Health checks:

   - App health endpoint: `http://localhost:8502/health`
   - Streamlit-compatible endpoint: `http://localhost:8502/_stcore/health`

10. Sentry setup (optional):

   Add `SENTRY_DSN` to `.env` to enable error reporting.

11. Logging with rotation:

   - App logs are written to `logs/app.log`.
   - Rotation keeps 3 backups: `app.log.1`, `app.log.2`, `app.log.3`.

12. UpTimeRobot setup:

   - Create a new HTTP monitor in UpTimeRobot.
   - Monitor URL: `https://<your-app-domain>/health` (or `/_stcore/health`).
   - Recommended interval: 5 minutes.

13. Continuous deployment hook:

   - Create GitHub Actions secret `DEPLOY_HOOK_URL`.
   - Add your Render (or provider) deploy hook URL as the secret value.
   - The workflow file `.github/workflows/deploy.yml` builds the Docker image and triggers this hook.

Notes:
- The app uses SQLAlchemy `create_engine` to connect to the database using `DATABASE_URL`.
- If you prefer not to use Poetry, you can still use a venv and `pip install -r requirements.txt`.
