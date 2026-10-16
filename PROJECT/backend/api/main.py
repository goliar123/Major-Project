import sys
import os
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from config.logging_config import logger
from api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Failure Attribution API Server started.")
    yield
    logger.info("Failure Attribution API Server shutting down.")

app = FastAPI(
    title="Automated Failure Attribution for LLM-Based Multi-Agent Systems",
    description="Developer diagnostic backend for localizing root causes in multi-agent executions using dependency DAGs and backward causal traversal.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Streamlit / Frontend web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

from dataset.schema import MultiAgentTrace, AttributionVerdict, StepEvaluation
from api.routes import ingest_trace, evaluate_step, resolve_attribution, EvaluateStepRequest

@app.post("/ingest", tags=["Root Aliases (Slide Deck Specs)"])
async def root_ingest(trace: MultiAgentTrace):
    return await ingest_trace(trace)

@app.post("/evaluate", response_model=StepEvaluation, tags=["Root Aliases (Slide Deck Specs)"])
async def root_evaluate(req: EvaluateStepRequest):
    return await evaluate_step(req)

@app.post("/resolve", response_model=AttributionVerdict, tags=["Root Aliases (Slide Deck Specs)"])
async def root_resolve(trace: MultiAgentTrace):
    return await resolve_attribution(trace)

@app.get("/")
async def root():
    return {
        "title": "Automated Failure Attribution for LLM Multi-Agent Systems",
        "status": "online",
        "docs_url": "/docs",
        "version": "1.0.0",
        "endpoints": {
            "ingest": ["/ingest", "/api/v1/ingest"],
            "evaluate": ["/evaluate", "/api/v1/evaluate"],
            "resolve": ["/resolve", "/api/v1/resolve", "/api/v1/attribute"],
            "overview": "/api/v1/overview",
            "traces": "/api/v1/traces",
            "benchmark": "/api/v1/benchmark/run",
            "cache": "/api/v1/cache/stats"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
