import os
import datetime
from fastapi import FastAPI, status
from pydantic import BaseModel
from contextlib import asynccontextmanager

# SQLAlchemy async tools
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# ==========================================
# 1. INFRASTRUCTURE & DATABASE CONFIG
# ==========================================
# Environment variable injected via Kubernetes Secret/ConfigMap
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://fake_user:fake_password@db-server:5432/fake_db"
)

# Database engine and session factory
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# ==========================================
# 2. DATA MODELS & SCHEMAS
# ==========================================
# Database Table Schema (SQLAlchemy)
Base = declarative_base()

class TelemetryModel(Base):
    __tablename__ = "transformer_telemetry"

    id = Column(Integer, primary_key=True)
    current = Column(Float)
    voltage = Column(Float)
    temperature = Column(Float)

# API Request Validation Schema (Pydantic)
class TelemetryScheme(BaseModel):
    current: float
    voltage: float
    temperature: float

# ==========================================
# 3. LIFECYCLE & APPLICATION SETUP
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Attempts database connection on startup (creates tables if DB is available)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Warning: Could not connect to database yet (expected in DevOps environments): {e}")
    yield
    # Cleans up database connection pool on shutdown
    await engine.dispose()

# Initialize FastAPI with lifecycle manager
app = FastAPI(
    title="Transformer Telemetry API",
    description="Asynchronous microservice for collecting transformer telemetry data",
    version="1.0.0",
    lifespan=lifespan
)

# ==========================================
# 4. API ENDPOINTS (ROUTES)
# ==========================================

# 4.1. Health Check (Critical for Kubernetes Liveness / Readiness Probes)
@app.get("/", status_code=status.HTTP_200_OK)
@app.get("/healthz", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Kubernetes calls this endpoint to check if the Pod is alive and healthy.
    """
    return {
        "status": "healthy",
        "service": "transformer-telemetry-api",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

# 4.2. Telemetry Data Ingestion Endpoint
@app.post("/telemetry", status_code=status.HTTP_201_CREATED)
async def receive(data: TelemetryScheme):
    """
    Ingests current, voltage, and temperature data from transformer sensors and persists it to PostgreSQL.
    """
    async with async_session() as session:
        new_data = TelemetryModel(
            current=data.current,
            voltage=data.voltage,
            temperature=data.temperature
        )
        session.add(new_data)
        await session.commit()

    return {
        "message": "Data received and saved to PostgreSQL successfully",
        "data": data.model_dump()
    }
