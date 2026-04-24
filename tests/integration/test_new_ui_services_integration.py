from __future__ import annotations

from io import BytesIO

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth import register_user
from app.database import Base
from app.services import compute_dashboard_stats, process_uploaded_statement
from app.utils import seed_default_categories


def _seeded_session_and_user_id() -> tuple[object, int]:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = SessionLocal()

    seed_default_categories(session)
    ok, _, user = register_user(session, "user@example.com", "Password123!", "User")
    assert ok and user is not None
    return session, int(user.id)


def test_new_ui_services_upload_to_dashboard_stats_happy_path() -> None:
    session, user_id = _seeded_session_and_user_id()
    try:
        frame = pd.DataFrame(
            [
                {"date": "2024-01-03", "details": "Whole Foods Market", "amount": -42.15},
                {"date": "2024-01-05", "details": "Train Ticket", "amount": -18.50},
            ]
        )
        buffer = BytesIO()
        frame.to_csv(buffer, index=False)

        inserted_count, message = process_uploaded_statement(
            session=session,
            user_id=user_id,
            file_name="statement.csv",
            file_bytes=buffer.getvalue(),
            source="bank",
        )
        assert inserted_count == 2
        assert "Imported 2 transactions" in message

        stats = compute_dashboard_stats(session, user_id)
        assert stats["total_transactions"] == 2
        assert stats["total_expenses"] > 0
    finally:
        session.close()
