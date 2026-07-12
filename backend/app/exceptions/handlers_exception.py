import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions.base_exception import AppException

logger = logging.getLogger(__name__)

def register_exception_handler(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException
    ):
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message
                },
            },
        )
    
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):
        """
        Handle unhandled error
        """
        
        logger.exception("Unhandler exception")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Internal server error"
                },
            },
        )
        