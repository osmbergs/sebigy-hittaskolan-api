import os
from typing import Union

from pydantic.v1 import BaseSettings


print("config:Environ is " + str(os.environ.get("FASTAPI_ENV")))


class ProductionConfig(BaseSettings):
    #DB_URL: str = str(os.environ.get("DB_URL"))
    DB_URL: str = "cockroachdb://gpc:UfK17k3A6FyXLzdthx6N_g@umber-auk-9889.j77.aws-eu-central-1.cockroachlabs.cloud:26257/sebigy-hittaskolan?sslmode=verify-full"
    AUTH0_DOMAIN: str = str(os.environ.get("AUTH0_DOMAIN"))
    AUTH0_API_AUDIENCE: str = str(os.environ.get("AUTH0_API_AUDIENCE"))
    AUTH0_ISSUER: str = str(os.environ.get("AUTH0_ISSUER"))
    AUTH0_ALGORITHMS: str = str(os.environ.get("AUTH0_ALGORITHMS"))
    CELERY_BROKER_URL: str = str(os.environ.get("CELERY_BROKER_URL"))
    CELERY_RESULT_BACKEND: str = str(os.environ.get("CELERY_RESULT_BACKEND"))
    CELERY_WORKER_NAME_PREFIX: str = str(os.environ.get("CELERY_WORKER_NAME_PREFIX"))


class StagingConfig(ProductionConfig):
    pass


class DevelopmentConfigAWS(ProductionConfig):
    pass


class DevelopmentConfigDockerCompose(ProductionConfig):
    pass


class DevelopmentConfig(ProductionConfig):

    DB_URL:str="cockroachdb://gpc:UfK17k3A6FyXLzdthx6N_g@umber-auk-9889.j77.aws-eu-central-1.cockroachlabs.cloud:26257/sebigy-hittaskolan?sslmode=verify-full"

#    DB_URL: str = "postgresql+pg8000://postgres:postgres@localhost/sebigy-hittaskolan"

    CELERY_BROKER_URL: str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379"
    CELERY_WORKER_NAME_PREFIX: str = "local"


class DevelopmentDockerLocalConfig(ProductionConfig):
    DB_URL: str = "postgresql+pg8000://postgres:postgres@host.docker.internal/sebigy-hittaskolan"
    CELERY_BROKER_URL: str = "redis://host.docker.internal:6379"
    CELERY_RESULT_BACKEND: str = "redis://host.docker.internal:6379"
    CELERY_WORKER_NAME_PREFIX: str ="local_docker"


class TestConfig(DevelopmentConfig):
    #    DB_URL :str= "sqlite:///./test2.db?check_same_thread=False"
    DB_URL: str = "postgresql+pg8000://postgres:postgres@localhost/sebigy-hittaskolan_test"


config = dict(
    production=ProductionConfig,
    staging=StagingConfig,
    test=TestConfig,
    dev=DevelopmentConfig,
    dev_docker_local=DevelopmentDockerLocalConfig,
)

settings: Union[
    ProductionConfig,
    StagingConfig,
    TestConfig,
    DevelopmentConfig,
    DevelopmentDockerLocalConfig,
] = config[os.environ.get("FASTAPI_ENV", "production").lower()]()

print("config: Settings is " + str(settings))
