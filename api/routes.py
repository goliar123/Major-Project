"""
FastAPI Route Handlers for Automated Failure Attribution.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from typing import List, Optional, Dict, Any
from dataset.schema import (
    MultiAgentTrace,
    AttributionVerdict,
    BenchmarkResult,
    ExecutionStep
)
from dataset.loader import dataset_loader
from core.engine import attribution_engine
from core.cache import cache_manager
from evaluation.evaluator import benchmark_evaluator
from config.logging_config import logger

router = APIRouter(prefix="/api/v1", tags=["Failure Attribution"])

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Automated Failure Attribution Engine"}

@router.post("/attribute", response_model=AttributionVerdict)
async def attribute_trace(trace: MultiAgentTrace):
    """
    Analyzes a failed multi-agent execution trace and pinpoints:
    1. The responsible agent
    2. The decisive root-cause error step
    3. Causal DAG and explanatory justification
    """
    try:
        verdict = attribution_engine.attribute_trace(trace)
        return verdict
    except Exception as e:
        logger.error(f"Attribution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/traces", response_model=List[MultiAgentTrace])
async def list_benchmark_traces(
    subset: Optional[str] = Query(None, description="hand_crafted or algorithm_generated"),
    limit: Optional[int] = Query(None, description="Max traces to return")
):
    """Lists available Who&When benchmark traces."""
    traces = dataset_loader.load_traces(subset=subset)
    if limit:
        traces = traces[:limit]
    return traces

@router.get("/traces/{trace_id}", response_model=MultiAgentTrace)
async def get_trace_by_id(trace_id: str):
    """Retrieves a single trace by ID."""
    trace = dataset_loader.get_trace_by_id(trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail=f"Trace with ID '{trace_id}' not found.")
    return trace

@router.post("/benchmark/run", response_model=BenchmarkResult)
async def run_benchmark(
    method: str = Query("proposed", description="Method to evaluate: proposed, all_at_once, step_by_step, binary_search"),
    subset: Optional[str] = Query(None, description="hand_crafted, algorithm_generated, or null for all"),
    limit: Optional[int] = Query(None, description="Limit traces for evaluation")
):
    """Runs benchmark evaluation and returns accuracy and efficiency metrics."""
    try:
        result = benchmark_evaluator.evaluate_method(
            method_name=method,
            subset=subset,
            max_traces=limit
        )
        return result
    except Exception as e:
        logger.error(f"Benchmark run failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cache/stats")
async def get_cache_statistics():
    """Returns SHA256 prompt hashing cache statistics."""
    return cache_manager.get_stats()

@router.post("/cache/clear")
async def clear_cache():
    """Clears the evaluation prompt cache."""
    cache_manager.clear()
    return {"message": "Cache successfully cleared."}

# Live Streaming Session Endpoints
from core.live_monitor import live_trace_monitor

@router.post("/live/start")
async def start_live_session(trace_id: str, task_goal: str, expected_output: Optional[str] = None):
    """Initializes a real-time streaming trace session."""
    session = live_trace_monitor.start_session(trace_id=trace_id, task_goal=task_goal, expected_output=expected_output)
    return {"status": "started", "trace_id": session.trace_id, "goal": session.task_goal}

@router.post("/live/ingest")
async def ingest_live_step(trace_id: str, step: ExecutionStep):
    """Incrementally ingests a step, builds DAG node, and evaluates in shadow memory."""
    session = live_trace_monitor.get_session(trace_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Live session '{trace_id}' not found.")
    evaluation, edges = session.ingest_step(step)
    return {
        "step_index": step.step_index,
        "score": evaluation.score,
        "anomaly_detected": evaluation.anomaly_detected,
        "new_edges_count": len(edges)
    }

@router.post("/live/finish")
async def finish_live_session(trace_id: str, final_output: str = "", status: str = "COMPLETED"):
    """Concludes session; evaluates terminal conflict and returns attribution if failed."""
    session = live_trace_monitor.get_session(trace_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Live session '{trace_id}' not found.")
    verdict = session.finish_session(final_output=final_output, status=status)
    live_trace_monitor.close_session(trace_id)
    return {
        "status": "concluded",
        "clean_run": verdict is None,
        "verdict": verdict
    }
