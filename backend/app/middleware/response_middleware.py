from fastapi import Request
from fastapi.responses import JSONResponse


async def response_wrapper(request: Request, call_next):

    response = await call_next(request)

    # Don't wrap Swagger/OpenAPI and Auth responses
    if request.url.path in [
        "/openapi.json",
        "/docs",
        "/redoc",
        "/auth/login",
        "/auth/me",
        "/auth/google-login",
        "/auth/register"
    ]:
        return response

    if response.headers.get("content-type") == "application/json":

        body = b""

        async for chunk in response.body_iterator:
            body += chunk


        import json

        try:

            data = json.loads(body)


            # Don't wrap already formatted responses
            if (
                isinstance(data, dict)
                and "success" in data
            ):
                return JSONResponse(
                    content=data,
                    status_code=response.status_code
                )


            return JSONResponse(
                content={
                    "success": True,
                    "data": data
                },
                status_code=response.status_code
            )


        except Exception:
            pass


    return response