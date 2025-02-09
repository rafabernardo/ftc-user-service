from contextlib import contextmanager
from typing import Generator

from core.settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

settings = get_settings()
engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_postgresql_session() -> Generator[Session, None, None]:
    """
    Context manager to provide a transactional scope around operations.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e from e
    finally:
        db.close()
