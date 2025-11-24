from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        field = error["loc"][-1] if len(error["loc"]) > 1 else "general"
        msg = error["msg"]
        if "whitespace" in msg.lower():
            msg = f"No whitespace in {field} is allowed"
        errors.setdefault(field, []).append(msg)
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": errors}
    )
