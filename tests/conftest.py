from pathlib import Path
import sys

# Ensure src directory is importable so tests can import the FastAPI app
proj_root = Path(__file__).parent.parent.resolve()
src_dir = proj_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

try:
    # Prefer importing as a top-level module (app.py inside src/)
    from app import app as fastapi_app
except Exception:
    # Fallback: load module directly from file
    import importlib.util

    spec = importlib.util.spec_from_file_location("app", src_dir / "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fastapi_app = module.app

from fastapi.testclient import TestClient
import pytest


@pytest.fixture(scope="module")
def client():
    """Provides a TestClient for the FastAPI app."""
    with TestClient(fastapi_app) as c:
        yield c
