from fastapi import Depends, Security
from sqlalchemy.orm import Session

from app.core.auth_util import auth, RequestContext
from app.core.deps import get_db


class BaseService:
    _db: Session
    _ctx: RequestContext
    def __init__(self, db: Session , ctx:RequestContext):
        self._db = db
        self._ctx = ctx


#        self._audit_service = AuditService()
