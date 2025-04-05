import logging
import os
import sys


from dotenv import load_dotenv
load_dotenv()
from app.core.auth_util import VerifyToken
print("CWD",os.getcwd())


from fastapi.security import HTTPBearer


from fastapi_pagination import add_pagination, response

from starlette.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.DEBUG,
                    stream=sys.stdout)


from fastapi import FastAPI, APIRouter

token_auth_scheme = HTTPBearer()

def create_app() -> FastAPI:


    tags_metadata = [

    ]

    app = FastAPI(
        title="Sebigu HittaSkolan API",
        description="",
        version="1.0.0",
        terms_of_service="",
        openapi_tags=tags_metadata,
    )

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_pagination(app)

    from app.routers import (
        schools
    )

    main_router = APIRouter()

    main_router.include_router(schools.router)

    app.include_router(main_router, prefix="/api/v1")


    logging.info("App created")
    return app


app = create_app()

#celery = app.celery_app


