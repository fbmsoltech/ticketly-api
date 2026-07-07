import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import get_settings  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.seed.initial_data import seed_initial_data  # noqa: E402


def main() -> None:
    settings = get_settings()
    db = SessionLocal()
    try:
        seed_initial_data(db, settings)
    finally:
        db.close()


if __name__ == "__main__":
    main()
