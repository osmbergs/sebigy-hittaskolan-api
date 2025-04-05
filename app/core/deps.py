from typing import Generator, AsyncIterator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal
from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()  # 2
    try:
        yield db  # 3
    finally:
        db.close()  # 4





#async def get_async_db() -> AsyncIterator[AsyncSession]:
 #   session = AsyncSessionLocal()
 #   if session is None:
 #       raise Exception("DatabaseSessionManager is not initialized")
 #   try:
        # Setting the search path and yielding the session...
   #     await session.execute(
   #         text(f"SET search_path TO {SCHEMA}")
   #     )
 #       yield session
 #   except Exception:
 #       await session.rollback()
 #       raise
 #   finally:
        # Closing the session after use...
 #       await session.close()
