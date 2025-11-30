"""Pytest configuration for tests."""

import pytest


@pytest.fixture
def anyio_backend():
    """Use asyncio as the backend for anyio tests."""
    return "asyncio"
