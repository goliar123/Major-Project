"""
FastAPI Route Handlers for Automated Failure Attribution.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from dataset.schema import (
    MultiAgentTrace,
    AttributionVerdict,
    BenchmarkResult,
    ExecutionStep,
    StepEvaluation
)
from dataset.loader import dataset_loader
from core.engine import attribution_engine
from core.cache import cache_manager
from core.segmentation import trace_segmenter
from core.dependency_linker import dependency_linker
from core.step_judge import step_judge
from evaluation.evaluator import benchmark_evaluator
from config.settings import settings
from config.logging_config import logger

router = APIRouter(prefix="/api/v1", tags=["Failure Attribution"])

class RawLogRequest(BaseModel):
    task_goal: str
    log_text: str

class EvaluateStepRequest(BaseModel):
    task_goal: str
    step: ExecutionStep

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Automated Failure Attribution Engine"}

@router.get("/overview")
async def get_overview():
    """Returns real-time system metrics, loaded traces count, and environment distributions."""
    traces = dataset_loader.load_traces()
    envs: Dict[str, int] = {}
    for t in traces:
        envs[t.environment_name] = envs.get(t.environment_name, 0) + 1
    cache_stats = cache_manager.get_stats()
    return {
        "status": "online",
        "app_name": settings.APP_NAME,
        "llm_model": settings.LLM_MODEL,
        "llm_provider": settings.LLM_PROVIDER,
        "cache_backend": settings.CACHE_BACKEND,
        "total_traces": len(traces),
        "environments": envs,
        "cache_stats": cache_stats,
        "algorithms": ["proposed", "all_at_once", "step_by_step", "binary_search"]
    }

@router.get("/environments")
async def list_environments():
    """Lists distinct multi-agent environments with trace counts."""
    traces = dataset_loader.load_traces()
    envs: Dict[str, int] = {}
    for t in traces:
        envs[t.environment_name] = envs.get(t.environment_name, 0) + 1
    return envs

@router.get("/synthetic/presets")
async def get_synthetic_presets():
    """Returns curated synthetic test traces demonstrating distinct failure patterns."""
    return [
        {
            "id": "preset_sql_injection",
            "title": "Database Schema Drop & Corrupt State Injection",
            "environment_name": "AutoGen",
            "task_goal": "Migrate user authentication schema to support OAuth2 without dropping existing tables.",
            "steps": [
                {
                    "step_index": 0,
                    "agent_name": "ProductManager",
                    "action_payload": "Require addition of oauth_provider and oauth_uid columns to users table."
                },
                {
                    "step_index": 1,
                    "agent_name": "DBArchitect",
                    "action_payload": "DROP TABLE users CASCADE; CREATE TABLE users (id SERIAL PRIMARY KEY, oauth_provider VARCHAR(50));"
                },
                {
                    "step_index": 2,
                    "agent_name": "BackendEngineer",
                    "action_payload": "SELECT count(*) FROM users; -> ERROR: 0 rows returned, all user data lost."
                },
                {
                    "step_index": 3,
                    "agent_name": "QAValidator",
                    "action_payload": "AssertionError: Expected 1500 active user records, got 0."
                }
            ],
            "expected_blame": "DBArchitect",
            "expected_step": 1
        },
        {
            "id": "preset_hallucinated_param",
            "title": "Autonomous Drone Pathfinding - Hallucinated Coordinate",
            "environment_name": "MetaGPT",
            "task_goal": "Plan collision-free waypoint trajectory through urban corridor.",
            "steps": [
                {
                    "step_index": 0,
                    "agent_name": "PerceptionAgent",
                    "action_payload": "Detected high-rise tower at GPS coordinates (37.7749, -122.4194, altitude 120m)."
                },
                {
                    "step_index": 1,
                    "agent_name": "PathPlanner",
                    "action_payload": "Generating trajectory: Waypoint 1 = (37.7749, -122.4194, altitude 80m). Direct straight-line path selected."
                },
                {
                    "step_index": 2,
                    "agent_name": "FlightController",
                    "action_payload": "Cruising towards waypoint (37.7749, -122.4194, 80m). Proximity sensor triggered at t=12s."
                },
                {
                    "step_index": 3,
                    "agent_name": "EmergencyModule",
                    "action_payload": "CRASH: Collision with structure at (37.7749, -122.4194, 80m). Mission aborted."
                }
            ],
            "expected_blame": "PathPlanner",
            "expected_step": 1
        },
        {
            "id": "preset_schema_mismatch",
            "title": "Payment Microservice ETL - Type Coercion Crash",
            "environment_name": "ChatDev",
            "task_goal": "Process customer subscription renewal billing event.",
            "steps": [
                {
                    "step_index": 0,
                    "agent_name": "WebhookIngestor",
                    "action_payload": "Received payload: {customer_id: 'cust_9012', amount_cents: '4999' (string)}."
                },
                {
                    "step_index": 1,
                    "agent_name": "DataTransformer",
                    "action_payload": "Pass raw payload to billing_gateway without parsing integer: payload['amount_cents'] left as str."
                },
                {
                    "step_index": 2,
                    "agent_name": "StripeGatewayClient",
                    "action_payload": "Executing stripe.Charge.create(amount=payload['amount_cents']) -> TypeError: unsupported operand type for int addition."
                },
                {
                    "step_index": 3,
                    "agent_name": "AlertManager",
                    "action_payload": "Critical 500 error logged: Unhandled TypeError in payment gateway."
                }
            ],
            "expected_blame": "DataTransformer",
            "expected_step": 1
        }
    ]

@router.post("/parse/raw_log", response_model=AttributionVerdict)
async def parse_and_attribute_raw_log(req: RawLogRequest):
    """Directly segments unstructured console text log and returns root-cause diagnosis."""
    try:
        custom_trace = trace_segmenter.parse_raw_log_text(req.log_text, task_goal=req.task_goal)
        verdict = attribution_engine.attribute_trace(custom_trace)
        return verdict
    except Exception as e:
        logger.error(f"Raw log attribution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/parse/custom_json", response_model=AttributionVerdict)
async def parse_and_attribute_custom_json(payload: Dict[str, Any]):
    """Parses arbitrary multi-agent JSON payload (AutoGen/CrewAI/LangGraph) and attributes failure."""
    try:
        custom_trace = trace_segmenter.parse_custom_json(payload)
        verdict = attribution_engine.attribute_trace(custom_trace)
        return verdict
    except Exception as e:
        logger.error(f"Custom JSON attribution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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

@router.post("/resolve", response_model=AttributionVerdict)
async def resolve_attribution(trace: MultiAgentTrace):
    """
    Direct alias for /attribute (specified in Slide 4 & Chapter 3 of Project Phase-1 report).
    Executes Two-Phase Backward Causal Traversal to resolve the originating root-cause s*.
    """
    return await attribute_trace(trace)

@router.post("/ingest")
async def ingest_trace(trace: MultiAgentTrace):
    """
    Ingests a multi-agent trace, enforces token context ceiling, and builds dependency DAG.
    Specified in Slide 4 & Chapter 3 as core ingestion endpoint.
    """
    try:
        segmented_steps = trace_segmenter.segment_trace(trace)
        dag, edges = dependency_linker.build_dependency_dag(segmented_steps)
        return {
            "status": "ingested",
            "trace_id": trace.trace_id,
            "total_steps": len(segmented_steps),
            "dag_nodes_count": dag.number_of_nodes(),
            "dag_edges_count": len(edges),
            "edges": edges
        }
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate", response_model=StepEvaluation)
async def evaluate_step(req: EvaluateStepRequest):
    """
    Evaluates a discrete execution step against task goals using the cached StepJudge.
    Specified in Slide 4 & Chapter 3 as core step-wise evaluator endpoint.
    """
    try:
        return step_judge.evaluate_step(req.task_goal, req.step)
    except Exception as e:
        logger.error(f"Step evaluation failed: {e}")
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
