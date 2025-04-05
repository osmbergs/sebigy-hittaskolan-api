from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


engine = create_engine(  # 2
    settings.DB_URL,
    pool_size=20,
    max_overflow=0,
    #    echo=True
    #    echo=True
    # required for sqlite
    #  connect_args={"check_same_thread": False}
)

#async_engine = create_async_engine(  # 2
 #   settings.DB_URL,
  #  pool_size=20,
  #  max_overflow=0,
    #    echo=True
    #    echo=True
    # required for sqlite
    #  connect_args={"check_same_thread": False}
#)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
#AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine, expire_on_commit=False)