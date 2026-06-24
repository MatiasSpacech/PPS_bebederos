"""Compatibility entrypoint for running the FastAPI application.

The real application lives under app.main so the project can grow with a
standard package layout while keeping this top-level module available for
simple execution commands.
"""

from app.main import app

