from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


def build_database_url() -> str:
    if settings.database_url:
        return settings.database_url
    if settings.use_sqlite_fallback:
        return "sqlite:///./app.db"
    return (
        f"mysql+pymysql://{settings.mysql_user}:{settings.mysql_password}@"
        f"{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_db}"
    )


DATABASE_URL = build_database_url()
engine_kwargs = {"echo": False}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db() -> None:
    global engine, SessionLocal

    from app.db.models import user, interview  # noqa: F401

    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError:
        if DATABASE_URL.startswith("mysql") and settings.use_sqlite_fallback:
            sqlite_url = "sqlite:///./app.db"
            engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=False)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            Base.metadata.create_all(bind=engine)
        else:
            raise
