from __future__ import annotations

from io import BytesIO

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth import login_user, register_user
from app.database import Base
from app.models import Category
from app.utils import parse_csv_statement, seed_default_categories


def _session():
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return SessionLocal()


def test_new_ui_auth_register_and_login_happy_path() -> None:
    session = _session()
    try:
        ok, msg, user = register_user(session, "user@example.com", "Password123!", "User")
        assert ok
        assert msg == "Account created successfully"
        assert user is not None

        login_ok, login_msg, login_user_obj = login_user(
            session, "user@example.com", "Password123!"
        )
        assert login_ok
        assert login_msg == "Login successful"
        assert login_user_obj is not None
        assert login_user_obj.email == "user@example.com"
    finally:
        session.close()


def test_new_ui_utils_seed_categories_and_parse_csv_happy_path() -> None:
    session = _session()
    try:
        seed_default_categories(session)
        uncategorized = session.query(Category).filter(Category.name == "Uncategorized").first()
        groceries = session.query(Category).filter(Category.name == "Groceries").first()
        assert uncategorized is not None
        assert groceries is not None

        frame = pd.DataFrame(
            [
                {"date": "2024-01-03", "details": "Whole Foods Market", "amount": -42.15},
                {"posted date": "2024-02-01", "merchant": "Uber Trip", "debit": "27.45", "credit": "0"},
            ]
        )
        buffer = BytesIO()
        frame.to_csv(buffer, index=False)
        parsed = parse_csv_statement(buffer.getvalue().decode("utf-8"))

        # One standard amount row + one debit/credit row.
        assert len(parsed) == 2
        assert parsed[0]["description"] == "Whole Foods Market"
        assert parsed[1]["description"] == "Uber Trip"
    finally:
        session.close()
