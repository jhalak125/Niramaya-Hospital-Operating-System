import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


logger = logging.getLogger(__name__)


async def http_exception_handler(
    request: Request,
    exc: HTTPException
):

    logger.error(
        f"{request.method} {request.url} - {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    logger.error(
        f"Validation error: {exc.errors()}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "errors": exc.errors()
        }
    )


async def global_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(
        f"Unexpected error: {str(exc)}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc)
        }
    )