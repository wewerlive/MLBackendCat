import asyncio
from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi import Security, status
from fastapi.security import APIKeyHeader
from concurrent.futures import ThreadPoolExecutor

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*"
]

# from serverUtils.modelUtils import predictTryOn

from fastapi import FastAPI, Depends
from routers import business, public, internal
from serverUtils.auth import getBusinessUser
from serverUtils.db import startup_db_client, shutdown_db_client

# import for fast api lifespan
from contextlib import asynccontextmanager

from serverUtils.requestModels import TryRequest

# define a lifespan method for fastapi
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the database connection
    await startup_db_client(app)
    yield
    # Close the database connection
    await shutdown_db_client(app)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    public.router,
    prefix="/api/v1/public"
)
app.include_router(
    business.router,
    prefix="/api/v1/business",
    dependencies=[Depends(getBusinessUser)]
)

app.include_router(
    internal.router,
    prefix="/api/v1/internal"
)



@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.post("/tryon")
# async def tryon(tryRequest: TryRequest):
#     try:
#         result = await asyncio.get_event_loop().run_in_executor(
#             executor,
#             predictTryOn,
#             tryRequest.personImage,
#             tryRequest.clothImage,
#             tryRequest.clothType,
#             tryRequest.num_inference_steps,
#             tryRequest.seed,
#             tryRequest.guidance_scale
#         )
#         # result = predictTryOn(
#         #     tryRequest.personImage,
#         #     tryRequest.clothImage,
#         #     tryRequest.clothType,
#         #     tryRequest.num_inference_steps,
#         #     tryRequest.seed,
#         #     tryRequest.guidance_scale
#         # )
#         return {"result": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
