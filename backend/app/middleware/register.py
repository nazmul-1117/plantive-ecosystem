from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.process_time import process_time_middleware
from app.middleware.request_uid import request_uid_middleware
from app.middleware.logging import logging_middleware
from app.middleware.exception_logging import exception_logging_middleware
from app.middleware.security_headers import security_header_middleware

from app.core.config import settings


def register_middleware(app: FastAPI):

    # custom middleware
    app.middleware("http")(request_uid_middleware)
    app.middleware("http")(exception_logging_middleware)
    app.middleware("http")(logging_middleware)
    app.middleware("http")(security_header_middleware)

    # pre-build-middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins = settings.ALLOWED_ORIGINS,
        allow_credentials = True,
        allow_methods = settings.ALLOWED_METHODS,
        allow_headers = settings.ALLOWED_HEADERS,
    )
