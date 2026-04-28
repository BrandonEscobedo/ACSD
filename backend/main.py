from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import assignment, reports
from app.api.routers import monitor as monitor_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Cleanup on shutdown
    from app.api.dependencies import get_monitor
    await get_monitor().stop_auto()


app = FastAPI(title="ACSD Monitor API", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(monitor_router.router)
app.include_router(assignment.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
