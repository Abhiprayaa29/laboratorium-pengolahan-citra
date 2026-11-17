"""Main FastAPI Application Entrypoint for Laboratorium Pengolahan Citra Digital (LPCD)."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.health import router as health_router
from app.api.v1.histogram import router as histogram_router
from app.api.v1.images import router as images_router
from app.api.v1.operations import router as operations_router
from app.api.v1.pipeline import router as pipeline_router
from app.core.registry.loader import register_all_operations

# Pre-register operations on module import
register_all_operations()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure all operations are loaded on startup
    register_all_operations()
    yield


app = FastAPI(
    title="Laboratorium Pengolahan Citra Digital (LPCD) API",
    description=(
        "Platform Web Akademik Pengolahan Citra Digital Modular berbasis Python, OpenCV, dan FastAPI.\n\n"
        "Arsitektur dirancang untuk kolaborasi 4 anggota kelompok praktikum dengan registrasi operasi terisolasi."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
raw_origins = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = [
    origin.strip()
    for origin in raw_origins.split(",")
    if origin.strip()
]

# Standard local development origins
default_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:3000",
]

merged_origins = list(set(default_origins + allowed_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=merged_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 Routers
api_v1_prefix = "/api/v1"
app.include_router(health_router, prefix=api_v1_prefix)
app.include_router(operations_router, prefix=api_v1_prefix)
app.include_router(images_router, prefix=api_v1_prefix)
app.include_router(pipeline_router, prefix=api_v1_prefix)
app.include_router(histogram_router, prefix=api_v1_prefix)


@app.get("/")
def root():
    return {
        "message": "Laboratorium Pengolahan Citra Digital (LPCD) API Berjalan.",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
