import uuid

from fastapi import HTTPException, Request
from fastapi.exceptions import ValidationException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from log import app_logger, request_id_ctx_var


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())

        request_id_ctx_var.set(request_id)

        app_logger.info(
            f"Request: {request.method} {request.url.path}",
        )
        try:
            response = await call_next(request)
            app_logger.info(
                f"Response: {response.status_code} {request.method} {request.url.path}",
            )
            response.headers["X-Request-ID"] = request_id
            return response
        except HTTPException as http_exception:
            return JSONResponse(
                status_code=http_exception.status_code,
                content={"error": "Client Error", "message": str(http_exception.detail)},
            )
        except ValidationException as e:
            app_logger.error(f"Exception - {e.__class__.__name__}, Detail - {e}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Client Error", "message": str(e.message)},
            )
        # except Exception as e:
        #     app_logger.error(f"Exception - {e.__class__.__name__}, Detail - {e}")
        #     return JSONResponse(
        #         status_code=500,
        #         content={"error": "Internal Server Error"},
        #     )