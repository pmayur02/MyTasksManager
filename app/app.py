from fastapi import FastAPI,  Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers.tasks import taskRouter
from app.routers.users import userRouter
from app.database.db import engine
import app.models.models as model
from fastapi.middleware.cors import CORSMiddleware
from app.utilities.config import FRONTEND_URL

model.Base.metadata.create_all(bind = engine)


app = FastAPI()

app.include_router(taskRouter)
app.include_router(userRouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    # Return your own JSON structure
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Validation failed",
            "details": exc.errors()
        }
    )



