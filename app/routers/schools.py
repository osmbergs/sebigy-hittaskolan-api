from typing import List

from fastapi import APIRouter, Depends, Security, BackgroundTasks
from fastapi_pagination import Page, Params
from sqlalchemy.orm import Session

from app.core import deps
from app.core.auth_util import RequestContext, auth
from app.models.school import SchoolType

from app.schemas.school import SchoolResponseFullSchema, SchoolResponseListSchema, SchoolRefreshData
from app.services.school_service import SchoolService

router = APIRouter(
    prefix="/schools",
    tags=["schools"],
    dependencies=[],
)




@router.get("/", status_code=200, response_model=Page[SchoolResponseListSchema])
def get_schools(*,
                pagination_params: Params = Depends(),
                 db: Session = Depends(deps.get_db),
                 ctx: RequestContext = Security(auth.verify),
                 type: SchoolType,
                municipality_code: str,
)  -> Page[SchoolResponseListSchema]:
    school_service = SchoolService(db, ctx)
    ret=school_service.get_schools(pagination_params,municipality_code,type)

    return ret


@router.get("/{id}/", status_code=200, response_model=SchoolResponseFullSchema)
def get_school(*,
                db: Session = Depends(deps.get_db),
                ctx: RequestContext = Security(auth.verify),
               id:str,
                ) -> SchoolResponseFullSchema:
    school_service = SchoolService(db, ctx)
    ret = school_service.get_school_by_id(id)

    return ret


@router.put("/admin/refresh_recreate",response_model=SchoolRefreshData, status_code=200)  # 1
def admin_refresh (*,
    db:Session = Depends(deps.get_db),
    ctx: RequestContext = Security(auth.verify),

):
    school_service = SchoolService(db, ctx)
    ret = school_service.admin_recreate_all()



    return ret


@router.put("/admin/refresh_incomplete",response_model=SchoolRefreshData, status_code=200)  # 1
def admin_refresh (*,
    db:Session = Depends(deps.get_db),
    ctx: RequestContext = Security(auth.verify),

):
    school_service = SchoolService(db, ctx)
    ret = school_service.admin_refresh_incomplete()



    return ret
