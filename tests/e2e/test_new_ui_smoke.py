"""E2E smoke tests for the new main.py + app/views UI.

These tests are intentionally light happy-path checks.
Set E2E_BASE_URL (for example http://localhost:8501) to run them.
"""

from __future__ import annotations

import os

import pytest

playwright = pytest.importorskip("playwright.sync_api")
Page = playwright.Page


@pytest.fixture(scope="session")
def base_url() -> str:
    value = os.getenv("E2E_BASE_URL")
    if not value:
        pytest.skip("Set E2E_BASE_URL to run e2e tests")
    return value


def test_new_ui_auth_page_renders_happy_path(page: Page, base_url: str) -> None:
    page.goto(base_url)

    assert page.locator("text=FinanceFlow").count() > 0
    assert page.locator("text=Sign In").count() > 0
    assert page.locator("text=Create Account").count() > 0
    assert page.locator('input[placeholder="you@example.com"]').count() > 0
    assert page.locator('input[placeholder="Enter your password"]').count() > 0


def test_new_ui_register_tab_inputs_exist(page: Page, base_url: str) -> None:
    page.goto(base_url)
    page.click("text=Create Account")

    assert page.locator('input[placeholder="Jane Doe"]').count() > 0
    assert page.locator('input[placeholder="At least 6 characters"]').count() > 0
    assert page.locator('input[placeholder="Re-enter password"]').count() > 0
    assert page.locator("button:has-text('Create Account')").count() > 0
