import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from .api.routers.submissions import router as submissions_router
from .exceptions import validation_exception_handler
from .middleware import RandomDelayMiddleware

app = FastAPI()

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
origins = [o.strip() for o in origins if o.strip()]

app.add_middleware(RandomDelayMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.exception_handler(RequestValidationError)(validation_exception_handler)
app.include_router(submissions_router)
