from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker, scoped_session
from app.core.config import settings



celery_engine = create_engine(  # 2
    settings.DB_URL,
    poolclass=NullPool
)
SessionLocalCelery =scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=celery_engine, expire_on_commit=False))
